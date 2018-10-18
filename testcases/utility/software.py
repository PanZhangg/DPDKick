import utilities as util

"""
DPDK software related utility functions
"""
class sw_runtime_telemetry():
    def __init__(self):
        self.mem_bandwidth = 0
        self.process_context_switch_rate = 0
        self.cpus_ipc = []

    def update_all(self):
        pass

class Software_conf():
    def __init__(self):
        self.pid = self.get_sw_pid()
        self.cpu_mask = self.get_cpu_mask()
        self.thread_num = 0

    """
    Software PID is read from file dpdkick.conf
    TODO: Automatic detect from the env
    """
    def get_sw_pid(self):
        return util.get_dpdk_app_pid()

    def get_cpu_mask(self):
        return util.get_cpu_mask()

    def get_cpu_list_by_mask(self, cpu_total_num):
        n = util.convert_cpu_mask_into_int(self.cpu_mask)
        l = [] 
        for i in range(cpu_total_num):
            if n == 0:
                break
            if (n & 0x1) == 1:
                l.append(i)
            n = n >> 1
        return l 

    def get_sw_threads_num(self):
        pass
