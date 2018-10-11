import os

"""
Utilities for OS command interaction
"""

def str_cmd_output(cmd):
    output = os.popen(cmd, 'r').read()
    return output

def int_cmd_output(cmd):
    output = self.str_cmd_output(cmd)
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
