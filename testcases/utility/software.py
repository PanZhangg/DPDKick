import utilities as util
import globalvar

"""
DPDK software related utility functions
"""

class software_base():
    def __init__(self):
        self.pid = self.__get_sw_pid()
        self.pid_exists = self.__check_pid_is_exists(self.pid)

    """
    Software PID is read from file dpdkick.conf
    TODO: Automatic detect from the env
    """
    def __get_sw_pid(self):
        return util.get_dpdk_app_pid()
        #TODO: uncomment below
        #pid = util.get_dpdk_app_pid()
        #exist = self.__check_pid_is_exists(pid)
        #if exist == False:
        #    print 'PID not exists'
        #    raise SystemExit

    def __check_pid_is_exists(self, pid):
        pids = util.get_all_sys_pids()
        if pid in pids:
            return True
        else:
            return False

    """
    Code to parse proc/pid/stat file, thanks to psutil project
    """
    def parse_stat_file(self, pid):
        with util.open_binary("%s/%s/stat" % ("/proc", pid)) as f:
            data = f.read()
        rpar = data.rfind(b')')
        name = data[data.find(b'(') + 1:rpar]
        others = data[rpar + 2 :].split()
        return [name] + others

class sw_runtime_telemetry(software_base):
    def __init__(self):
        software_base.__init__(self)
        self.mem_bandwidth = 0
        self.process_context_switch_rate = 0
        self.cpus_ipc = []

    def update_all(self):
        pass

class Software_conf(software_base):
    def __init__(self):
        software_base.__init__(self)
        if self.pid_exists == False:
            print "PID does not exists, some software tests will be skipped"
            self.process_name = "None"
        else:
            self.process_name = self.__get_process_name(self.pid)
            self.cpu_mask = self.__get_cpu_mask()
            self.thread_num = self.__get_sw_threads_num(self.pid)
            self.master_cpu_core = self.__get_sw_master_cpu_core()


    """
    Software cpu mask for pinning workload to
    certain cpu cores is read from file dpdkick.conf
    """
    def __get_cpu_mask(self):
        return util.get_cpu_mask()

    def __get_sw_master_cpu_core(self):
        return util.get_dpdk_master_cpu()

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

    def __get_process_name(self, pid):
        name = self.parse_stat_file(pid)[0]
        return name

    def __get_sw_threads_num(self, pid):
        command = 'ps -o nlwp ' + str(pid)
        output = util.str_cmd_output(command)
        l = output.split('\n')[1]
        if l == '':
            globalvar.CONF_PID_IS_VALID = False
        else:
            return int(l)
