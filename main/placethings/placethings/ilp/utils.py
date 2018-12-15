from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

import networkx as nx


log = logging.getLogger()


def _find_src_nodes(Gt):
    src_list = []
    for node in Gt.nodes():
        predecessors = list(Gt.predecessors(node))
        if not predecessors:
            src_list.append(node)
    return src_list


def _find_dst_nodes(Gt):
    dst_list = []
    for node in Gt.nodes():
        successors = list(Gt.successors(node))
        if not successors:
            dst_list.append(node)
    return dst_list


def has_simple_path(G, src, dst):
    all_path = list(nx.all_simple_paths(G, src, dst))
    return len(all_path) > 0


def find_all_simple_path(G):
    """
    Generate all simple paths in the graph G from source to target.
    Args:
        G (nx.DiGraph)
    Returns:
        src_list (list of str): source nodes
        dst_list (list of str): dstination nodes
        all_paths (list of list(str)): all simple paths of nodes' names
    """
    src_list = _find_src_nodes(G)
    dst_list = _find_dst_nodes(G)
    log.info('find all path from {} to {}'.format(src_list, dst_list))
    all_paths = []
    for src in src_list:
        for dst in dst_list:
            paths = list(nx.all_simple_paths(G, src, dst))
            log.info('found path: {}'.format(paths))
            all_paths += paths
    return src_list, dst_list, all_paths
