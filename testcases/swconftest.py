import unittest
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
    nics = env.g_env_conf.nics_conf

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
        cpu_ids = self.sw.get_cpu_list_by_mask()
        numa_node_list = []
        for cpu_id in cpu_ids:
            cpu = self.cpu.get_single_CPU_conf_by_id(cpu_id)
            numa_node = cpu.numa_node
            numa_node_list.append(numa_node)
        for nic in self.nics.nics_conf:
            numa_node = nic.NUMA_node
            numa_node_list.append(numa_node)

        prev_numa_node = numa_node_list[0]
        for node in numa_node_list:
            self.assertEqual(prev_numa_node, node)
            prev_numa_node = node

if __name__ == '__main__':
    unittest.main()
