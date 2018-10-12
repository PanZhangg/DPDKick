import utilities as util

class Kernel_conf():
    def __init__(self):
        self.iommu_conf = ''
        self.nmi_is_disabled = self.b_nmi_is_disabled()
        self.wb_cpumask = self.get_writeback_cpumask()

    def b_nmi_is_disabled(self):
        ret = util.int_cmd_output('cat /proc/sys/kernel/nmi_watchdog')
        if ret == 0:
            return True
        else:
            return False

    def get_iommu_conf(self):
        pass

    def get_writeback_cpumask(self):
       return util.str_cmd_output('cat /sys/bus/workqueue/devices/writeback/cpumask')
