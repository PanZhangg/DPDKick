#!/usr/bin/env python
import unittest
import TestRunner
from testcases import hwconftest
from testcases import swconftest
from testcases import kernelconftest
from testcases.utility import utilities as util
import globalvar

def dpdkick_main():
    util.format_print_launch_screen()
    conf_ok = util.check_conf_file_is_completed()
    if (conf_ok == False):
        print 'Fill the correct values in dpdkick.conf before launching DPDKick'
        print 'program exit..'
        raise SystemExit

    hw_conf_test_suite = unittest.TestLoader().loadTestsFromTestCase(hwconftest.hwconftest)
    sw_conf_test_suite = unittest.TestLoader().loadTestsFromTestCase(swconftest.swconftest)
    kernel_conf_test_suite = unittest.TestLoader().loadTestsFromTestCase(kernelconftest.kernelconftest)

    runner = TestRunner.TestRunner()

    util.format_print_test_suite_title('Hardware Configuration Verification')
    runner.run(hw_conf_test_suite, description = 'Hardware')

    util.format_print_test_suite_title('Software Configuration and Runtime Verification')
    runner.run(sw_conf_test_suite, description = 'Software')

    util.format_print_test_suite_title('Kernel Configuration Verification')
    runner.run(kernel_conf_test_suite, description = 'Kernel')

if __name__ == '__main__':
    dpdkick_main()
