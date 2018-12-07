from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

import networkx as nx
from matplotlib import pyplot as plt

from placethings.utils import common_utils


log = logging.getLogger()


def save_plot(filepath):
    common_utils.check_file_folder(filepath)
    log.info('save plot to: {}'.format(filepath))
    plt.savefig(filepath)
    plt.close()


def plot(
        graph, pos=None,
        with_edge=True, which_edge_label=None, edge_label_dict=None,
        node_label_dict=None, filepath=None):
    if not pos:
        pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(
        graph,
        pos=pos,
        nodelist=None,
        node_size=300,
        node_color='r',
        node_shape='o',
    )
    nx.draw_networkx_labels(
        graph,
        pos=pos,
        labels=node_label_dict,
        font_size=10,
        font_color='k',
        font_family='sans-serif',
        font_weight='normal',
    )
    if with_edge:
        nx.draw_networkx_edges(
            graph,
            pos=pos,
            edgelist=None,
            width=1.0,
            edge_color='k',
            style='solid',
        )
        assert not (edge_label_dict and which_edge_label)
        if not edge_label_dict:
            if not which_edge_label:
                edge_label_dict = {}
            else:
                edge_label_dict = {
                    (src, dst): attr[which_edge_label]
                    for src, dst, attr in graph.edges(data=True)
                }
        nx.draw_networkx_edge_labels(
            graph,
            pos=pos,
            edge_labels=edge_label_dict,
            label_pos=0.5,
            font_size=10,
            font_color='k',
            font_family='sans-serif',
            font_weight='normal',
        )
    if not filepath:
        filepath = 'output/plot.png'
    save_plot(filepath)
