import os
import functools

from celery import task
from psutil import Process

from .models import Submission
from .container import Container


def ensure_cleanup(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        c = fn(*args, **kwargs)
        c.cleanup()
    return wrapper


@task
@ensure_cleanup
def judge(submission_id):
    s = Submission.objects.get(pk=submission_id)
    s.state = 'processing'
    s.save()
    p = s.problem
    c = Container('c{}'.format(s.id))
    c.init()
    dump_src(s.id, s.source_code)
    dump_test(c.rootfs, p.test_input)

    if not make(c.rootfs, s.id):
        s.set_verdict('compilation error')
        return c

    c.clear_timer()
    pid = c.run_cmd(['/{} < test.in > test.out'.format(submission_id)])
    process = Process(pid)
    time_limit = p.time_limit

    while True:
        if sum(process.cpu_times()) > time_limit or not process.is_running():
            break

    if c.running_time() > time_limit:
        s.set_verdict('time limit exceed')
        return c
    if c.exceed_memory_limit():
        s.set_verdict('memory limit exceed')
        return c

    test_output = p.test_output.split('\n\r')

    with open(c.rootfs+'/test.out') as f:
        i = 0
        for line in f:
            if line != test_output[i]:
                s.set_verdict('wrong answer')
                return c
            i += 1
    s.set_verdict('Accepted')
    return c


def dump_src(s_id, src):
    """dump source code to a tmp file"""
    with open('/tmp/{}.cpp'.format(s_id), 'w') as f:
        f.write(src)


def dump_test(c_root, test_input):
    """dump test input to container's filesystem"""
    with open(c_root + '/test.in', 'w') as f:
        f.write(test_input)


def make(c_root, s_id):
    """
    c_root: container's root path
    s_id: submission id

    compile source code"""
    cmd = 'clang++ -std=c++11 /tmp/{}.cpp -o {}/{}'.format(s_id, c_root, s_id)
    pipe = os.popen(cmd)
    return pipe.close() is None


def compare_output():
    pass
