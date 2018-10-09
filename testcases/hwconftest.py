import unittest
import os

class hwconftest(unittest.TestCase):

    NUMA_ENABLED_IN_BIOS = False

    def test_NUMA_BIOS_ENABLED(self):
        command = 'grep -i numa /var/log/dmesg'
        no_numa_string = 'No NUMA configuration found'

        output = os.popen(command, 'r')
        ret = output.read().find(no_numa_string)
        self.assertEqual(ret, -1)

        if (ret == -1):
            NUMA_ENABLED_IN_BIOS = True

if __name__ == '__main__':
    unittest.main()
