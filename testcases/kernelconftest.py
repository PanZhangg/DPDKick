import unittest
from utility import kernel as kernelutil
from utility import utilities as util

class kernelconftest(unittest.TestCase):
    kernel = kernelutil.Kernel_conf()

    """
    Verify if NMI is disabled
    """
    def test_nmi_is_disable(self):
        self.assertEqual(self.kernel.nmi_is_disabled , True)

    """
    Verify if intel_pstat is disabled
    """
    def test_pstat_is_disabled(self):
        pass

if __name__ == '__main__':
    unittest.main()
