import unittest
import os
from utility import hardware as hwutil

"""
Testcases related to hardware configuration
"""

class hwconftest(unittest.TestCase):

    NUMA_ENABLED_IN_BIOS = False

    nics = hwutil.NICs_conf()

    cpu = hwutil.CPU_conf()

    """
    Verify if NUMA is enabled by BIOS configuration
    """
    def test_NUMA_BIOS_enabled(self):
        command = 'grep -i numa /var/log/dmesg'
        numa_disable_string = 'No NUMA configuration found'

        output = os.popen(command, 'r')
        ret = output.read().find(numa_disable_string)
        self.assertEqual(ret, -1)

        if (ret == -1):
            NUMA_ENABLED_IN_BIOS = True
        #self.cpu.get_lscpu_specific_conf('CPU(s)')
        #print len(self.nics.nics_conf)
        print self.cpu.cpu_core_total_num
        

    """
    Verify DPDK nics' LnkCap and LnkSta are identical
    """
    def test_NIC_LnkCap_LnkSta_identical(self):
        for i in range(self.nics.nic_total_num):
            nic = self.nics.nics_conf[i]
            self.assertEqual(nic.LnkCap, nic.LnkSta)

    """
    Verify DPDK nics and pinning CPU cores are at the same
    NUMA node
    """
    def test_CPU_NIC_on_same_NUMA_node(self):
        pass


if __name__ == '__main__':
    unittest.main()
