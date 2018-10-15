import unittest
import os
from utility import hardware as hwutil
from utility import utilities as util
from utility import env as env

"""
Testcases related to hardware configuration
"""
class hwconftest(unittest.TestCase):

    NUMA_ENABLED_IN_BIOS = False

    nics = env.g_env_conf.nics_conf

    cpu = env.g_env_conf.cpu_conf

    """
    Verify if NUMA is enabled by BIOS configuration
    """
    def test_NUMA_BIOS_enabled(self):
        command = 'grep -i numa /var/log/dmesg'
        numa_disable_string = 'No NUMA configuration found'

        ret = util.check_if_cmd_output_contains(command, numa_disable_string)

        if ret == False:
            self.NUMA_ENABLED_IN_BIOS = True
        self.assertEqual(ret, False)

    """
    Verify DPDK nics' LnkCap and LnkSta are identical
    """
    def test_NIC_LnkCap_LnkSta_identical(self):
        for i in range(self.nics.nic_total_num):
            nic = self.nics.nics_conf[i]
            self.assertEqual(nic.LnkCap, nic.LnkSta)

if __name__ == '__main__':
    unittest.main()
