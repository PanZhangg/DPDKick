import os

class CPU_conf:
    def __init__(self):
        self.CPU_code_name = ''
        self.cpu_core_total_num = 0
        self.memroy_total_num = 0

class Single_NIC_conf:
    def __init__(self):
        self.nic_code_name = ''
        self.rx_queue_num = 0
        self.tx_queue_num = 0
        self.NUMA_node = 0
        self.LnkCap = 0
        self.LnkSta = 0
        self.pci_address = ''

    """
    NIC related utility functions
    """
    def NIC_rx_queue_num(self):
        pass
    
    def NIC_tx_queue_num(self):
        pass

class Single_NIC_conf_82599(Single_NIC_conf):
    def __init__(self):
        super.__init__(self)
    
class NICs_conf:
    lspci_nic_cmd = 'lspci | grep Ether'

    def read_nic_pci_conf(self):
        output = os.popen(self.lspci_nic_cmd, 'r')
        return output.read()

    def nic_total_num(self):
        command = self.lspci_nic_cmd + '|wc -l'
        output = os.popen(command, 'r')
        return int(output.read())

    def nic_pci_address(self, list_num):
        output = self.nic_pci_conf.splitlines()[list_num]
        return output[0:7]

    def nic_code_name(self, list_num):
        output = self.nic_pci_conf.splitlines()[list_num].split(':')[2]
        return output
        
    def nic_LnkCap(self, list_num):
        pci_addr = nic_pci_address(list_num)
        command = 'lspci -s ' + pci_addr + ' -vv'
        output = os.popen(command, 'r')
        loc = output.read().find('LnkCap')
    
    def nic_LnkSta(self, list_num):
        pci_addr = nic_pci_address(list_num)
        command = 'lspci -s ' + pci_addr + ' -vv'
        output = os.popen(command, 'r')
        loc = output.read().find('LnkSta')
        
    def __init__(self):
        self.nic_pci_conf = self.read_nic_pci_conf()
        self.nic_total_num = self.nic_total_num()
        self.nics_info = dict()
    

class Huagepage_conf:
    """
    Huagepage related utility functions
    """
    def Huagepage_size(self):
        pass
    
    def Huagepage_num(self):
        pass

    def __init__(self):
        self.hugepage_total_num = 0
        self.huagepage_size = 0
    
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


"""
CPU related utility functions
"""

def CPU_code_name(self):
    pass

def HT_enabled(self):
    pass

def CPU_cores_total_num(self):
    pass

def CPU_SSSE_Instructions_supported(self):
    pass

