#!/usr/bin/env python
import globalvar
import unittest
from testcases import hwconftest
from testcases import swconftest
from testcases import kernelconftest
from testcases.utility import utilities as util
import TestRunner

def dpdkick_init():
    util.format_print_launch_screen()

    if (globalvar.CONF_PID_IS_VALID == False):
        print "Fill the correct values in dpdkick.conf before launching DPDKick"
        print "program exit.."
        raise SystemExit

def dpdkick_main():

    dpdkick_init()

    if(globalvar.ENV_CONF_TYPE == "performance"):
        hw_conf_test_suite = unittest.TestLoader().loadTestsFromTestCase(hwconftest.hwconftest)
        sw_conf_test_suite = unittest.TestLoader().loadTestsFromTestCase(swconftest.swconftest)
        kernel_conf_test_suite = unittest.TestLoader().loadTestsFromTestCase(kernelconftest.kernelconftest)
    else:
        print "Invalid Configuration Type"
        print "program exit.."
        raise SystemExit

    runner = TestRunner.TestRunner()

    util.format_print_test_suite_title('Hardware Configuration Verification')
    runner.run(hw_conf_test_suite, description = 'Hardware')

    util.format_print_test_suite_title('Software Configuration and Runtime Verification')
    runner.run(sw_conf_test_suite, description = 'Software')

    util.format_print_test_suite_title('Kernel Configuration Verification')
    runner.run(kernel_conf_test_suite, description = 'Kernel')

if __name__ == '__main__':
    dpdkick_main()
