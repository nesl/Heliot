from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from future.utils import iteritems

import networkx as nx

from placethings import config_factory
from placethings.definition import Const, GdInfo, GnInfo
from placethings.topology import TopoGraph
from placethings.utils import json_utils, common_utils


log = logging.getLogger()


class NetworkGraph(object):

    _DEFAULT_DEVICE_TO_SWITCH_RATIO = 5

    @staticmethod
    def _add_nodes(graph, device_info):
        for name, attr in iteritems(device_info):
            graph.add_node(name, **attr)

    @staticmethod
    def _add_edges(graph, topo_graph):
        for src in graph.nodes():
            for dst in graph.nodes():
                if src == dst:
                    continue
                try:
                    total_latency = nx.shortest_path_length(
                        topo_graph,
                        source=src,
                        target=dst,
                        weight=GnInfo.LATENCY)
                except nx.NetworkXNoPath:
                    total_latency = Const.INT_MAX
                attr = {
                    GdInfo.LATENCY: total_latency,
                }
                graph.add_edge(src, dst, **attr)

    @classmethod
    def create(cls, device_info, topo_graph):
        """
        Args:
            device_info (dict): device attributes
            topo_graph (networkx.DiGraph): how computing devices connected to
                network devices (routers, switches, APs)
        Returns:
            network_graph (networkx.DiGraph): end-to-end relationship between
                computing devices
        """
        graph = nx.DiGraph()
        # create graph from input data
        cls._add_nodes(graph, device_info)
        cls._add_edges(graph, topo_graph)
        return graph

    @classmethod
    def create_default_device_info(cls):
        # generate default device info
        _device_spec, _device_inventory = (
            config_factory.create_default_device_data())
        device_spec, device_inventory = json_utils.import_bundle(
            common_utils.get_file_path('config_default/device_data.json'),
            'device_spec', 'device_inventory')
        assert _device_spec == device_spec
        assert _device_inventory == device_inventory
        return config_factory.derive_device_info(device_spec, device_inventory)

    @classmethod
    def create_default_graph(cls):
        all_device_info = cls.create_default_device_info()
        n_switch = len(all_device_info) // cls._DEFAULT_DEVICE_TO_SWITCH_RATIO
        switch_list = TopoGraph.create_default_switch_list(n_switch)
        topo_graph = TopoGraph.create_default_topo(
            switch_list, list(all_device_info))
        # generate network graph
        graph = cls.create(all_device_info, topo_graph)
        return graph
