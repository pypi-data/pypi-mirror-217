from datetime import datetime, timezone
from typing import *  # type: ignore

from uniserde.objectid_proxy import ObjectId

from . import caching_deserializer, case_convert, json_deserialize
from .common import SerdeError
from .typedefs import Bsonable

__all__ = [
    "from_bson",
]


T = TypeVar("T")


class BsonDeserializer(caching_deserializer.CachingDeserializer[Bsonable]):
    def _get_class_fields_and_deserializers(
        self, value_type: Type
    ) -> Iterable[Tuple[str, str, Callable[[Bsonable, Type], Any]]]:
        for field_name_py, field_type in get_type_hints(value_type).items():
            if field_name_py == "id":
                field_name_doc = "_id"
            else:
                field_name_doc = case_convert.all_lower_to_camel_case(field_name_py)

            yield (
                field_name_py,
                field_name_doc,
                field_type,
            )

    def _deserialize_datetime_from_datetime(
        self,
        value: Bsonable,
        value_type: Type[datetime],
    ) -> datetime:
        if not isinstance(value, datetime):
            raise SerdeError(f"Expected datetime, got {value}")

        # BSON doesn't support timezones, and MongoDB convention dictates UTC to
        # be assumed. Impute that.
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        return value

    _passthrough_types = {
        bool,
        int,
        float,
        bytes,
        str,
        ObjectId,
    }
    _deserializer_cache = json_deserialize.JsonDeserializer._deserializer_cache.copy()  # type: ignore
    _deserializer_cache[datetime] = _deserialize_datetime_from_datetime
    _override_method_name = "from_bson"


def from_bson(
    value: Any,
    as_type: Type[T],
    *,
    custom_deserializers: Dict[Type, Callable[[Bsonable], Any]] = {},
) -> T:
    deserializer = BsonDeserializer(
        custom_deserializers={
            t: lambda v, _: cb(v) for t, cb in custom_deserializers.items()
        }
    )

    return deserializer.deserialize(value, as_type)
