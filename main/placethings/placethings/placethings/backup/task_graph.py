from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from future.utils import iteritems
import networkx as nx
from matplotlib import pyplot as plt

from placethings import config_factory
from placethings.definition import GtInfo, Hardware
from placethings.utils import json_utils, common_utils


log = logging.getLogger()


class TaskGraph(object):

    DEVICE_NOT_ASSIGNED = 'unkown'

    @classmethod
    def create(cls, src_map, dst_map, task_info, edge_info):
        """
        Args:
            src_map (dict): mapping of sensing tasks <-> devices
            dst_map (dict): mapping of actuation tasks <-> devices
            task_info (dict)
            edge_info (dict)
        Returns:
            graph (networkx.DiGraph)

        """
        # currently only support multi-source, single destination
        assert len(src_map) > 0
        assert len(dst_map) == 1
        graph = nx.DiGraph()
        # create graph from input data
        cls._add_nodes(graph, src_map, dst_map, task_info)
        cls._add_edges(graph, edge_info)
        # derive extra information from the input data and stored in the graph
        cls._derive_data(graph, task_info)

        # check graph
        for node in graph.nodes():
            if node in src_map:
                assert graph.node[node][GtInfo.DEVICE] == src_map[node]
            elif node in dst_map:
                assert graph.node[node][GtInfo.DEVICE] == dst_map[node]
            else:
                assert graph.node[node][GtInfo.DEVICE] == (
                    cls.DEVICE_NOT_ASSIGNED)
        return graph

    @classmethod
    def _add_nodes(cls, graph, src_map, dst_map, task_info):
        for name, task_attr in iteritems(task_info):
            attr = {GtInfo.DEVICE: cls.DEVICE_NOT_ASSIGNED}
            attr.update(task_attr)
            graph.add_node(name, **attr)
        for map in [src_map, dst_map]:
            for task, device in iteritems(map):
                graph.add_node(task, **{GtInfo.DEVICE: device})

    @staticmethod
    def _add_edges(graph, edge_info):
        for edge_str, attr in iteritems(edge_info):
            src_node, dst_node = edge_str.split(' -> ')
            assert src_node in graph.nodes()
            assert dst_node in graph.nodes()
            graph.add_edge(src_node, dst_node, **attr)

    @staticmethod
    def _derive_data(graph, task_info):
        for task in task_info:
            ingress_traffic = sum(
                [graph[src][dst][GtInfo.TRAFFIC]
                    for (src, dst) in graph.edges() if dst == task])
            egress_traffic = sum(
                [graph[src][dst][GtInfo.TRAFFIC]
                    for edge in graph.edges() if src == task])
            build_rqmt_info = graph.node[task][GtInfo.RESRC_RQMT]
            for _build, rqmt in iteritems(build_rqmt_info):
                rqmt[Hardware.NIC_INGRESS] = ingress_traffic
                rqmt[Hardware.NIC_EGRESS] = egress_traffic

    @classmethod
    def create_default_graph(cls):
        _task_info, _edge_info, _src_map, _dst_map = (
            config_factory.create_default_task_graph())
        task_info, edge_info, src_map, dst_map = json_utils.import_bundle(
            common_utils.get_file_path('config_default/task_graph.json'),
            'task_info', 'edge_info', 'src_map', 'dst_map')
        assert _src_map == src_map
        assert _dst_map == dst_map
        assert _task_info == task_info
        assert _edge_info == edge_info
        return cls.create(src_map, dst_map, task_info, edge_info)

    @staticmethod
    def plot(graph):
        nx.draw_networkx(
            graph,
            pos=nx.spring_layout(graph),
            arrows=False,
            with_labels=True,
        )
        plt.show(graph)
