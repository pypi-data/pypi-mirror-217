from __future__ import annotations
from typing import Dict, List, Union
import json


JsonValue = Union[str, int, float, bool, type(None), "JsonArray", "JsonObject"]
JsonArray = List[Union[JsonValue, "CommentedValue"]]
JsonObject = Dict[str, Union[JsonValue, "CommentedValue"]]


class CommentedValue:
    comment: str
    value: JsonValue


def dump(
    obj: JsonValue,
    fp,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
    **kw
    ):
    return json.dump(
        obj, fp,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
        **kw
    )

def dumps(
    obj: JsonValue,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
    **kw
    ) -> str:
    return json.dumps(
        obj,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
        **kw
    )
