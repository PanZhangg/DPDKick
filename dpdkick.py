import unittest
from testcases import hwconftest
from testcases import kernelconftest
from testcases.utility import utilities as util

def dpdkick_main():
    util.format_print_launch_screen()

    hw_conf_test_suite = unittest.TestLoader().loadTestsFromTestCase(hwconftest.hwconftest)
    kernel_conf_test_suite = unittest.TestLoader().loadTestsFromTestCase(kernelconftest.kernelconftest)

    util.format_print_test_suite_title('Hardware Configuration Verfication')
    unittest.TextTestRunner(verbosity=2).run(hw_conf_test_suite)

    util.format_print_test_suite_title('Kernel Configuration Verfication')
    unittest.TextTestRunner(verbosity=2).run(kernel_conf_test_suite)

if __name__ == '__main__':
    dpdkick_main()
