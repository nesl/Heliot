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


def get_max_latency(Gt, Gd, result_mapping, use_assigned_latency=True):
    src_list, dst_list, all_paths = utils.find_all_simple_path(Gt)
    max_latency = 0
    for path in all_paths:
        path_length = solver.get_path_length(
            path, Gt, Gd, result_mapping, use_assigned_latency)
        max_latency = max(path_length, max_latency)
    return max_latency


def place_things(
        Gt_ro, Gnd_ro, is_export, export_suffix='', use_assigned_latency=True):
    Gt = deepcopy(Gt_ro)
    Gnd = deepcopy(Gnd_ro)
    status, result_mapping, result_latency = solver.solve(
        Gt, Gnd, use_assigned_latency)
    assert status == pulp.constants.LpStatusOptimal
    log.info('solver status: {}'.format(pulp.LpStatus[status]))
    log.info('check solution for all simple path from src to dst')
    max_latency = get_max_latency(
        Gt, Gnd, result_mapping, use_assigned_latency=use_assigned_latency)
    log.info('max_latency={}'.format(max_latency))
    log.info('result_mapping={}'.format(result_mapping))
    log.info('result_latency={}'.format(result_latency))
    # update mapping and gen node labels
    Gt = task_graph.update_graph(
        result_mapping, result_latency, Gt, Gnd, is_export, export_suffix)
    return Gt, result_mapping
