from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from copy import deepcopy
import logging
import pulp

# NOTE: to use glpk solver, sudo apt-get install glpk-utils

from placethings.graph_gen import task_graph
from placethings.ilp import utils, solver


log = logging.getLogger()


def get_max_latency(Gt, Gd, result_mapping):
    src_list, dst_list, all_paths = utils.find_all_simple_path(Gt)
    max_latency = 0
    for path in all_paths:
        path_length = utils.get_path_length(path, Gt, Gd, result_mapping)
        max_latency = max(path_length, max_latency)
    return max_latency


def place_things(Gt_ro, Gd_ro, is_export, export_suffix=''):
    Gt = deepcopy(Gt_ro)
    Gd = deepcopy(Gd_ro)
    status, result_mapping = solver.solve(Gt, Gd)
    assert status == pulp.constants.LpStatusOptimal
    log.info('solver status: {}'.format(pulp.LpStatus[status]))
    log.info('check solution for all simple path from src to dst')
    max_latency = get_max_latency(Gt, Gd, result_mapping)
    log.info('max_latency={}'.format(max_latency))
    # update mapping and gen node labels
    Gt = task_graph.update_graph(
        result_mapping, Gt, Gd, is_export, export_suffix)
    return Gt, result_mapping
