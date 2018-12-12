from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import range
from future.utils import listvalues
import logging
import networkx as nx

from placethings.definition import GdInfo, GtInfo


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


def find_all_simple_path(Gt):
    """
    Generate all simple paths in the graph G from source to target.
    Args:
        Gt (nx.DiGraph)
    Returns:
        src_list (list of str): source nodes
        dst_list (list of str): dstination nodes
        all_paths (list of list(str)): all simple paths of nodes' names
    """
    src_list = _find_src_nodes(Gt)
    dst_list = _find_dst_nodes(Gt)
    log.info('find all path from {} to {}'.format(src_list, dst_list))
    all_paths = []
    for src in src_list:
        for dst in dst_list:
            paths = list(nx.all_simple_paths(Gt, src, dst))
            log.info('found path: {}'.format(paths))
            all_paths += paths
    return src_list, dst_list, all_paths


def get_path_length(path, Gt, Gd, result_mapping):
    log.info('path: {}'.format(path))
    path_vars = []
    # first node: src
    ti = path[0]
    di = Gt.node[ti][GtInfo.DEVICE]
    # device_mapping start from path[1] to path[N-1]
    for j in range(1, len(path)-1):
        tj = path[j]
        dj = result_mapping[tj]
        # get transmission latency from di -> dj
        Ld_di_dj = Gd[di][dj][GdInfo.LATENCY]
        path_vars.append(Ld_di_dj)
        log.debug('Ld_di_dj (move {} -> {}) = {}'.format(di, dj, Ld_di_dj))
        # get computation latency for task tj at dj
        dj_type = Gd.node[dj][GdInfo.DEVICE_TYPE]
        # get latency of the default build flavor
        Lt_tj_dj = listvalues(Gt.node[tj][GtInfo.LATENCY_INFO][dj_type])[0]
        path_vars.append(Lt_tj_dj)
        log.debug('Lt_tj_dj (do {} at {}) = {}'.format(tj, dj, Lt_tj_dj))
        ti = tj
        di = dj
    # last node: dst
    tj = path[len(path)-1]
    dj = Gt.node[tj][GtInfo.DEVICE]
    Ld_di_dj = Gd[di][dj][GdInfo.LATENCY]
    path_vars.append(Ld_di_dj)
    log.debug('Ld_di_dj (move {} -> {}) = {}'.format(di, dj, Ld_di_dj))
    path_length = sum(path_vars)
    log.info('\tlength: {}, {}'.format(path_length, path_vars))
    return path_length
