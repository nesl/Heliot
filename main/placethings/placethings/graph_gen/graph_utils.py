from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from future.utils import iteritems
import networkx as nx

from placethings.utils import common_utils, json_utils, plot_utils


log = logging.getLogger()


class GraphGen(object):
    @staticmethod
    def create(node_info, edge_info, base_graph=None):
        """
        Args:
            task_info (dict)
            edge_info (dict)
            graph (networkx.DiGraph): the base graph to add nodes / edges
        Returns:
            graph (networkx.DiGraph)
        """
        if not base_graph:
            base_graph = nx.DiGraph()
        for name, attr in iteritems(node_info):
            base_graph.add_node(name, **attr)
        for edge_str, attr in iteritems(edge_info):
            src_node, dst_node = edge_str.split(' -> ')
            assert src_node in base_graph.nodes()
            assert dst_node in base_graph.nodes()
            base_graph.add_edge(src_node, dst_node, **attr)
        return base_graph


class FileHelper(object):
    OUTPUT_FOLDER = 'output'

    @classmethod
    def gen_config_filepath(cls, data_name):
        filename = '{}.json'.format(data_name)
        return common_utils.get_config_filepath(cls.OUTPUT_FOLDER, filename)

    @classmethod
    def gen_graph_filepath(cls, data_name):
        filename = '{}.png'.format(data_name)
        return common_utils.get_config_filepath(cls.OUTPUT_FOLDER, filename)

    @classmethod
    def export_graph(
            cls, graph, graph_type,
            with_edge=True, which_edge_label=None, edge_label_dict=None,
            node_label_dict=None):
        filepath = cls.gen_graph_filepath(graph_type)
        plot_utils.plot(
            graph,
            with_edge=with_edge,
            which_edge_label=which_edge_label,
            edge_label_dict=edge_label_dict,
            node_label_dict=node_label_dict,
            filepath=filepath)

    @classmethod
    def export_data(cls, node_info, edge_info, data_name):
        """Export data."""
        filepath = cls.gen_config_filepath(data_name)
        filemap = dict(
            node_info=node_info,
            edge_info=edge_info)
        json_utils.export_bundle(filepath, filemap)

    @classmethod
    def import_data(cls, data_name):
        """Import data.

        Returns:
            node_info (dict)
            edge_info (dict)

        """
        filepath = cls.gen_config_filepath(data_name)
        filemap = json_utils.import_bundle(filepath)
        node_info = filemap['node_info']
        edge_info = filemap['edge_info']
        return node_info, edge_info
