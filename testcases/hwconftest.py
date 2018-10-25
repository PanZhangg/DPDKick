import unittest
import os
from utility import utilities as util
from utility import env as env
import globalvar

"""
Testcases related to hardware configuration
"""
class hwconftest(unittest.TestCase):
    NUMA_ENABLED_IN_BIOS = False
    nics = env.g_env_conf.nics_conf
    cpu = env.g_env_conf.cpu_conf

    """
    Verify if NUMA is enabled
    """
    def test_NUMA_BIOS_enabled(self):
        command = 'grep -i numa /var/log/dmesg'
        numa_disable_string = 'No NUMA configuration found'

        ret = util.check_if_cmd_output_contains(command, numa_disable_string)

        if ret == False:
            self.NUMA_ENABLED_IN_BIOS = True
        self.assertEqual(ret, False)

    """
    Verify if Hyper Thread is disabled
    """
    def test_hyper_thread_disabled(self):
        self.assertEqual(self.cpu.b_hyperthread_enabled, False)

    """
    Verify if CPU C3 power state is disabled
    """
    def test_CPU_C3state_disabled(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Add \'max_cstate=0\' to grub")
        self.assertEqual(self.cpu.b_c3state_disabled, True)

    """
    Verify if CPU C6 power state is disabled
    """
    def test_CPU_C6state_disabled(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Add \'max_cstate=0\' to grub")
        self.assertEqual(self.cpu.b_c6state_disabled, True)

    """
    Verify if DCU data prefetcher is enabled
    """
    @unittest.skipIf(globalvar.MSR_TOOLS_IS_INSTALLED == False, "msr-tools not installed")
    def test_CPU_DCU_data_prefetcher_enabled(self):
        util.testcase_append_suggestions(self._testMethodName,
        "ENABLE this feature in BIOS")
        output = util.str_cmd_output('rdmsr 0x1A4')
        v = int(output, 16)
        self.assertEqual((v & (1 << 2)), 0)

    """
    Verify if Direct Cache Access is enabled
    """
    def test_direct_cache_access_enabled(self):
        self.assertEqual(self.cpu.b_direct_cache_access_enabled, True)

    """
    Verify if Turbo Boost is disabled
    """
    def test_turbo_boost_disabled(self):
        self.assertEqual(self.cpu.b_turbo_disabled, True)

    """
    Verify if intel pstate is disabled
    """
    def test_intel_pstate_disabled(self):
        self.assertEqual(self.cpu.b_pstate_disabled, True)

    """
    Verify DPDK nics' LnkCap and LnkSta are identical
    """
    def test_NIC_LnkCap_LnkSta_identical(self):
        for i in range(self.nics.nic_total_num):
            nic = self.nics.nics_conf[i]
            self.assertEqual(nic.LnkCap, nic.LnkSta)

if __name__ == '__main__':
    unittest.main()
