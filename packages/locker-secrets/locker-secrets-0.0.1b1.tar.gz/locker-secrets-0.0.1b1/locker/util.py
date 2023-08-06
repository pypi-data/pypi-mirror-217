from __future__ import absolute_import, division, print_function

import datetime
import functools
import hmac
import io
import logging
import sys
import os
import re
import calendar
from collections import OrderedDict

import six
import time

import locker


def get_object_classes():
    # This is here to avoid a circular dependency
    from locker.object_classes import OBJECT_CLASSES
    return OBJECT_CLASSES


def convert_to_ls_object(
    resp, access_key=None, api_base=None, api_version=None, params=None
):
    # If we get a LSResponse, we'll want to return a
    # LSObject with the last_response field filled out with
    # the raw API response information
    ls_response = None

    if isinstance(resp, locker.ls_response.LSResponse):
        ls_response = resp
        resp = ls_response.data

    if isinstance(resp, list):
        return [
            convert_to_ls_object(i, access_key, api_base, api_version) for i in resp
        ]
    elif isinstance(resp, dict) and not isinstance(
        resp, locker.ls_object.LSObject
    ):
        resp = resp.copy()
        klass_name = resp.get("object")
        if isinstance(klass_name, six.string_types):
            klass = get_object_classes().get(
                klass_name, locker.ls_object.LSObject
            )
        else:
            klass = locker.ls_object.LSObject

        obj = klass.construct_from(
            resp,
            access_key=access_key,
            api_base=api_base,
            api_version=api_version,
            last_response=ls_response,
        )

        # We only need to update _retrieve_params when special params were
        # actually passed. Otherwise, leave it as is as the list / search result
        # constructors will instantiate their own params.
        if (
            params is not None
            and hasattr(obj, "object")
            and ((obj.object == "list") or (obj.object == "search_result"))
        ):
            obj._retrieve_params = params
        return obj
    else:
        return resp


def read_special_variable(params, key_name, default_value):
    value = default_value
    params_value = None

    if params is not None and key_name in params:
        params_value = params[key_name]
        del params[key_name]
    if value is None:
        value = params_value
    return value


def encode_datetime(dttime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        utc_timestamp = time.mktime(dttime.timetuple())

    return int(utc_timestamp)


def _encode_datetime(dttime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        utc_timestamp = time.mktime(dttime.timetuple())

    return int(utc_timestamp)


def _encode_nested_dict(key, data, fmt="%s[%s]"):
    d = OrderedDict()
    for sub_key, sub_value in six.iteritems(data):
        d[fmt % (key, sub_key)] = sub_value
    return d


def api_encode(data):
    for key, value in six.iteritems(data):
        if value is None:
            continue
        elif hasattr(value, "locker_id"):
            yield key, value.stripe_id
        elif isinstance(value, list) or isinstance(value, tuple):
            for i, sv in enumerate(value):
                if isinstance(sv, dict):
                    subdict = _encode_nested_dict("%s[%d]" % (key, i), sv)
                    for k, v in api_encode(subdict):
                        yield k, v
                else:
                    yield "%s[%d]" % (key, i), sv
        elif isinstance(value, dict):
            subdict = _encode_nested_dict(key, value)
            for sub_key, sub_value in api_encode(subdict):
                yield sub_key, sub_value
        elif isinstance(value, datetime.datetime):
            yield key, _encode_datetime(value)
        else:
            yield key, value


# def background_exception_wrapper(func):
#     def wrap(*args, **kwargs):
#         try:
#             result = func(*args, **kwargs)
#             return result
#         except Exception as e:
#             tb = traceback.format_exc()
#             CyLog.error(**{"message": f"{func.__name__} error: {tb}"})
#         finally:
#             connection.close()
#     return wrap

# def class_method_variant(class_method_name):
#     def wrap(*args, **kwargs):
#         if obj is not None:
#             # Method was called as an instance method, e.g.
#             # instance.method(...)
#             return self.method(obj, *args, **kwargs)
#         elif len(args) > 0 and isinstance(args[0], objtype):
#             # Method was called as a class method with the instance as the
#             # first argument, e.g. Class.method(instance, ...) which in
#             # Python is the same thing as calling an instance method
#             return self.method(args[0], *args[1:], **kwargs)
#         else:
#             # Method was called as a class method, e.g. Class.method(...)
#             class_method = getattr(objtype, self.class_method_name)
#             return class_method(*args, **kwargs)
#
#     def __call__(self, method):
#         self.method = method
#         return self
#
#     def __get__(self, obj, objtype=None):
#         @functools.wraps(self.method)
#         def _wrapper(*args, **kwargs):
#             if obj is not None:
#                 # Method was called as an instance method, e.g.
#                 # instance.method(...)
#                 return self.method(obj, *args, **kwargs)
#             elif len(args) > 0 and isinstance(args[0], objtype):
#                 # Method was called as a class method with the instance as the
#                 # first argument, e.g. Class.method(instance, ...) which in
#                 # Python is the same thing as calling an instance method
#                 return self.method(args[0], *args[1:], **kwargs)
#             else:
#                 # Method was called as a class method, e.g. Class.method(...)
#                 class_method = getattr(objtype, self.class_method_name)
#                 return class_method(*args, **kwargs)
#
#         return _wrapper
