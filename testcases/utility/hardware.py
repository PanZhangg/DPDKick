import os

"""
CPU related configurations
"""

class CPU_conf:
    def __init__(self):
        self.str_CPU_code_name = self.get_CPU_code_name()
        self.str_instruction_supported = self.get_CPU_instructions_supported()
        self.cpu_core_total_num = self.get_CPU_cores_total_num()
        self.b_HT_enabled = self.HT_is_enabled()
        #self.cores = list[]

    """
    CPU related utility functions
    """
    
    def get_CPU_code_name(self):
        pass
    
    def HT_is_enabled(self):
        pass
    
    def get_CPU_cores_total_num(self):
        pass
    
    def get_CPU_instructions_supported(self):
        pass
    
    
class CPU_core_conf:
    def __init__(self, core_num, numa_node):
        self.core_num = core_num
        self.numa_node = numa_node

"""
Memory related configurations
"""

class memory_conf:
    def __init__(self, total_num):
        self.memroy_total_num = total_num

"""
NIC related configurations
"""

class Single_NIC_conf:
    def __init__(self, code_name, rx_q_num, tx_q_num,
                 numa_node, LnkCap, LnkSta, pci_addr,
                 drv):

        self.nic_code_name = code_name
        self.rx_queue_num = rx_q_num
        self.tx_queue_num = tx_q_num
        self.NUMA_node = numa_node
        self.LnkCap = LnkCap
        self.LnkSta = LnkSta
        self.pci_address = pci_addr
        self.driver_in_use = drv


class Single_NIC_conf_82599(Single_NIC_conf):
    def __init__(self):
        super.__init__(self)
    
class NICs_conf:
    lspci_nic_cmd = 'lspci | grep Ether'

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
        
    def get_nic_LnkCap(self, list_num):
        pci_addr = self.get_nic_pci_address(list_num)
        command = 'lspci -s ' + pci_addr + ' -vv'
        output = os.popen(command, 'r').read()
        loc = output.rfind('LnkCap')
        str_tmp = output[loc :]
        loc = str_tmp.find('Speed')
        return str_tmp[loc + 6 : loc + 11]
    
    def get_nic_LnkSta(self, list_num):
        pci_addr = self.get_nic_pci_address(list_num)
        command = 'lspci -s ' + pci_addr + ' -vv'
        output = os.popen(command, 'r').read()
        loc = output.find('LnkSta')
        str_tmp = output[loc :]
        loc = str_tmp.find('Speed')
        return str_tmp[loc + 6 : loc + 11]

    def init_single_nic_conf(self):
        pass

    def init_all_nics_conf(self):
        pass
        
    def __init__(self):
        self.str_nic_pci_conf= self.print_nic_pci_conf()
        self.nic_total_num = self.get_nic_total_num()
        self.nics_info = dict()
    

"""
Huagepage related configurations
"""
class Huagepage_conf:
    """
    Huagepage related utility functions
    """
    def Huagepage_size(self):
        pass
    
    def Huagepage_num(self):
        pass

    def __init__(self, total_num, size):
        self.hugepage_total_num = total_num
        self.huagepage_size = size
        self.page_num_on_first_numa_node
        
"""
NUMA related configurations
"""
    
"""
NUMA related utility functions
"""

def CPU_cores_NUMA_distribution(self):
    pass

def memory_NUMA_distribution(self):
    pass

def NIC_NUMA_distribution(self):
    pass

def Hugepage_NUMA_distribution(self):
    pass

def NICs_using_DPDK_driver(self):
    pass


