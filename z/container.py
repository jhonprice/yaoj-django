import lxc


class Container(lxc.Container):
    """Customize Container class to meet our need."""
    def __str__(self):
        return "Container: {}\nState: {}\n".format(self.name, self.state)

    def clear_timer(self):
        return self.set_cgroup_item('cpuacct.usage', '0')

    def init(self):
        if self.defined:
            self.cleanup()
        self.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu",
                                                       "release": "trusty",
                                                       "arch": "amd64"})
        self.start()

    def cleanup(self):
        self.stop()
        self.destroy()

    def run_cmd(self, cmd):
        return self.attach(lxc.attach_run_command, cmd)

    @property
    def running_time(self):
        return int(self.get_cgroup_item('cpuacct.usage'))/1000

    @property
    def exceed_memory_limit(self):
        return int(self.get_cgroup_item('memory.memsw.failcnt')) > 0

    @property
    def arch(self):
        return self.get_config_item('lxc.arch')

    @property
    def rootfs(self):
        return self.get_config_item('lxc.rootfs')


def list_containers():
    """Make lxc.list_containers fits customized Container class."""
    for name in lxc.list_containers():
        yield Container(name)


def init_containers(num_containers=2):
    """Every time the daemon start, we recreate containers to make sure
    the containers are what we want."""
    for i in range(num_containers):
        c = Container("c{:0=2}".format(i))
        if c.defined:
            if not c.shutdown():
                c.stop()
            c.destroy()
            c = Container("c{:0=2}".format(i))
        c.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu",
                                                    "release": "trusty",
                                                    "arch": "amd64"})
