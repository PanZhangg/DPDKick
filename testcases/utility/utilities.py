import os

"""
Utilities for OS command interaction
"""

def str_cmd_output(cmd):
    output = os.popen(cmd, 'r').read()
    return output

def int_cmd_output(cmd):
    output = str_cmd_output(cmd)
    return int(output)

def check_if_cmd_output_contains(cmd, str_to_check):
    output = str_cmd_output(cmd)
    ret = output.find(str_to_check)
    if ret == -1:
        return False
    else:
        return True

def str_get_specific_value_after_colon(cmd, spec):
    output = str_cmd_output(cmd)
    l = output.split('\n')
    for i in range(len(l)):
        if (l[i].find(spec) != -1):
            break;
    ll = l[i].split(':')[1]
    return ll.strip()

"""
Utilities for formatted printing
"""

def format_print_launch_screen():
    print '|#######################################|'
    print '|    ____  ____  ____  __ __ _      __  |'
    print '|   / __ \/ __ \/ __ \/ //_/(_)____/ /__|'
    print '|  / / / / /_/ / / / / ,<  / / ___/ //_/|'
    print '| / /_/ / ____/ /_/ / /| |/ / /__/ ,<   |'
    print '|/_____/_/   /_____/_/ |_/_/\___/_/|_|  |'
    print '|                                       |'
    print '| ULTIMATE DPDK SYSTEM ENABLING EXPERT  |'
    print '|#######################################|'
    print ''

def format_print_test_suite_title(title):
    print '========================================='
    print title
    print '========================================='

"""
Utilities for reading conf file
"""
def check_conf_file_is_completed():
    return True

def get_specific_conf_from_conf_file(conf):
    f = open('./dpdkick.conf', 'r')
    lines = f.read().split('\n')
    for l in lines:
        if l.find(conf) != -1:
            break
    if l == '':
        print '[Error]: No such configuration'
    print l
    spec = l.split('=')[1]
    f.close()
    return spec
    
def get_dpdk_app_pid():
    pid = int(get_specific_conf_from_conf_file('dpdk-app-pid'))
    return pid

def get_cpu_mask():
    mask = get_specific_conf_from_conf_file('dpdk-app-cpu-mask')
    return mask
