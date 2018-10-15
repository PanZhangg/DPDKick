import hardware as hwutil
import software as swutil
import kernel as kernelutil

class env():
    def __init__(self):
        self.cpu_conf = hwutil.CPU_conf()
        self.nics_conf = hwutil.NICs_conf()
        self.sw_conf = swutil.Software_conf()
        self.rt_telemetry = swutil.sw_runtime_telemetry()
        self.kernel = kernelutil.Kernel_conf()

    def rt_telemetry_update_all(self):
        self.rt_telemetry.update_all()

g_env_conf = env()
