import utilities as util

class Kernel_conf():
    def __init__(self):
        self.iommu_conf = ''
        self.nmi_is_disabled = self.b_nmi_is_disabled()

    def b_nmi_is_disabled(self):
        ret = util.int_cmd_output('cat /proc/sys/kernel/nmi_watchdog')
        if ret == 0:
            return True
        else:
            return False
