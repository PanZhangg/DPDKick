import unittest
from utility import software as swutil
from utility import hardware as hwutil
from utility import utilities as util
from utility import env as env
import hwconftest as hwconf

"""
Testcases related to software configuration
and runtime env variables
"""

class swconftest(unittest.TestCase):

    cpu = env.g_env_conf.cpu_conf

    sw = env.g_env_conf.sw_conf

    """
    Verify software thread number is less than the
    number of total CPU cores
    """
    def test_thread_num_less_than_cpu_core_num(self):
        nr_cpu = self.cpu.cpu_core_total_num
        nr_thread = self.sw.thread_num
        self.assertLess(nr_thread, nr_cpu)

    """
    Verify if DPDK NICs and pinning CPU cores are at the same
    NUMA node
    """
    def test_CPU_NIC_on_same_NUMA_node(self):
        pass


if __name__ == '__main__':
    unittest.main()
