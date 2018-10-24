import unittest
import os
from utility import utilities as util
from utility import env as env

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
        pass

    """
    Verify if CPU C6 power state is disabled
    """
    def test_CPU_C6state_disabled(self):
        pass

    """
    Verify if MLC streamer is enabled
    """
    def test_CPU_MLC_streamer_enabled(self):
        pass

    """
    Verify if MLC spacial prefetcher is enabled
    """
    def test_CPU_MLC_spacial_prefetcher_enabled(self):
        pass

    """
    Verify if DCU data prefetcher is enabled
    """
    def test_CPU_DCU_data_prefetcher_enabled(self):
        pass

    """
    Verify if Direct Cache Access is enabled
    """
    def test_direct_cache_access_enabled(self):
        pass

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
