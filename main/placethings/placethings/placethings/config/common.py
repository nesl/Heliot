from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import range
from future.utils import iteritems
import logging


log = logging.getLogger()


class Validator(object):
    @staticmethod
    def validate_inventory(device_spec, device_inventory):
        for device_cat, device_dict in iteritems(device_inventory):
            if device_cat not in device_spec:
                log.error('{} not in {}'.format(device_cat, set(device_spec)))
                return False
            device_set = set(device_spec[device_cat])
            for device in device_dict:
                if device not in device_set:
                    log.error('{} not in {}'.format(device, device_set))
                    return False
        return True

    @staticmethod
    def validate_mapping(task_set, device_inventory, mapping):
        inventory = InventoryManager(device_inventory)
        device_set = inventory.get_device_set()
        for task, device in iteritems(mapping):
            if task not in task_set:
                log.error('{} not in {}'.format(task, set(task_set)))
                return False
            if device not in device_set:
                log.error('{} not in {}'.format(device, set(device_set)))
                return False
        return True


class LinkHelper(object):
    _LINK_SYMBOL = ' -> '

    @classmethod
    def get_edge(cls, src, dst):
        """
        Args:
            src (str)
            dst (str)
        Returns:
            link_str (str): 'src -> dst'
        """
        return '{}{}{}'.format(src, cls._LINK_SYMBOL, dst)

    @classmethod
    def get_nodes(cls, link_str):
        """
        Args:
            link_str (str): 'src -> dst'
        Returns:
            src (str)
            dst (str)
        """
        src, dst = link_str.split(cls._LINK_SYMBOL)
        return src, dst


class InventoryManager(object):

    def __init__(self, inventory, spec=None):
        record, device_map = self._init_inventory_record(inventory)
        self._inventory = inventory
        self._record = record
        self._device_map = device_map
        if spec is None:
            spec = dict({})
        self._spec = spec

    def get_device_set(self):
        """
        Returns:
            all_devices (set of str): names of all devices
        """
        return set(self._device_map)

    def get_device_record(self):
        """
        Returns:
            device record (dict): categorized device names
        """
        return self._record

    @staticmethod
    def _gen_device_name(device_type, device_id):
        return '{}.{}'.format(device_type.name, device_id)

    @classmethod
    def _init_inventory_record(cls, inventory):
        """
        Args:
            inventory (dict)
        Returns:
            Record (dict)
            device_map (dict): {device_name: (device_cat, device_type)}
        """
        record = {}
        device_map = {}
        for device_cat, device_dict in iteritems(inventory):
            record[device_cat] = {}
            for device_type, n_device in iteritems(device_dict):
                record[device_cat][device_type] = []
                for device_id in range(n_device):
                    device_name = cls._gen_device_name(device_type, device_id)
                    record[device_cat][device_type].append(device_name)
                    assert device_name not in device_map
                    device_map[device_name] = (device_cat, device_type)
        return record, device_map

    def reset_inventory_record(self):
        self._record, self._all_devices = (
            self._init_inventory_record(self.inventory))

    def pop(self, device_cat, device_type):
        device_list = self._record[device_cat][device_type]
        assert len(device_list) > 0
        return device_list.pop(0)  # pop the first item

    def push(self, device_name):
        device_cat, device_type = self._device_map[device_name]
        device_list = self._record[device_cat][device_type]
        assert len(device_list) < self._inventory[device_cat][device_type]
        device_list.append(device_name)

    def get_spec(self, device_name, item=None):
        device_cat, device_type = self._device_map[device_name]
        if device_cat in self._spec:
            if device_type in self._spec[device_cat]:
                return self._spec[device_cat][device_type]
        log.error('cannot find spec')
        assert False
        return None

    def has_device(self, device_name):
        return device_name in self._device_map
