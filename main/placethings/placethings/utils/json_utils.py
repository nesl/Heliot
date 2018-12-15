from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future.utils import iteritems
import logging
import json
import os

from placethings.utils import common_utils
from placethings.config.definition.common_def import EnumHelper


log = logging.getLogger()


class CustomEncoder(json.JSONEncoder):
    @classmethod
    def _convert_keys_to_strs(cls, dict_obj):
        new_dict = {}
        for key, value in iteritems(dict_obj):
            if isinstance(value, dict):
                value = cls._convert_keys_to_strs(value)
            if EnumHelper.is_enum(key):
                new_dict[EnumHelper.enum_to_str(key)] = value
            else:
                new_dict[key] = value
        return new_dict

    def iterencode(self, obj):
        log.debug('encode using CustomEncoder.iterencode')
        if isinstance(obj, dict):
            obj = self._convert_keys_to_strs(obj)
        return super(CustomEncoder, self).iterencode(obj)

    def default(self, obj):
        log.debug('encode using CustomEncoder.default')
        if EnumHelper.is_enum(obj):
            return EnumHelper.enum_to_str(obj)
        return super(CustomEncoder, self).default(obj)


class CustomDecoder(json.JSONDecoder):
    @classmethod
    def _convert_keys_from_strs(cls, dict_obj):
        new_dict = {}
        for key, value in iteritems(dict_obj):
            if isinstance(value, dict):
                value = cls._convert_keys_from_strs(value)
            elif isinstance(value, (str, unicode)):
                value = EnumHelper.str_to_enum(value)
            new_key = EnumHelper.str_to_enum(key)
            if new_key:
                new_dict[new_key] = value
            else:
                new_dict[key] = value
        return new_dict

    def decode(self, obj):
        log.info('decode using CustomDecoder')
        obj = super(CustomDecoder, self).decode(obj)
        if isinstance(obj, dict):
            obj = self._convert_keys_from_strs(obj)
        elif isinstance(obj, (str, unicode)):
            obj = EnumHelper.str_to_enum(obj)
        return obj


def to_json(obj):
    pretty_str = json.dumps(
        obj, indent=4, separators=(',', ': '), cls=CustomEncoder)
    return pretty_str


def from_json(json_str):
    obj = json.loads(json_str, cls=CustomDecoder)
    return obj


def export_to_file(filepath, obj):
    common_utils.check_file_folder(filepath)
    with open(filepath, mode='w') as fp:
        json.dump(obj, fp, indent=4, separators=(',', ': '), cls=CustomEncoder)
    log.info('exported to file: {}'.format(filepath))
    return os.path.exists(filepath)


def import_from_file(filepath):
    assert os.path.exists(filepath)
    with open(filepath) as fp:
        obj = json.load(fp, cls=CustomDecoder)
    log.info('imported from file: {}'.format(filepath))
    return obj


def export_bundle(filepath, filemap, if_verify=True):
    """
    Args:
        filepath (str): save all data to the file
        filemap (dict): {data_struct_name: data_struct_obj}
        if_verify (bool): verify if the exproted file is exactly the same
            as the assigned data structure
    """
    is_success = export_to_file(filepath, filemap)
    assert is_success
    imported_filemap = import_bundle(filepath)
    assert imported_filemap == filemap
    return True


def import_bundle(filepath, *args):
    """
    Args:
        filepath (str): save all data to the file
        *args (str): desired data_struct names
    Returns:
        filemap (dict): {data_struct_name: data_struct_obj}
    """
    bundle = import_from_file(filepath)
    if not args:
        return bundle
    else:
        filemap = {}
        for name in args:
            filemap[args] = bundle[args]
        return filemap
