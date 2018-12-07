from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import os

from future.utils import iteritems


def string_to_number(byte_repr_str):
    """
    Args:
        byte_repr_str (str): e.g. 100MB, 10Kb; float is not allowed
    Returns:
        num (int): bytes
    """
    is_parsing_unit = False
    num = 0
    for ch in byte_repr_str:
        if ch.isdigit():
            assert is_parsing_unit is False
            num = num * 10 + int(ch)
            continue
        else:
            is_parsing_unit = True

        if ch.lower() == 'k':
            num = num * 1024
        elif ch.lower() == 'm':
            num = num * 1024 * 1024
        elif ch.lower() == 'g':
            num = num * 1024 * 1024 * 1024
        elif ch == 'B':
            num = num * 8
        elif ch == 'b':
            num = num * 1
        else:
            # invalid format
            assert(False)
    return num


class SerializableObject(object):
    def to_dict(self):
        ret = {}
        for objname, obj in iteritems(self.__dict__):
            if isinstance(obj, SerializableObject):
                ret[objname] = obj.to_dict()
            else:
                ret[objname] = obj
        return ret

    def to_json(self):
        return json.dumps(
            self, sort_keys=True, indent=4,
            default=lambda obj: obj.to_dict())

    def export_to_file(self, filepath):
        filedir = os.path.dirname(filepath)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        assert os.path.exists(filedir)
        with open(filepath, mode='w') as fp:
            fp.write(self.to_json())
        return os.path.exists(filepath)
