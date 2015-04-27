import os
import shutil
from subprocess import PIPE
from functools import partial

from celery import shared_task
from psutil import Popen, TimeoutExpired

from .models import Submission


TMP = '/tmp'


@shared_task
def judge(submission_id):
    submission = Submission.objects.get(pk=submission_id)
    submission.set_state('processing')
    problem = submission.problem

    base_dir = os.path.join(TMP, 'oj_{}'.format(submission_id))
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.mkdir(base_dir)

    get_path = partial(os.path.join, base_dir)

    dump_file(get_path('main.cpp'), submission.source_code)
    dump_file(get_path('test.in'), problem.test_input)
    dump_file(get_path('answer'), problem.test_output)

    submission.set_state('compiling')
    ok, msg = make(base_dir)
    if not ok:
        submission.set_verdict('compile error')
        return

    submission.set_state('running')
    ok, msg = run(base_dir, problem.time_limit/1000)
    if not ok:
        submission.set_verdict(msg)
        return

    if compare(get_path('answer'), get_path('test.out')):
        submission.set_verdict('accepted')
    else:
        submission.set_verdict('wrong answer')


def make(base_dir, timeout=5):
    """compile source code.

    return (ok?, msg)"""
    cmd = ['clang++', '-std=c++11', 'main.cpp']
    p = Popen(cmd, stderr=PIPE, cwd=base_dir)
    try:
        p.wait(timeout)
    except TimeoutExpired:
        return False, 'compilation take too much time.'
    else:
        if p.returncode == 0:
            return True, ''
        else:
            return False, p.communicate()[1]


def run(base_dir, timeout):
    """run the program.

    return (ok?, msg)"""
    cmd = ['./a.out']
    out_path = os.path.join(base_dir, 'test.out')
    in_path = os.path.join(base_dir, 'test.in')
    with open(out_path, 'w') as fout, open(in_path) as fin:
        p = Popen(cmd, stdin=fin, stdout=fout, cwd=base_dir)
        try:
            p.wait(timeout)
        except TimeoutExpired:
            p.kill()
            return False, 'time limit exceed'
        else:
            if p.returncode == 0:
                return True, ''
            else:
                return False, 'runtime error'


def compare(answer_path, output_path):
    """compare two file, ignore whitespace in the start of line and the end
    of line"""
    with open(answer_path) as answer, open(output_path) as output:
        for line in answer:
            if line.strip() != output.readline().strip():
                return False
    return True


def dump_file(path, content):
    """dump file from database to file system."""
    with open(path, 'w') as f:
        f.write(content)
        f.write('\n')

