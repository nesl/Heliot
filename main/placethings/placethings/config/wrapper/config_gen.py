from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from placethings.config.wrapper.device_gen import AllDeviceData
from placethings.config.wrapper.nw_device_gen import AllNwDeviceData
from placethings.config.wrapper.task_gen import AllTaskData

sandeep_debug = False


class Config(object):
    def __init__(self, folderpath=None):
        if not folderpath:
            self.all_device_data = AllDeviceData()
            self.all_nw_device_data = AllNwDeviceData()
            self.all_task_data = AllTaskData()
        else:
            self.all_device_data = AllDeviceData(
                filepath=self._gen_file_path(folderpath, 'device_data'))
            self.all_nw_device_data = AllNwDeviceData(
                filepath=self._gen_file_path(folderpath, 'nw_device_data'))
            self.all_task_data = AllTaskData(
                filepath=self._gen_file_path(folderpath, 'task_data'))

        if sandeep_debug:
            raw_input('Sandeep: Press enter to continue: ')
            print('Device Specs')
            print(self.all_device_data.device_spec.data)
            print('*'*100)
            print('*'*100)
            print('Device inventory')
            print(self.all_device_data.device_inventory.data)
            print('*'*100)
            print('*'*100)
            print('Device links')
            print(self.all_device_data.device_links.data)
            print('*'*100)
            print('*'*100)

            # Network Devices
            print('NW Device Specs')
            print(self.all_nw_device_data.nw_device_spec.data)
            print('*'*100)
            print('*'*100)
            print('NW Device inventory')
            print(self.all_nw_device_data.nw_device_inventory.data)
            print('*'*100)
            print('*'*100)
            print('NW Device links')
            print(self.all_nw_device_data.nw_device_links.data)
            print('*'*100)
            print('*'*100)

            print('Tasks Details')
            print(self.all_task_data.task_mapping.data)
            print('*'*100)
            print('*'*100)

            print(self.all_task_data.task_links.data)
            print('*'*100)
            print('*'*100)

            print(self.all_task_data.task_info.data)
            print('*'*100)
            print('*'*100)

    @staticmethod
    def _gen_file_path(folder_path, filename):
        return '{}/{}.json'.format(folder_path, filename)

    def export_data(self, folderpath):
        self.all_device_data.export_data(
            self._gen_file_path(folderpath, 'device_data'))
        self.all_nw_device_data.export_data(
            self._gen_file_path(folderpath, 'nw_device_data'))
        self.all_task_data.export_data(
            self._gen_file_path(folderpath, 'task_data'))

    def add_device(self, device_category, device, num):
        spec = self.all_device_data.device_spec.data
        assert device_category in spec
        assert device in spec[device_category]
        self.all_device_data.add_device(device_category, device, num)

    def add_nw_device(self, nw_device_category, nw_device, num):
        nw_spec = self.all_nw_device_data.nw_device_spec.data
        assert nw_device_category in nw_spec
        assert nw_device in nw_spec[nw_device_category]
        self.all_nw_device_data.add_nw_device(
            nw_device_category, nw_device, num)

    def add_dev_link(self, dev, nw_dev, latency):
        nw_dev_list = (
            self.all_nw_device_data.nw_device_inventory.get_device_list())
        self.all_device_data.add_dev_link(dev, nw_dev, latency, nw_dev_list)

    def add_nw_dev_link(self, src, dst, src_link_type, dst_link_type, latency):
        self.all_nw_device_data.add_nw_dev_link(
            src, dst, src_link_type, dst_link_type, latency)

    def add_task(self, task_name):
        self.all_task_data.add_task(task_name)

    def add_task_flavor(self, task_name, flavor_obj):
        """
        args:
            task_name (str)
            flavor_obj (TaskFlavor)
        """
        self.all_task_data.add_flavor(task_name, flavor_obj)

    def add_task_link(self, src, dst, traffic):
        self.all_task_data.add_link(src, dst, traffic)

    def add_task_mapping(self, task, device):
        device_list = self.all_device_data.device_inventory.get_device_list()
        self.all_task_data.add_mapping(task, device, device_list)
