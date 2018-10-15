import hardware as hwutil
import software as swutil


class env():
    def __init__(self):
        self.cpu_conf = hwutil.CPU_conf()
        self.nics_conf = hwutil.NICs_conf()
        self.sw_conf = swutil.Software_conf()

g_env_conf = env()
