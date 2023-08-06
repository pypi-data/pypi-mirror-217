import base64
from datetime import datetime
from typing import *  # type: ignore

import dateutil.parser

from . import caching_deserializer, case_convert
from .common import SerdeError
from .objectid_proxy import ObjectId
from .serde_json import Jsonable
from .typedefs import Jsonable

__all__ = [
    "from_json",
]


T = TypeVar("T")


class JsonDeserializer(caching_deserializer.CachingDeserializer[Jsonable]):
    def _get_class_fields_and_deserializers(
        self, value_type: Type
    ) -> Iterable[Tuple[str, str, Callable[[Jsonable, Type], Any]]]:
        for field_name_py, field_type in get_type_hints(value_type).items():
            yield (
                field_name_py,
                case_convert.all_lower_to_camel_case(field_name_py),
                field_type,
            )

    def _deserialize_bytes_from_str(
        self,
        value: Any,
        value_type: Type[str],
    ) -> bytes:
        if not isinstance(value, str):
            raise SerdeError(f"Expected bytes encoded as string, got `{value}`")

        try:
            return base64.b64decode(value.encode("utf-8"))
        except ValueError:
            raise SerdeError("Received invalid base64 encoded string.")

    def _deserialize_datetime_from_str(
        self,
        value: Any,
        value_type: Type[datetime],
    ) -> datetime:
        if not isinstance(value, str):
            raise SerdeError(f"Expected date/time string, got `{value}`")

        try:
            result = dateutil.parser.isoparse(value)
        except ValueError:
            raise SerdeError(f"Expected date/time, got `{value}`") from None

        if result.tzinfo is None:
            raise SerdeError(f"The date/time value `{value}` is missing a timezone.")

        return result

    def _deserialize_list_from_list(
        self,
        value: Any,
        value_type: Type[List],
    ) -> List[Any]:
        if not isinstance(value, list):
            raise SerdeError(f"Expected list, got `{value}`")

        subtype = get_args(value_type)[0]
        child_deserializer = self._get_deserializer(subtype)

        return [child_deserializer(self, v, subtype) for v in value]

    def _deserialize_dict_from_dict(
        self,
        value: Any,
        value_type: Type[Dict],
    ) -> Dict[Any, Any]:
        if not isinstance(value, dict):
            raise SerdeError(f"Expected dict, got `{value}`")

        subtypes = get_args(value_type)

        key_type = subtypes[0]
        key_deserializer = self._get_deserializer(key_type)

        value_type = subtypes[1]
        value_deserializer = self._get_deserializer(value_type)

        return {
            key_deserializer(self, k, key_type): value_deserializer(self, v, value_type)
            for k, v in value.items()
        }

    def _deserialize_object_id_from_str(
        self,
        value: Any,
        value_type: Type[ObjectId],
    ) -> ObjectId:
        if not isinstance(value, str):
            raise SerdeError(f"Expected ObjectId string, got `{value}`")

        try:
            result = ObjectId(value)
        except ValueError:
            raise SerdeError(f"Expected ObjectId string, got `{value}`") from None

        return result

    def _deserialize_optional(
        self,
        value: Any,
        value_type: Type,
    ) -> Any:
        if value is None:
            return None

        return self.deserialize(value, get_args(value_type)[0])

    def _deserialize_any(
        self,
        value: Any,
        value_type: Type[Any],
    ) -> Any:
        return value

    def _deserialize_literal_as_is(
        self,
        value: Any,
        value_type: Type[Any],
    ) -> str:
        options = get_args(value_type)
        if value not in options:
            raise SerdeError(f"Expected `{value_type}`, got `{value}`")

        return value

    def _deserialize_tuple_from_list(
        self,
        value: Any,
        value_type: Type[Tuple],
    ) -> Tuple[Any]:
        if not isinstance(value, list):
            raise SerdeError(f"Expected list, got `{value}`")

        subtypes = get_args(value_type)

        if len(value) != len(subtypes):
            raise SerdeError(
                f"Expected list of length {len(subtypes)}, but received one of length {len(value)}"
            )

        return tuple(
            self.deserialize(v, subtype) for v, subtype in zip(value, subtypes)
        )

    def _deserialize_set_from_list(
        self,
        value: Any,
        value_type: Type[Set],
    ) -> Set:
        if not isinstance(value, list):
            raise SerdeError(f"Expected list, got `{value}`")

        subtype = get_args(value_type)[0]

        return set(self.deserialize(v, subtype) for v in value)

    _passthrough_types = {
        bool,
        int,
        float,
        str,
    }

    _deserializer_cache = {
        bytes: _deserialize_bytes_from_str,
        datetime: _deserialize_datetime_from_str,
        list: _deserialize_list_from_list,
        dict: _deserialize_dict_from_dict,
        Union: _deserialize_optional,
        Any: _deserialize_any,
        ObjectId: _deserialize_object_id_from_str,
        Literal: _deserialize_literal_as_is,
        tuple: _deserialize_tuple_from_list,
        set: _deserialize_set_from_list,
    }

    _override_method_name = "from_json"


def from_json(
    value: Any,
    as_type: Type[T],
    *,
    custom_deserializers: Dict[Type, Callable[[Jsonable], Any]] = {},
) -> T:
    deserializer = JsonDeserializer(
        custom_deserializers={
            t: lambda v, _: cb(v) for t, cb in custom_deserializers.items()
        }
    )

    return deserializer.deserialize(value, as_type)
