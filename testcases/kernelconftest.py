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
        self.assertEqual(self.kernel.nmi_is_disabled, True)
        print self.kernel.get_nohz_full_conf()

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

if __name__ == '__main__':
    unittest.main()
