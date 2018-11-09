import os
import utilities as util
import globalvar

"""
CPU related configurations
"""

class CPU_conf:
    def __init__(self):
        self.str_CPU_code_name = self.__get_CPU_code_name()
        self.str_instruction_supported = self.get_CPU_instructions_supported()
        self.cpu_total_num = self.__get_cpu_total_num()
        self.b_hyperthread_enabled = self.__hyperthread_is_enabled()
        self.b_pstate_disabled = self.__intel_pstate_is_disabled()
        self.b_turbo_disabled = self.__turbo_is_disabled()
        self.b_c6state_disabled = self.__c6state_disabled()
        self.b_c3state_disabled = self.__c3state_disabled()
        self.b_direct_cache_access_enabled = self.__dca_is_enabled()
        self.scaling_governor = self.__get_scaling_governor()
        self.cpu_core_total_num = self.__get_core_total_num()
        self.cores = []
        self.init_all_cpus_conf()

    """
    CPU related utility functions
    """

    def __print_lscpu_cmd(self):
        return util.str_cmd_output('lscpu')

    def __print_lscpu_e_cmd(self):
        return util.str_cmd_output('lscpu -e')

    def __get_lscpu_specific_conf(self, spec):
        return util.str_get_specific_value_after_colon('lscpu', spec)

    def get_lscpu_e_specific_conf(self, cpu_id, column):
        output = self.__print_lscpu_e_cmd();
        l = output.split('\n')
        l_title = l[0].split()
        ll = l[cpu_id + 1].split()
        column_idx = l_title.index(column)
        return ll[column_idx]

    def __get_cpu_total_num(self):
        output = self.__print_lscpu_cmd()
        num = self.__get_lscpu_specific_conf('CPU(s)')
        return int(num)

    def get_cpu_numa_node_by_cpu_id(self, cpu_id):
        return int(self.get_lscpu_e_specific_conf(cpu_id, 'NODE'))

    def get_cpu_core_by_cpu_id(self, cpu_id):
        return int(self.get_lscpu_e_specific_conf(cpu_id, 'CORE'))

    def init_all_cpus_conf(self):
        for i in range(self.cpu_total_num ):
            core = self.get_cpu_core_by_cpu_id(i)
            node = self.get_cpu_numa_node_by_cpu_id(i)
            single_cpu = Single_CPU_core_conf(cpu_id = i,
                                              core_num = core,
                                              numa_node = node)
            self.cores.append(single_cpu)

    def __get_CPU_code_name(self):
        output = self.__print_lscpu_cmd()
        name = self.__get_lscpu_specific_conf('Model name')
        return name

    def __hyperthread_is_enabled(self):
        output = self.__print_lscpu_cmd()
        tpc = self.__get_lscpu_specific_conf('Thread(s) per core')
        if int(tpc) == 1:
            return False
        else:
            return True

    def __turbo_is_disabled(self):
        output = util.get_cat_command_output('/sys/devices/system/cpu/intel_pstate/no_turbo')
        if output == None:
            return False
        if output == '0':
            return False
        else:
            return True

    def __dca_is_enabled(self):
        output = util.str_cmd_output('dmesg | grep dca')
        if output.find('disabled') == -1:
            return True
        else:
            return False

    def __get_core_total_num(self):
        if self.b_hyperthread_enabled == True:
            return (self.cpu_total_num / 2)
        else:
            return self.cpu_total_num

    def get_CPU_instructions_supported(self):
        pass

    def __intel_pstate_is_disabled(self):
        output = util.get_cat_command_output('/boot/config-$(uname -r) | grep -i pstate')
        if output is None:
            return True
        else:
            return False

    def __c6state_disabled(self):
        output = util.int_cmd_output('cat /sys/module/intel_idle/parameters/max_cstate')
        if output >= 6:
            return False
        else:
            return True

    def __c3state_disabled(self):
        output = util.int_cmd_output('cat /sys/module/intel_idle/parameters/max_cstate')
        if output >= 3:
            return False
        else:
            return True

    def __get_scaling_governor(self):
        ret = []
        output = util.get_cat_command_output('/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor')
        if output == None:
            return None
        l = output.split('\n')
        ret.append(l[0])
        for ll in l:
            if ll not in ret:
                ret.append(ll)
        return ret

    def get_single_CPU_conf_by_id(self, id):
        return self.cores[id]

class Single_CPU_core_conf:
    def __init__(self, cpu_id, core_num, numa_node):
        self.cpu_id = cpu_id
        self.core_num = core_num
        self.numa_node = numa_node

"""
Memory related configurations
"""

class Memory_conf:
    def __init__(self):
        self.memroy_total_size = self.__get_memory_total_size()
        self.memory_DIMM_num = self.__get_memory_DIMM_num()
        if self.memory_DIMM_num == 0:
            #Not running in a normal physical host env
            globalvar.NORMAL_PHY_HOST_MEM = False
            return
        self.memory_channels_num = self.__get_memory_channels_num()
        self.memory_DIMM_per_channel = self.memory_DIMM_num / self.memory_channels_num
        self.dmidecode_output = self.__get_dmidecode_output()
        self.dimms = []
        self.__init_memory_DIMMs()

    """
    Memory related utility functions
    """
    def __get_memory_total_size(self):
        cmd = 'cat /proc/meminfo'
        total = util.str_get_specific_value_after_colon(cmd, 'MemTotal')
        return total

    def __get_memory_DIMM_num(self):
        cmd = 'dmidecode -t memory | grep Locator | grep DIMM |wc -l'
        return util.int_cmd_output(cmd)

    def __get_memory_channels_num(self):
        cmd = 'dmidecode -t memory | grep Locator | grep DIMM | grep 1 |wc -l'
        return util.int_cmd_output(cmd)

    def __get_dmidecode_output(self):
        cmd = 'dmidecode -t memory'
        output = util.str_cmd_output(cmd)
        l = output.split('\n')
        return l

    def __init_memory_DIMMs(self):
        for i in range(self.memory_DIMM_num):
            locator = self.__get_mem_dimm_locator(i)
            size = self.__get_mem_dimm_size(i)
            speed = self.__get_mem_dimm_speed(i)
            conf_speed = self.__get_mem_conf_speed(i)
            node = self.__get_mem_bank_locator(i)
            dimm = Memory_DIMM(locator = locator, size = size,
                                speed = speed, conf_speed = conf_speed,
                                node = node)
            self.dimms.append(dimm)

    def __get_mem_dimm_spec_conf(self, conf, index):
        cnt = 0
        for l in self.dmidecode_output:
            if l.find(conf) != -1:
                if cnt == index:
                    return l.split(":")[1].strip()
                cnt = cnt + 1
        return None

    def __get_mem_dimm_locator(self, index):
        return self.__get_mem_dimm_spec_conf("Locator: DIMM", index)

    def __get_mem_dimm_size(self, index):
        return self.__get_mem_dimm_spec_conf("Size", index)

    def __get_mem_dimm_speed(self, index):
        cnt = 0
        for l in self.dmidecode_output:
            if l.find("Speed") != -1 and l.find("Configured") == -1:
                if cnt == index:
                    speed = l.split(":")[1].strip()
                    if speed != "Unknown":
                        return int(speed.split(" ")[0].strip())
                    else:
                        return speed
                cnt = cnt + 1
        return None

    def __get_mem_conf_speed(self, index):
        speed = self.__get_mem_dimm_spec_conf("Configured Clock Speed", index)
        if speed != "Unknown":
            return int(speed.split(" ")[0].strip())
        else:
            return speed

    def __get_mem_bank_locator(self, index):
        return self.__get_mem_dimm_spec_conf("Bank Locator", index)

class Memory_DIMM:
    def __init__(self, locator, size, speed, conf_speed, node):
        self.locator = locator
        self.memory_size = size
        self.memory_speed = speed
        self.memory_config_speed = conf_speed
        self.bank_node = node


"""
NIC related configurations
"""

class Single_NIC_conf:
    def __init__(self, lspci_vv_output, code_name, rx_q_num, tx_q_num,
                 numa_node, LnkCap, LnkSta, pci_addr,
                 cap_mpl, ctl_mpl, mrq, target_link_speed,
                 ker_drv):

        self.lspci_vv_output = lspci_vv_output
        self.nic_code_name = code_name
        self.rx_queue_num = rx_q_num
        self.tx_queue_num = tx_q_num
        self.NUMA_node = numa_node
        self.LnkCap = LnkCap
        self.LnkSta = LnkSta
        self.pcie_width = 0
        self.pcie_devcap_maxpayloadsize = cap_mpl
        self.pcie_devctl_maxpayloadsize = ctl_mpl
        self.pcie_maxreadreq = mrq
        self.pcie_targetlinkspeed = target_link_speed
        self.pci_address = pci_addr
        self.ker_drv_in_use = ker_drv


"""
class Single_NIC_conf_82599(Single_NIC_conf):
    def __init__(self):
        super.__init__(self)
"""

class NICs_conf:
    lspci_nic_cmd = 'lspci | grep Ether'

    def __init__(self):
        self.str_nic_pci_conf= self.print_nic_pci_conf()
        self.nic_total_num = self.get_nic_total_num()
        self.nics_conf = []
        self.init_all_nics_conf()

    """
    NIC related utility functions
    """
    def NIC_rx_queue_num(self):
        pass

    def NIC_tx_queue_num(self):
        pass

    def print_nic_pci_conf(self):
        output = os.popen(self.lspci_nic_cmd, 'r')
        return output.read()

    def get_nic_lspci_vv_output(self, pci_addr):
        command = 'lspci -s ' + pci_addr + ' -vv'
        return os.popen(command, 'r').read()

    def get_nic_total_num(self):
        command = self.lspci_nic_cmd + '|wc -l'
        output = os.popen(command, 'r')
        return int(output.read())

    def get_nic_pci_address(self, list_num):
        output = self.str_nic_pci_conf.splitlines()[list_num]
        return output[0 : 7]

    def get_nic_code_name(self, list_num):
        output = self.str_nic_pci_conf.splitlines()[list_num].split(':')[2]
        return output

    def get_nic_LnkCap(self, lspci_vv_output):
        loc = lspci_vv_output.rfind('LnkCap')
        str_tmp = lspci_vv_output[loc :]
        loc = str_tmp.find('Speed')
        return str_tmp[loc + 6 : loc + 11]

    def get_nic_LnkSta(self, lspci_vv_output):
        loc = lspci_vv_output.find('LnkSta')
        str_tmp = lspci_vv_output[loc :]
        loc = str_tmp.find('Speed')
        return str_tmp[loc + 6 : loc + 11]

    def get_nic_numa_node(self, lspci_vv_output):
        loc = lspci_vv_output.find('NUMA node')
        if loc == -1:
            return 0
        else:
            return int(lspci_vv_output[loc + 11 : loc + 12])

    def get_nic_devcap_maxpayload(self, lspci_vv_output):
        loc = lspci_vv_output.find('DevCap')
        if loc == -1:
            return None
        maxpayload = lspci_vv_output[loc + 19: loc + 23]
        return int(maxpayload)

    def get_nic_devctl_maxpayload(self, lspci_vv_output):
        loc = lspci_vv_output.find('DevCtl')
        if loc == -1:
            return None
        loc1 = lspci_vv_output[loc :].find('MaxPayload')
        if loc1 == -1:
            return None
        maxpayload = lspci_vv_output[loc + loc1 + 11: loc + loc1 + 15]
        return int(maxpayload)

    def get_nic_max_read_req(self, lspci_vv_output):
        loc = lspci_vv_output.find('MaxReadReq')
        if loc == -1:
            return None
        loc1 = lspci_vv_output[loc :].find('bytes')
        if loc1 == -1:
            return None
        maxreadreq = lspci_vv_output[loc + 10 : loc + loc1]
        return int(maxreadreq)

    def get_nic_target_link_speed(self, lspci_vv_output):
        loc = lspci_vv_output.find('Target Link Speed')
        if loc == -1:
            return None
        loc1 = lspci_vv_output[loc :].find('GT')
        tls = lspci_vv_output[loc + 19 : loc + loc1]
        return tls + 'GT/s'

    def get_nic_ker_drv_in_use(self, lspci_vv_output):
        loc = lspci_vv_output.find('Kernel driver in use')
        str_tmp = lspci_vv_output[loc :]
        return str_tmp[22 : 37]

    def init_single_nic_conf(self, list_num):
        pci_addr = self.get_nic_pci_address(list_num)
        lspci_vv_output = self.get_nic_lspci_vv_output(pci_addr)
        code_name = self.get_nic_code_name(list_num)
        numa_node = self.get_nic_numa_node(lspci_vv_output)
        LnkCap = self.get_nic_LnkCap(lspci_vv_output)
        LnkSta = self.get_nic_LnkSta(lspci_vv_output)
        devcap_maxpayload = self.get_nic_devcap_maxpayload(lspci_vv_output)
        devctl_maxpayload = self.get_nic_devctl_maxpayload(lspci_vv_output)
        max_read_req = self.get_nic_max_read_req(lspci_vv_output)
        tls = self.get_nic_target_link_speed(lspci_vv_output)
        ker_drv = self.get_nic_ker_drv_in_use(lspci_vv_output)

        sig_nic = Single_NIC_conf(lspci_vv_output = lspci_vv_output,
                                  code_name = code_name, rx_q_num = 0,
                                  tx_q_num = 0, numa_node = numa_node,
                                  LnkCap = LnkCap, LnkSta = LnkSta,
                                  cap_mpl = devcap_maxpayload, ctl_mpl = devctl_maxpayload,
                                  mrq = max_read_req, target_link_speed = tls,
                                  pci_addr = pci_addr, ker_drv = ker_drv)

        self.nics_conf.append(sig_nic)

    def init_all_nics_conf(self):
        for i in range(self.nic_total_num):
            self.init_single_nic_conf(i)
