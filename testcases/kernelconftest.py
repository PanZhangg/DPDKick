import unittest
from utility import kernel as kernelutil
from utility import utilities as util
from utility import env as env

class kernelconftest(unittest.TestCase):
    cpu = env.g_env_conf.cpu_conf
    sw = env.g_env_conf.sw_conf
    kernel = env.g_env_conf.kernel

    """
    Verify if NMI is disabled
    """
    def test_nmi_is_disable(self):
        print self.kernel.__dict__
        self.assertEqual(self.kernel.nmi_is_disabled, True)

    """
    Verify if intel_pstat is disabled
    """
    def test_pstat_is_disabled(self):
        pass

    """
    Verify hugepage size is 1G
    """
    def test_hugepage_size_1G(self):
        pass

    """
    Verify if masked CPU cores(indicated in dpdk.conf
    file) are included in isolcpus configuration list
    """
    def test_masked_cpu_included_in_ioslcpus(self):
        masked_cpus = self.sw.get_cpu_list_by_mask(self.cpu.cpu_core_total_num)
        included = True
        for i in masked_cpus:
            if i in self.kernel.isolcpus:
                continue
            else:
                included = False
                break

        self.assertEqual(included, True)

    """
    Verify if masked CPU cores(indicated in dpdk.conf
    file) are included in nohz_full configuration list
    """
    def test_masked_cpu_included_in_nohz_full(self):
        masked_cpus = self.sw.get_cpu_list_by_mask(self.cpu.cpu_core_total_num)
        included = True
        for i in masked_cpus:
            if i in self.kernel.nohz_full :
                continue
            else:
                included = False
                break

        self.assertEqual(included, True)

    """
    Verify if masked CPU cores(indicated in dpdk.conf
    file) are included in rcu_nocbs configuration list
    """
    def test_masked_cpu_included_in_rcu_nocbs(self):
        masked_cpus = self.sw.get_cpu_list_by_mask(self.cpu.cpu_core_total_num)
        included = True
        for i in masked_cpus:
            if i in self.kernel.rcu_nocbs:
                continue
            else:
                included = False
                break

        self.assertEqual(included, True)

    """
    Verify if masked CPU cores(indicated in dpdk.conf
    file) are excluded in kthread configuration list
    """
    def test_masked_cpu_excluded_in_kthread(self):
        masked_cpus = self.sw.get_cpu_list_by_mask(self.cpu.cpu_core_total_num)
        excluded = True
        for i in masked_cpus:
            if i in self.kernel.kthread_cpus :
                excluded = False
                break

        self.assertEqual(excluded, True)

    """
    Verify if masked CPU cores(indicated in dpdk.conf
    file) are excluded in irqaffinity configuration list
    """
    def test_masked_cpu_excluded_in_irqaffinity(self):
        masked_cpus = self.sw.get_cpu_list_by_mask(self.cpu.cpu_core_total_num)
        excluded = True
        for i in masked_cpus:
            if i in self.kernel.irqaffinity :
                excluded = False
                break

        self.assertEqual(excluded, True)

if __name__ == '__main__':
    unittest.main()
