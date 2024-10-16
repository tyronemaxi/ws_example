#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: request.py
Time: 2024/10/15 09:57
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import functools
from functools import partial
from typing import Any, Type, Tuple, List

from flask_restful import request
from werkzeug.exceptions import BadRequest

from app.core.http_code import ParamCheckError as ParamCheckErrorCode
from app.core.exception import ParamsCheckError


def fields(type: (Type, Tuple[Type]), required: bool = False, choices: (tuple, list) = None, dest: str = None,
           location=None, default: Any = None, children: dict = None, process: (Tuple[Any], List[Any]) = None):
    """
    参数定义
    :param type: 参数类型 如非此类型,且不可转换时将报错
    :param required: 是否必传 传入参数中是否必须有此参数
    :param choices: 输入参数范围 超出范围将报错
    :param dest: 参数名称转换
    :param location: 参数来源位置
    :param default: 当参数未传时 默认补全参数
    :param children: 子参数信息 当参数是可迭代对象时,进一步定义子参数信息
    :param process: 处理方法 可以传递1个或1组方法对入参进行处理
    :return: 参数要求字典
    """
    if required is True and default:
        raise KeyError("The parameter [default] will not run when 'required = True'")
    if default is not None and not isinstance(default, type):
        raise TypeError("The parameter [{}] does not belong to {}".format(default, type))
    if dest is not None and not dest:
        raise KeyError("The parameter [dest] not allowed to be empty")
    if choices is not None and (not choices or not isinstance(choices, (tuple, list))):
        raise KeyError("The parameter [choices] must have a value when used and belong to the '(list,tuple)'")

    location_enum = ("json", "form", "args", "values", "headers", "cookies", "file", "files")
    if location is not None:
        if location not in location_enum:
            raise KeyError("The parameter [location] just allowed {}".format(location_enum))
        if location not in ("json", "args", "headers", "form", "file", "files"):
            raise KeyError("The parameter [location]-[{}] not supported yet, please add it yourself~".format(location))

    return dict(type=type, required=required, choices=choices, dest=dest, location=location, default=default,
                children=children, process=process)


def args_parser(args_map: dict):
    """
    参数解析入口方法
    整体风格偏向倾向于 flask_restful.reparser, 并进行了功能扩展
    :param args_map: 由 field 方法组成的参数要求字典
    :return: 装饰器
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            input_data = parser_input(args_map, **kwargs)
            args_process(args_map=args_map, input_data=input_data)
            return func(*args, **input_data)
        return wrapper
    return decorator


def parser_input(args_map: dict, **kwargs):
    """
    参数解析
    :param args_map: 由 field 方法组成的参数要求字典
    :param kwargs: API 入参
    :return: 提取后的入参字典
    """
    default_location = "args" if request.method == "GET" else "json"
    input_data = kwargs if kwargs else {}
    for arg_key, arg_value in args_map.items():
        location = arg_value["location"] if arg_value.get("location") is not None else default_location
        if arg_key in input_data:
            input_data[arg_key] = arg_value.get("type")(input_data[arg_key])
        if location == "json":
            v = request.get_json().get(arg_key) if request.get_json(silent=True) else None
        elif location == "args":
            v = request.args.get(arg_key, type=arg_value.get("type"))
        elif location == "headers":
            v = request.headers.get(arg_key)
        elif location == "form":
            v = request.form.get(arg_key, type=arg_value.get("type"))
        elif location == "file":
            v = request.files.get(arg_key)
        elif location == "files":
            v = request.files.getlist(arg_key)
        else:
            raise KeyError("Unsupported location '{}'".format(location))

        if v is not None:
            input_data[arg_key] = v

    return input_data


def args_process(args_map: dict, input_data: dict):
    """
    参数处理方法
    :param args_map: 由 field 方法组成的参数要求字典
    :param input_data: 提取后的 API 入参
    :return: None 所有参数原地修改
    """
    for arg_key, arg_value in args_map.items():
        if arg_key not in input_data:
            if arg_value.get("required") is True:
                raise BadRequest("Missing required parameters [{}]".format(arg_key))
            if arg_value.get("default") is not None:
                input_data[arg_key] = arg_value["default"]
            else:
                input_data[arg_key] = None

        else:
            if arg_value.get("type"):
                if not isinstance(arg_value["type"], (tuple, list)):
                    arg_value["type"] = (arg_value["type"])
                if not isinstance(input_data[arg_key], arg_value["type"]) and input_data[arg_key] is not None:
                    raise BadRequest("The type '{}' of parameter [{}] is not the set type '{}'".format(
                        type(input_data[arg_key]), arg_key, arg_value["type"]))

            if arg_value.get("choices"):
                if input_data[arg_key] not in arg_value["choices"]:
                    raise BadRequest("The parameter [{}] value is allowed '{}'".format(arg_key, arg_value["choices"]))

            if arg_value.get("process"):
                if not isinstance(arg_value["process"], (tuple, list)):
                    arg_value["process"] = (arg_value["process"],)
                for f in arg_value["process"]:
                    try:
                        input_data[arg_key] = f(input_data[arg_key])
                    except Exception as e:
                        e.args = ("The parameter [{}] {}".format(arg_key, e.args[0]),)
                        raise e

        if arg_value.get("children"):
            if isinstance(input_data[arg_key], dict):
                args_process(arg_value["children"], input_data[arg_key])
            elif isinstance(input_data[arg_key], list):
                for input_item in input_data[arg_key]:
                    args_process(arg_value["children"], input_item)
            elif input_data[arg_key] is None:
                continue
            else:
                raise TypeError("The elements in 'children' only attention list or dict")

        if arg_value.get("dest") and arg_key in input_data:
            input_data[arg_value["dest"]] = input_data.pop(arg_key)


def strip(text: str):
    return text.strip()


def not_in(params: Any, words: (tuple, list)):
    for w in words:
        if w in params:
            raise ValueError("'{}' is not allowed".format(w))
    return params


def not_empty(params: Any):
    if not params:
        raise ValueError("not allowed to be empty")
    return params


def length_check(params: Any, operation: str, length: int):
    if operation == "gt":
        check = bool(len(params) > length)
    elif operation == "gte":
        check = bool(len(params) >= length)
    elif operation == "lt":
        check = bool(len(params) < length)
    elif operation == "lte":
        check = bool(len(params) <= length)
    elif operation == "equal":
        check = bool(len(params) == length)
    else:
        msg = "Not support [operation] '{}'".format(operation)
        err = ParamsCheckError(code=ParamCheckErrorCode, message=msg)
        err.args = (err.message,)
        raise err

    if check is False:
        msg = "accept length {} {}".format(operation, length)
        err = ParamsCheckError(code=ParamCheckErrorCode, message=msg)
        err.args = (err.message,)
        raise err

    return params


def wrapper_list(params: Any):
    if not isinstance(params, list):
        return [params]
    return params


def as_type(params: Any, type: Type):
    return type(params)


def id_check(params: (int, list)):
    if isinstance(params, int):
        if params < -1:
            raise ValueError("not allowed to lt than -1")
    else:
        for p in params:
            if p < -1:
                raise ValueError("not allowed to lt than -1")
    return params


def check_datetime(date_str: str):
    if len(date_str) != 19:
        raise ValueError("only supports '%Y-%m-%d %H:%M:%S'")
    return date_str


def check_duplicate(lst: list):
    if len(lst) != len(set(lst)):
        raise ValueError("have duplicate value")
    return lst


def search_start_datetime(start: (datetime.datetime, str)):
    if isinstance(start, str) and len(start) == 19:
        return start
    if isinstance(start, datetime.datetime):
        start = start.date()
    else:
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
    start = start.strftime("%Y-%m-%d %H:%M:%S")
    return start


def search_end_datetime(end: (datetime.datetime, str)):
    if isinstance(end, str) and len(end) == 19:
        return end

    if isinstance(end, datetime.datetime):
        end = end + datetime.timedelta(days=1)
        end = end.date()
    else:
        end = datetime.datetime.strptime(end, "%Y-%m-%d") + datetime.timedelta(days=1)

    end = end.strftime("%Y-%m-%d %H:%M:%S")
    return end


lte_3 = partial(length_check, operation="lte", length=3)
lte_200 = partial(length_check, operation="lte", length=200)
lte_50 = partial(length_check, operation="lte", length=50)
lte_15 = partial(length_check, operation="lte", length=15)
lte_500 = partial(length_check, operation="lte", length=500)
equal_4 = partial(length_check, operation="equal", length=4)
gte_1 = partial(length_check, operation="gte", length=1)
as_int = partial(as_type, type=int)