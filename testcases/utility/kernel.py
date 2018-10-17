import utilities as util

class Kernel_conf():
    def __init__(self):
        self.iommu_conf = ''
        self.nmi_is_disabled = self.b_nmi_is_disabled()
        self.wb_cpumask = self.get_writeback_cpumask()
        self.nohz_full = self.get_nohz_full_conf()
        self.isolcpus = self.get_isolcpus_conf()
        self.kthread_cpus = self.get_kthread_cpus()
        self.irqaffinity = self.get_irqaffinity()
        self.rcu_nocbs = self.get_rcu_nocbs()

    def __get_grub_cmdline_conf(self):
        output = util.str_cmd_output('cat /etc/default/grub')
        lines = output.split('\n')
        for line in lines:
            if line.find('GRUB_CMDLINE_LINUX') != -1:
                break
        return line

    def __get_specific_conf_from_grub_cmdline(self, cmdline, spec):
        confs = cmdline.split(' ')
        for conf in confs:
            if conf.find(spec) != -1:
                break
        value = conf.split('=')[1]
        return value

    def __get_specific_grub_conf(self, spec):
        cmdline = self.__get_grub_cmdline_conf()
        return self.__get_specific_conf_from_grub_cmdline(cmdline, spec)

    def b_nmi_is_disabled(self):
        ret = util.int_cmd_output('cat /proc/sys/kernel/nmi_watchdog')
        if ret == 0:
            return True
        else:
            return False

    def get_intel_iommu_conf(self):
        return self.__get_specific_grub_conf('intel_iommu');

    def get_isolcpus_conf(self):
        l = self.__get_specific_grub_conf('isolcpus');
        return util.convert_multipule_str_range_to_int_list(l)

    def get_nohz_full_conf(self):
        l = self.__get_specific_grub_conf('nohz_full');
        return util.convert_multipule_str_range_to_int_list(l)

    def get_kthread_cpus(self):
        l = self.__get_specific_grub_conf('kthread_cpus');
        return util.convert_multipule_str_range_to_int_list(l)

    def get_irqaffinity(self):
        l = self.__get_specific_grub_conf('irqaffinity');
        return util.convert_multipule_str_range_to_int_list(l)

    def get_rcu_nocbs(self):
        l = self.__get_specific_grub_conf('rcu_nocbs');
        return util.convert_multipule_str_range_to_int_list(l)

    def get_writeback_cpumask(self):
        return util.str_cmd_output('cat /sys/bus/workqueue/devices/writeback/cpumask')
