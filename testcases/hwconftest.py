import unittest
import os
from utility import hardware as hwutil

"""
Testcases related to hardware configuration
"""

class hwconftest(unittest.TestCase):

    NUMA_ENABLED_IN_BIOS = False

    def test_NUMA_BIOS_ENABLED(self):
        command = 'grep -i numa /var/log/dmesg'
        numa_disable_string = 'No NUMA configuration found'

        output = os.popen(command, 'r')
        ret = output.read().find(numa_disable_string)
        self.assertEqual(ret, -1)

        if (ret == -1):
            NUMA_ENABLED_IN_BIOS = True

    def test_CPU_NIC_on_same_NUMA_node(self):
        pass

if __name__ == '__main__':
    unittest.main()
