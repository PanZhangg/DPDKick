import utilities as util


"""
Kernel related configurations
"""
class Kernel_conf():
    def __init__(self):
        self.iommu_conf = ''
        self.nmi_is_disabled = self.b_nmi_is_disabled()
        self.wb_cpumask = self.get_writeback_cpumask()
        self.nohz_full = self.__get_nohz_full_conf()
        self.isolcpus = self.__get_isolcpus_conf()
        self.kthread_cpus = self.__get_kthread_cpus()
        self.irqaffinity = self.__get_irqaffinity()
        self.rcu_nocbs = self.__get_rcu_nocbs()
        self.intel_iommu = self.__get_intel_iommu()
        self.iommu_pt = self.__get_iommu_pt()

    """
    Kernel related utility functions
    """
    def __get_grub_cmdline_conf(self):
        output = util.str_cmd_output('cat /etc/default/grub')
        lines = output.split('\n')
        for line in lines:
            if line.find('GRUB_CMDLINE_LINUX') != -1:
                break
        return line

    def __get_specific_conf_from_grub_cmdline(self, cmdline, spec):
        confs = cmdline.split(' ')
        found = False
        for conf in confs:
            if conf.find(spec) != -1:
                found = True
                break
        if found == False:
            return ''
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

    def __get_isolcpus_conf(self):
        l = self.__get_specific_grub_conf('isolcpus');
        return util.convert_multipule_str_range_to_int_list(l)

    def __get_nohz_full_conf(self):
        l = self.__get_specific_grub_conf('nohz_full');
        return util.convert_multipule_str_range_to_int_list(l)

    def __get_kthread_cpus(self):
        l = self.__get_specific_grub_conf('kthread_cpus');
        return util.convert_multipule_str_range_to_int_list(l)

    def __get_irqaffinity(self):
        l = self.__get_specific_grub_conf('irqaffinity');
        return util.convert_multipule_str_range_to_int_list(l)

    def __get_rcu_nocbs(self):
        l = self.__get_specific_grub_conf('rcu_nocbs');
        return util.convert_multipule_str_range_to_int_list(l)

    def __get_intel_iommu(self):
        l = self.__get_specific_grub_conf('intel_iommu');
        if l != '':
            return l[:2]
        else:
            return ''

    def __get_iommu_pt(self):
        l = self.__get_specific_grub_conf('iommu');
        if l is not None:
            return True
        else:
            return False

    def get_writeback_cpumask(self):
        return util.str_cmd_output('cat /sys/bus/workqueue/devices/writeback/cpumask')


"""
Huagepage related configurations
"""
class Huagepage_conf:

    def __init__(self):
        self.hugepage_total_num = self.__get_hugepage_total_num()
        self.hugepage_free_num = self.__get_huagepage_free_num()
        self.hugepage_mem_size = self.__get_hugepage_mem_size()
        self.transparent_hp_enabled = self.__get_thp_enabled()

    """
    Huagepage related utility functions
    """
    def __get_huagepage_free_num(self):
        command = 'cat /proc/meminfo'
        n = util.str_get_specific_value_after_colon(command, 'HugePages_Free')
        return int(n)

    def __get_hugepage_mem_size(self):
        command = 'cat /proc/meminfo'
        size = util.str_get_specific_value_after_colon(command, 'Hugepagesize')
        return size

    def __get_hugepage_total_num(self):
        command = 'cat /proc/meminfo'
        n = util.str_get_specific_value_after_colon(command, 'HugePages_Total')
        return int(n)

    def __get_thp_enabled(self):
        path = '/sys/kernel/mm/transparent_hugepage/enabled'
        output = util.get_cat_command_output(path)
        if output == None:
            return None
        loc = output.find('[')
        #[never]
        if output[loc + 1] == 'n':
            return False
        else:
            return True
