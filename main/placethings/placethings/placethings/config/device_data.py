from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from placethings.config import default_def, spec_def
from placethings.config.common import Validator
from placethings.utils import json_utils


log = logging.getLogger()


def get_default_spec():
    return spec_def.DEVICE_SPEC


def get_default_links():
    return default_def.DEVICE_LINKS


def get_default_inventory(device_spec):
    log.info('create default device inventory')
    device_inventory = default_def.DEVICE_INVENTORY
    # validate the inventory
    assert Validator.validate_inventory(device_spec, device_inventory)
    return device_inventory


def create_default_device_data():
    device_spec = get_default_spec()
    device_inventory = get_default_inventory(device_spec)
    links = get_default_links()
    return device_spec, device_inventory, links


def get_device_data(filepath):
    device_spec, device_inventory, links = import_data(filepath)
    return device_spec, device_inventory, links


def export_data(filepath):
    device_spec, device_inventory, links = create_default_device_data()
    filemap = dict(
        device_spec=device_spec,
        device_inventory=device_inventory,
        links=links)
    json_utils.export_bundle(filepath, filemap)


def import_data(filepath):
    filemap = json_utils.import_bundle(filepath)
    device_spec = filemap['device_spec']
    device_inventory = filemap['device_inventory']
    links = filemap['links']
    return device_spec, device_inventory, links
