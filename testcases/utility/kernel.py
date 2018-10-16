import utilities as util

class Kernel_conf():
    def __init__(self):
        self.iommu_conf = ''
        self.nmi_is_disabled = self.b_nmi_is_disabled()
        self.wb_cpumask = self.get_writeback_cpumask()

    def get_grub_cmdline_conf(self):
        output = util.str_cmd_output('cat /etc/default/grub')
        lines = output.split('\n')
        for line in lines:
            if line.find('GRUB_CMDLINE_LINUX') != -1:
                break
        return line

    def get_specific_conf_from_grub_cmdline(self, cmdline, spec):
        confs = cmdline.split(' ')
        for conf in confs:
            if conf.find(spec) != -1:
                break
        value = conf.split('=')[1]
        return value

    def get_specifc_grub_conf(self, spec):
        cmdline = self.get_grub_cmdline_conf()
        return self.get_specific_conf_from_grub_cmdline(cmdline, spec)

    def b_nmi_is_disabled(self):
        ret = util.int_cmd_output('cat /proc/sys/kernel/nmi_watchdog')
        if ret == 0:
            return True
        else:
            return False

    def get_intel_iommu_conf(self):
        return self.get_specifc_grub_conf('intel_iommu');

    def get_isolcpus_conf(self):
        return self.get_specifc_grub_conf('isolcpus');

    def get_nohz_full_conf(self):
        return self.get_specifc_grub_conf('nohz_full');

    def get_writeback_cpumask(self):
        return util.str_cmd_output('cat /sys/bus/workqueue/devices/writeback/cpumask')
