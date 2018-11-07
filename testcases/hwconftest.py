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
    mem = env.g_env_conf.mem_conf

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
        util.testcase_append_suggestions(self._testMethodName,
        "DISABLE this feature in BIOS")
        self.assertEqual(self.cpu.b_hyperthread_enabled, False)

    """
    Verify if CPU C3 power state is disabled
    """
    def test_CPU_C3state_disabled(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Add \'intel_idle.max_cstate=0\' to grub")
        self.assertEqual(self.cpu.b_c3state_disabled, True)

    """
    Verify if CPU C6 power state is disabled
    """
    def test_CPU_C6state_disabled(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Add \'intel_idle.max_cstate=0\' to grub")
        self.assertEqual(self.cpu.b_c6state_disabled, True)

    """
    Verify if CPU scaling governor is performance
    """
    def test_CPU_sg_is_perf(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Set \'performance\' to /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
        ret = True
        if self.cpu.scaling_governor == None:
            #Fail this testcase
            self.assertEqual(True, False)
        for l in self.cpu.scaling_governor:
            if l != 'performance':
                ret = False
                break
        self.assertEqual(ret, True)

    """
    Verify if DCU data prefetcher is enabled
    """
    @unittest.skipIf(globalvar.MSR_TOOLS_IS_INSTALLED == False, "msr-tools not installed")
    def test_CPU_DCU_enabled(self):
        util.testcase_append_suggestions(self._testMethodName,
        "ENABLE this feature in BIOS")
        output = util.str_cmd_output('rdmsr 0x1A4')
        v = int(output, 16)
        self.assertEqual((v & (1 << 2)), 0)

    """
    Verify if Direct Cache Access is enabled
    """
    def test_DCA_enabled(self):
        util.testcase_append_suggestions(self._testMethodName,
        "ENABLE this feature in BIOS")
        self.assertEqual(self.cpu.b_direct_cache_access_enabled, True)

    """
    Verify if Turbo Boost is disabled
    """
    def test_turbo_boost_disabled(self):
        util.testcase_append_suggestions(self._testMethodName,
        "DISABLE this feature in BIOS")
        self.assertEqual(self.cpu.b_turbo_disabled, True)

    """
    Verify if intel pstate is disabled
    """
    def test_intel_pstate_disabled(self):
        util.testcase_append_suggestions(self._testMethodName,
        "DISABLE this feature in BIOS")
        self.assertEqual(self.cpu.b_pstate_disabled, True)

    """
    Verify DPDK nics' PCIe Speed is 8GT/s in LnkCap
    """
    def test_NIC_LnkCap_speed_8GT(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Install NIC in a Width x8 Gen3 PCIe slot")
        detected = []
        result = True
        for i in range(self.nics.nic_total_num):
            nic = self.nics.nics_conf[i]
            if nic.LnkCap != "8GT/s":
                detected.append(nic.pci_address)
                result = False
        if result == False:
            util.format_print_detected_dev_list(detected)
        self.assertEqual(result, True)

    """
    Verify DPDK nics' PCIe Speed and target link speed are
    identical
    """
    def test_NIC_PCIe_target_link_speed(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Configure target link speed equal to PCIe speed")
        detected = []
        result = True
        for i in range(self.nics.nic_total_num):
            nic = self.nics.nics_conf[i]
            if nic.pcie_targetlinkspeed == None:
                continue
            if nic.pcie_targetlinkspeed != nic.LnkCap:
                detected.append(nic.pci_address)
                result = False
        if result == False:
            util.format_print_detected_dev_list(detected)
        self.assertEqual(result, True)

    """
    Verify DPDK nics' DevCap Maxpayload and DevCtl Maxpayload are
    identical
    """
    def test_NIC_devcap_devctl_maxpayload(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Set the maxpayload to identical number")
        detected = []
        result = True
        for i in range(self.nics.nic_total_num):
            nic = self.nics.nics_conf[i]
            if nic.pcie_devcap_maxpayloadsize != nic.pcie_devctl_maxpayloadsize:
                detected.append(nic.pci_address)
                result = False
        if result == False:
            util.format_print_detected_dev_list(detected)
        self.assertEqual(result, True)

    """
    Verify DPDK nics' LnkCap and LnkSta are identical
    """
    def test_NIC_LnkCap_LnkSta_identical(self):
        for i in range(self.nics.nic_total_num):
            nic = self.nics.nics_conf[i]
            self.assertEqual(nic.LnkCap, nic.LnkSta)

    """
    Verify Memory speed is equal to DDR4 frequency(2133 MHz)
    """
    @unittest.skipIf(globalvar.NORMAL_PHY_HOST_MEM == False, "Not running in a normal physical env")
    def test_mem_speed_ddr4(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Recommanded to use DDR4 memory")
        for i in self.mem.dimms:
            if i.memory_speed != "Unknown":
                self.assertEqual(i.memory_speed, "2133 MHz")

    """
    Verify Memory speed is equal to Memory configured speed
    """
    @unittest.skipIf(globalvar.NORMAL_PHY_HOST_MEM == False, "Not running in a normal physical env")
    def test_mem_speed_equal_conf_speed(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Configure speed should be equal to memory speed")
        for i in self.mem.dimms:
            if i.memory_speed != "Unknown":
                self.assertEqual(i.memory_speed, i.memory_config_speed)

    """
    Verify each memory DIMM has at least 4GB memory
    """
    @unittest.skipIf(globalvar.NORMAL_PHY_HOST_MEM == False, "Not running in a normal physical env")
    def test_mem_dimm_larger_4GB(self):
        util.testcase_append_suggestions(self._testMethodName,
        "It's recommaned to have more than 4GB each dimm slot")
        for i in self.mem.dimms:
            if i.memory_size != "No Module Installed":
                dimm_size = int(i.memory_size[:-2])
                self.assertGreaterEqual(dimm_size, 4096)

    """
    Verify each memory DIMM has identical memory size
    """
    @unittest.skipIf(globalvar.NORMAL_PHY_HOST_MEM == False, "Not running in a normal physical env")
    def test_mem_dimm_identical_size(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Memory size of each DIMM should be identical")
        for i in self.mem.dimms:
            dimm_size = int(self.mem.dimms[0].memory_size[:-2])
            if i.memory_size != "No Module Installed":
                dimm_size_t = int(i.memory_size[:-2])
                self.assertGreaterEqual(dimm_size, dimm_size_t)

    """
    Verify each memory channel has identical memory size
    """
    @unittest.skipIf(globalvar.NORMAL_PHY_HOST_MEM == False, "Not running in a normal physical env")
    def test_mem_channel_identical_size(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Memory size of each channel should be identical")
        for i in range(self.mem.memory_channels_num):
            channel_size = 0
            for j in range(self.mem.memory_DIMM_per_channel):
                if self.mem.dimms[i * self.mem.memory_DIMM_per_channel + j].memory_size != "No Module Installed":
                    channel_size += int(self.mem.dimms[j].memory_size[:-2])
            if i == 0:
                first_channel_size = channel_size
            else:
                self.assertEqual(first_channel_size, channel_size)

    """
    Verify installed DIMM slot location(s) are indentical of each channel
    """
    @unittest.skipIf(globalvar.NORMAL_PHY_HOST_MEM == False, "Not running in a normal physical env")
    def test_mem_channel_identical_locations(self):
        util.testcase_append_suggestions(self._testMethodName,
        "Install memory at identical slot location(s) each channel")
        for i in range(self.mem.memory_channels_num):
            locations = []
            for j in range(self.mem.memory_DIMM_per_channel):
                if self.mem.dimms[i * self.mem.memory_DIMM_per_channel + j].memory_size != "No Module Installed":
                    locations.append(1)
                else:
                    locations.append(0)
            if i == 0:
                first_channel_locations = locations
            else:
                self.assertEqual(first_channel_locations, locations)
