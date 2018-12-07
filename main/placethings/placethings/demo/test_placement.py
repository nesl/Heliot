from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from placethings import ilp_solver
from placethings.config import device_data, nw_device_data
from placethings.definition import GnInfo, Unit
from placethings.graph_gen import graph_factory, device_graph
from placethings.config.config_factory import FileHelper
from placethings.demo.base_test import BaseTestCase


log = logging.getLogger()

_DEFAULT_CONFIG = 'config_default'


class TestConfig(BaseTestCase):
    @staticmethod
    def test(config_name=None, is_export=False):
        if not config_name:
            config_name = _DEFAULT_CONFIG
        Gt = graph_factory.gen_task_graph(config_name, is_export)
        Gd = graph_factory.gen_device_graph(config_name, is_export)
        ilp_solver.place_things(Gt, Gd, is_export)


class TestDynamic(BaseTestCase):
    @staticmethod
    def test(config_name=None, is_export=False):
        if not config_name:
            config_name = _DEFAULT_CONFIG
        # generate device graph
        dev_file = FileHelper.gen_config_filepath(config_name, 'device_data')
        nw_file = FileHelper.gen_config_filepath(config_name, 'nw_device_data')
        spec, inventory, links = device_data.import_data(dev_file)
        nw_spec, nw_inventory, nw_links = nw_device_data.import_data(nw_file)
        Gd = device_graph.create_graph(
            spec, inventory, links, nw_spec, nw_inventory, nw_links, is_export)
        # generate task graph
        Gt = graph_factory.gen_task_graph(config_name, is_export)
        Gt = ilp_solver.place_things(Gt, Gd, is_export)
        update_id = 0
        # update device graph
        update_id += 1
        log.info('update round {}'.format(update_id))
        suffix = '_update{}'.format(update_id)
        del links['PHONE.0 -> BB_AP.0']
        del links['BB_AP.0 -> PHONE.0']
        links['PHONE.0 -> HOME_IOTGW.0'] = {
            GnInfo.LATENCY: Unit.ms(3),
        }
        links['HOME_IOTGW.0 -> PHONE.0'] = {
            GnInfo.LATENCY: Unit.ms(3),
        }
        Gd = device_graph.create_graph(
            spec, inventory, links, nw_spec, nw_inventory, nw_links,
            is_export, export_suffix='_update{}'.format(update_id))
        Gt = ilp_solver.place_things(Gt, Gd, is_export, export_suffix=suffix)
        # update device graph
        update_id += 1
        log.info('update round {}'.format(update_id))
        suffix = '_update{}'.format(update_id)
        nw_links['BB_SWITCH.0 -> CLOUD_SWITCH.0'][GnInfo.LATENCY] = Unit.sec(5)
        nw_links['CLOUD_SWITCH.0 -> BB_SWITCH.0'][GnInfo.LATENCY] = Unit.sec(5)
        Gd = device_graph.create_graph(
            spec, inventory, links, nw_spec, nw_inventory, nw_links,
            is_export, export_suffix=suffix)
        Gt = ilp_solver.place_things(Gt, Gd, is_export, export_suffix=suffix)
        # update device graph
        update_id += 1
        log.info('update round {}'.format(update_id))
        suffix = '_update{}'.format(update_id)
        del links['PHONE.0 -> HOME_IOTGW.0']
        del links['HOME_IOTGW.0 -> PHONE.0']
        links['PHONE.0 -> BB_AP.0'] = {
            GnInfo.LATENCY: Unit.ms(3),
        }
        links['BB_AP.0 -> PHONE.0'] = {
            GnInfo.LATENCY: Unit.ms(3),
        }
        Gd = device_graph.create_graph(
            spec, inventory, links, nw_spec, nw_inventory, nw_links,
            is_export, export_suffix='_update{}'.format(update_id))
        Gt = ilp_solver.place_things(Gt, Gd, is_export, export_suffix=suffix)
        # update device graph
        update_id += 1
        log.info('update round {}'.format(update_id))
        suffix = '_update{}'.format(update_id)
        nw_links['BB_SWITCH.0 -> CLOUD_SWITCH.0'][GnInfo.LATENCY] = Unit.ms(5)
        nw_links['CLOUD_SWITCH.0 -> BB_SWITCH.0'][GnInfo.LATENCY] = Unit.ms(5)
        Gd = device_graph.create_graph(
            spec, inventory, links, nw_spec, nw_inventory, nw_links,
            is_export, export_suffix=suffix)
        Gt = ilp_solver.place_things(Gt, Gd, is_export, export_suffix=suffix)
