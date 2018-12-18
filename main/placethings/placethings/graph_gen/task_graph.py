from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from copy import deepcopy
from future.utils import listvalues, iteritems
import logging

from placethings.config import task_data
from placethings.config.common import LinkHelper
from placethings.config.definition.common_def import GtInfo, GdInfo
from placethings.graph_gen.graph_utils import GraphGen, FileHelper


log = logging.getLogger()


def _derive_node_info(task_mapping, task_info):
    node_info = {}
    for task_name, data in iteritems(task_info):
        node_info[task_name] = {
            GtInfo.LATENCY_INFO: deepcopy(data[GtInfo.LATENCY_INFO]),
            GtInfo.RESRC_RQMT: deepcopy(data[GtInfo.RESRC_RQMT]),
            GtInfo.EXEC_CMD: deepcopy(data[GtInfo.EXEC_CMD]),
            GtInfo.DEVICE: task_mapping[task_name],
        }
    return node_info


def _derive_edge_info(task_links):
    edge_info = task_links
    # nothing to derive
    return edge_info


def _derive_graph_info(task_mapping, task_links, task_info):
    node_info = _derive_node_info(task_mapping, task_info)
    edge_info = _derive_edge_info(task_links)
    return node_info, edge_info


def create_graph(
        mapping, task_links, task_info, is_export=False, export_suffix=''):
    # Creates the Task Graph
    # Each node is the task. (name) and along with the propertie
    # (build flavours and how to invoke them)
    node_info, edge_info = _derive_graph_info(mapping, task_links, task_info)
    graph = GraphGen.create(node_info, edge_info)
    if is_export:
        export_data_name = 'task_graph{}'.format(export_suffix)
        FileHelper.export_graph(graph, export_data_name)
        FileHelper.export_data(node_info, edge_info, export_data_name)
    return graph


def create_default_graph(is_export=False):
    task_mapping, task_links, task_info = task_data.create_default_task_data()
    return create_graph(task_mapping, task_info, task_links, is_export)


def create_graph_from_file(filepath, is_export=False):
    task_mapping, task_links, task_info = task_data.import_data(filepath)
    return create_graph(task_mapping, task_links, task_info, is_export)


def _gen_update_info(result_mapping, result_latency, Gt, Gnd):
    node_info = {}
    for task, device in iteritems(result_mapping):
        if Gt.node[task][GtInfo.DEVICE]:
            assert device == Gt.node[task][GtInfo.DEVICE]
        device_type = Gnd.node[device][GdInfo.DEVICE_TYPE]
        latency_info = Gt.node[task][GtInfo.LATENCY_INFO]
        exec_cmd = deepcopy(Gt.node[task][GtInfo.EXEC_CMD])
        compute_latency = 0 if not latency_info else (
            listvalues(latency_info[device_type])[0])
        node_info[task] = {
            GtInfo.CUR_DEVICE: device,
            GtInfo.CUR_LATENCY: compute_latency,
            GtInfo.EXEC_CMD: exec_cmd
        }
    edge_info = {}
    for (t1, t2) in Gt.edges():
        transmission_latency = result_latency[(t1, t2)]
        edge_info[LinkHelper.get_edge(t1, t2)] = {
            GtInfo.CUR_LATENCY: transmission_latency,
        }
    return node_info, edge_info


def _gen_graph_labels(Gt):
    node_labels = {}
    for task in Gt.nodes():
        node_labels[task] = '{}\n{}({}ms)'.format(
            task,
            Gt.node[task][GtInfo.CUR_DEVICE],
            Gt.node[task][GtInfo.CUR_LATENCY])
    edge_labels = {}
    for edge in Gt.edges():
        t1, t2 = edge
        transmission_latency = Gt[t1][t2][GtInfo.CUR_LATENCY]
        edge_labels[edge] = '{}ms'.format(transmission_latency)
    return node_labels, edge_labels


def update_graph(
        result_mapping, result_latency, Gt, Gnd, is_export, export_suffix=''):
    node_info, edge_info = _gen_update_info(
        result_mapping, result_latency, Gt, Gnd)
    Gt = GraphGen.create(node_info, edge_info, base_graph=Gt)
    if is_export:
        export_data_name = 'task_graph_map{}'.format(export_suffix)
        node_labels, edge_labels = _gen_graph_labels(Gt)
        FileHelper.export_graph(
            Gt, export_data_name,
            with_edge=True, edge_label_dict=edge_labels,
            node_label_dict=node_labels)
        FileHelper.export_data(node_info, edge_info, export_data_name)
    return Gt
