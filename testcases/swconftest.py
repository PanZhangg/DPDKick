import unittest
from utility import software as swutil
from utility import utilities as util

"""
Testcases related to software configuration
and runtime env variables
"""

class swconftest(unittest.TestCase):

    """
    Verify if DPDK NICs and pinning CPU cores are at the same
    NUMA node
    """
    def test_CPU_NIC_on_same_NUMA_node(self):
        pass


if __name__ == '__main__':
    unittest.main()
