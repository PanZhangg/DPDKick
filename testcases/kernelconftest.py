import unittest
from utility import kernel as kernelutil
from utility import utilities as util
from utility import env as env

class kernelconftest(unittest.TestCase):
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
        pass

    """
    Verify if masked CPU cores(indicated in dpdk.conf
    file) are included in nohz_full configuration list
    """
    def test_masked_cpu_included_in_nohz_full(self):
        pass

    """
    Verify if masked CPU cores(indicated in dpdk.conf
    file) are excluded in kthread configuration list
    """
    def test_masked_cpu_excluded_in_kthread(self):
        pass

    """
    Verify if masked CPU cores(indicated in dpdk.conf
    file) are excluded in irqaffinity configuration list
    """
    def test_masked_cpu_excluded_in_irqaffinity(self):
        pass

if __name__ == '__main__':
    unittest.main()
