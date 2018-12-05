from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import time

from placethings import ilp_solver
from placethings.config import device_data, nw_device_data
from placethings.definition import GnInfo, Unit
from placethings.graph_gen import graph_factory, device_graph
from placethings.config.config_factory import FileHelper
from placethings.netgen.network import ControlPlane, DataPlane, NetGen


log = logging.getLogger()


_DEFAULT_CONFIG = 'config_default'


def _gen_topo_device_graph(config_name, is_export):
    # generate topo device graph
    dev_file = FileHelper.gen_config_filepath(config_name, 'device_data')
    nw_file = FileHelper.gen_config_filepath(config_name, 'nw_device_data')
    spec, inventory, links = device_data.import_data(dev_file)
    nw_spec, nw_inventory, nw_links = nw_device_data.import_data(nw_file)
    topo_graph, topo_device_graph, Gd = device_graph.create_topo_device_graph(
        spec, inventory, links, nw_spec, nw_inventory, nw_links, is_export)
    return topo_graph, topo_device_graph, Gd


def _gen_agent_name(device_name):
    return 'A-{}'.format(device_name)


def test_deploy_default(config_name=None, is_export=True):
    if not config_name:
        config_name = _DEFAULT_CONFIG
    # generate input topo, device task data
    Gt = graph_factory.gen_task_graph(config_name, is_export)
    topo_graph, topo_device_graph, Gd = _gen_topo_device_graph(
        config_name, is_export)
    G_map = ilp_solver.place_things(Gt, Gd, is_export)
    # simulate network
    control_plane = ControlPlane(topo_device_graph)
    control_plane.add_manager('HOME_ROUTER.0')
    control_plane.deploy_agent()
    # control_plane.runAgent()
    data_plane = DataPlane(topo_device_graph)
    data_plane.add_manager('HOME_ROUTER.0')
    data_plane.deploy_task(G_map, Gd)
    data_plane.start()
    time.sleep(20)
    # cleanup
    data_plane.stop()


def test_deploy_basic(config_name=None, is_export=False):
    if not config_name:
        config_name = _DEFAULT_CONFIG
    # generate topo device graph
    dev_file = FileHelper.gen_config_filepath(config_name, 'device_data')
    nw_file = FileHelper.gen_config_filepath(config_name, 'nw_device_data')
    spec, inventory, links = device_data.import_data(dev_file)
    nw_spec, nw_inventory, nw_links = nw_device_data.import_data(nw_file)
    topo_device_graph, _device_graph = device_graph.create_topo_device_graph(
        spec, inventory, links, nw_spec, nw_inventory, nw_links, is_export)
    net = NetGen.create(topo_device_graph)
    net.start()
    net.validate()

    command_switch_dir = 'cd /home/kumokay/github/placethings'
    port = 18800
    all_ips = set()

    device = 'PHONE.0'
    ip = net.get_device_ip(device)
    port += 1
    command_start = 'python main_entity.py run_agent -a {}:{}'.format(
        ip, port)
    net.run_cmd(device, command_switch_dir, async=False)
    net.run_cmd(device, command_start, async=True)
    all_ips.add((ip, port))

    device = 'CAMERA.0'
    ip = net.get_device_ip(device)
    port += 1
    command_start = 'python main_entity.py run_task -a {}:{} -t {}'.format(
        ip, port, 5000)
    net.run_cmd(device, command_switch_dir, async=False)
    net.run_cmd(device, command_start, async=True)
    all_ips.add((ip, port))

    device = 'T2_MICRO.0'
    port += 1
    ip = net.get_device_ip(device)
    command_start = 'python main_entity.py run_agent -a {}:{}'.format(
        ip, port)
    net.run_cmd(device, command_switch_dir, async=False)
    net.run_cmd(device, command_start, async=True)
    all_ips.add((ip, port))

    # cleanup
    for ip, port in all_ips:
        device = 'T2_MICRO.1'
        command_start = 'python main_entity.py stop_server -a {}:{}'.format(
            ip, port)
        net.run_cmd(device, command_switch_dir, async=False)
        net.run_cmd(device, command_start, async=False)
        all_ips.add((ip, port))
    net.stop()


def test_netgen(config_name=None, is_export=False):
    if not config_name:
        config_name = _DEFAULT_CONFIG
    # generate topo device graph
    dev_file = FileHelper.gen_config_filepath(config_name, 'device_data')
    nw_file = FileHelper.gen_config_filepath(config_name, 'nw_device_data')
    spec, inventory, links = device_data.import_data(dev_file)
    nw_spec, nw_inventory, nw_links = nw_device_data.import_data(nw_file)
    topo_device_graph, _device_graph = device_graph.create_topo_device_graph(
        spec, inventory, links, nw_spec, nw_inventory, nw_links, is_export)
    net = NetGen.create(topo_device_graph)
    net.start()
    net.validate()
    net.stop()


def test_config(config_name=None, is_export=False):
    if not config_name:
        config_name = _DEFAULT_CONFIG
    Gt = graph_factory.gen_task_graph(config_name, is_export)
    Gd = graph_factory.gen_device_graph(config_name, is_export)
    ilp_solver.place_things(Gt, Gd, is_export)


def test_dynamic(config_name=None, is_export=False):
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
