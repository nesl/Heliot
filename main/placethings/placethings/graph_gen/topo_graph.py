from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from copy import deepcopy
from future.utils import iteritems
import logging

from placethings.config import nw_device_data
from placethings.config.common import LinkHelper, InventoryManager
from placethings.config.definition.common_def import GInfo, GnInfo, LinkInfo, NodeType
from placethings.graph_gen.graph_utils import GraphGen, FileHelper


log = logging.getLogger()


def _derive_node_info(device_spec, device_inventory):
    all_device_info = {}
    inventory_manager = InventoryManager(device_inventory)
    device_record = inventory_manager.get_device_record()
    for device_cat, inventory_info in iteritems(device_record):
        for device_type, device_list in iteritems(inventory_info):
            for device_name in device_list:
                # copy link spec
                link_spec_dict = device_spec[device_cat][device_type]
                device_info = {
                    GInfo.NODE_TYPE: NodeType.NW_DEVICE,
                    GnInfo.DEVICE_CAT: device_cat,
                    GnInfo.DEVICE_TYPE: device_type,
                    GnInfo.LINK_INFO: deepcopy(link_spec_dict),
                }
                all_device_info[device_name] = device_info
    return all_device_info


def _get_link_info(inventory, name, link_type):
    spec = inventory.get_spec(name)[link_type]
    return (
        spec[LinkInfo.ULINK_BW],
        spec[LinkInfo.DLINK_BW],
        spec[LinkInfo.PROTOCOL])


def _derive_edge_info(nw_device_spec, nw_device_inventory, links):
    inventory = InventoryManager(nw_device_inventory, spec=nw_device_spec)
    edge_info = {}
    for edge_str, edge_data in iteritems(links):
        n1, n2 = LinkHelper.get_nodes(edge_str)
        link_type1 = edge_data[GnInfo.SRC_LINK_TYPE]
        link_type2 = edge_data[GnInfo.DST_LINK_TYPE]
        est_bandwidth = edge_data.get(GnInfo.BANDWIDTH, 2147483647)
        ul1, dl1, prot1 = _get_link_info(inventory, n1, link_type1)
        ul2, dl2, prot2 = _get_link_info(inventory, n2, link_type2)
        assert prot1 == prot2
        edge_info[edge_str] = {
            GnInfo.SRC_LINK_TYPE: link_type1,
            GnInfo.DST_LINK_TYPE: link_type2,
            GnInfo.BANDWIDTH: min(ul1, dl2, est_bandwidth),
            GnInfo.PROTOCOL: prot1,
        }
        if GnInfo.LATENCY in edge_data:
            assert GnInfo.DISTANCE not in edge_data
            edge_info[edge_str][GnInfo.LATENCY] = edge_data[GnInfo.LATENCY]
        if GnInfo.DISTANCE in edge_data:
            assert GnInfo.LATENCY not in edge_data
            edge_info[edge_str][GnInfo.DISTANCE] = edge_data[GnInfo.DISTANCE]
    return edge_info


def _derive_graph_info(spec, inventory, links):
    node_info = _derive_node_info(spec, inventory)
    edge_info = _derive_edge_info(spec, inventory, links)
    return node_info, edge_info


def create_graph(spec, inventory, links, is_export=False, export_suffix=''):
    node_info, edge_info = _derive_graph_info(spec, inventory, links)
    graph = GraphGen.create(node_info, edge_info)
    if is_export:
        export_data_name = 'topo_graph{}'.format(export_suffix)
        FileHelper.export_graph(graph, export_data_name)
        FileHelper.export_data(node_info, edge_info, export_data_name)
    return graph


def create_graph_from_file(filepath, is_export=False):
    spec, inventory, links = nw_device_data.import_data(filepath)
    return create_graph(spec, inventory, links, is_export)
