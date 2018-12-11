from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from placethings.config import default_def
from placethings.utils import json_utils


log = logging.getLogger()


def _get_default_task_mapping():
    return default_def.TASK_MAPPING


def _get_default_task_links():
    return default_def.TASK_LINKS


def _get_default_task_info():
    return default_def.TASK_INFO


def create_default_task_data():
    task_mapping = _get_default_task_mapping()
    task_links = _get_default_task_links()
    task_info = _get_default_task_info()
    return task_mapping, task_links, task_info


def export_data(filepath):
    task_mapping, task_links, task_info = create_default_task_data()
    filemap = dict(
        task_mapping=task_mapping,
        task_links=task_links,
        task_info=task_info)
    json_utils.export_bundle(filepath, filemap)


def import_data(filepath):
    filemap = json_utils.import_bundle(filepath)
    task_mapping = filemap['task_mapping']
    task_links = filemap['task_links']
    task_info = filemap['task_info']
    return task_mapping, task_links, task_info
