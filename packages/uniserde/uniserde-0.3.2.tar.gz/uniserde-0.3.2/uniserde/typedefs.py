from datetime import datetime
from typing import *  # type: ignore

from .objectid_proxy import ObjectId

__all__ = [
    "Jsonable",
    "Bsonable",
]


Jsonable = Union[
    None,
    bool,
    int,
    float,
    str,
    Dict[str, "Jsonable"],
    List["Jsonable"],
    Tuple["Jsonable", ...],
]


Bsonable = Union[
    None,
    bool,
    int,
    float,
    str,
    Dict[str, "Bsonable"],
    List["Bsonable"],
    Tuple["Bsonable", ...],
    bytes,
    ObjectId,
    datetime,
]
