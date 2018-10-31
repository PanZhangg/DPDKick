import hardware as hwutil
import software as swutil
import kernel as kernelutil
import utilities as util
import globalvar

class env():
    def __init__(self):

        #system variables detection and init
        self.cpu_conf = hwutil.CPU_conf()
        self.nics_conf = hwutil.NICs_conf()
        self.mem_conf = hwutil.Memory_conf()
        self.sw_conf = swutil.Software_conf()
        self.rt_telemetry = swutil.sw_runtime_telemetry()
        self.kernel = kernelutil.Kernel_conf()
        self.hugepage_mem = kernelutil.Huagepage_conf()

        #globalvar init
        globalvar.CONF_PID_IS_VALID = util.check_conf_file_is_completed()
        globalvar.MSR_TOOLS_IS_INSTALLED = util.check_if_command_exists('rdmsr')
        globalvar.PERF_TOOLS_IS_INSTALLED = util.check_if_command_exists('pcm.x')

    def rt_telemetry_update_all(self):
        self.rt_telemetry.update_all()

g_env_conf = env()
