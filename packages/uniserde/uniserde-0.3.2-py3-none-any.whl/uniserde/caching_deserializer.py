import enum
import inspect
from abc import ABC, abstractmethod
from typing import *  # type: ignore

from typing_extensions import Self

import uniserde

from . import case_convert, common, serde_class
from .common import SerdeError

T = TypeVar("T")
V = TypeVar("V")


class CachingDeserializer(ABC, Generic[T]):
    _passthrough_types: Set[Type]
    _deserializer_cache: Dict[Type, Callable[[Self, T, Type], Any]]
    _override_method_name: str

    def __init_subclass__(cls) -> None:
        def make_deserializer_from_passthrough_type(
            passthrough_type: Type,
        ) -> Callable[[Self, T, Type], Any]:
            def result(self, value: T, as_type: Type[V]) -> V:
                if not isinstance(value, as_type) and not (
                    isinstance(value, int) and as_type is float
                ):
                    raise SerdeError(f"Expected `{as_type}`, got `{value}`")

                return value  # type: ignore

            return result

        for typ in cls._passthrough_types:
            cls._deserializer_cache[typ] = make_deserializer_from_passthrough_type(typ)

    def __init__(
        self,
        *,
        custom_deserializers: Dict[Type, Callable[[T, Type], Any]] = {},
    ):
        self._custom_deserializers = custom_deserializers

    @abstractmethod
    def _get_class_fields_and_deserializers(
        self, value_type: Type
    ) -> Iterable[Tuple[str, str, Callable[[T, Type], Any]]]:
        """
        Return a list of (python_name, json_name, deserializer) tuples for each
        field in the class.
        """
        raise NotImplementedError()

    def deserialize(self, value: T, as_type: Type[V]) -> V:
        # Special case: passthrough types for performance
        if as_type in self._passthrough_types:
            if not isinstance(value, as_type) and not (
                isinstance(value, int) and as_type is float
            ):
                raise SerdeError(f"Expected `{as_type}`, got `{value}`")

            return value  # type: ignore

        # Otherwise get a deserializer and use it
        deserializer = self._get_deserializer(as_type)
        return deserializer(self, value, as_type)

    def _get_deserializer(
        self,
        value_type: Type,
    ) -> Callable[[Self, T, Type], Any]:
        # Prepare the key for the deserializer lookup
        key = get_origin(value_type)
        if key is None:
            key = value_type

        # Custom deserializers take precedence
        try:
            custom_callback = self._custom_deserializers[key]
        except KeyError:
            pass
        else:
            return lambda self, value, as_type: custom_callback(value, as_type)

        # Use a cached deserializer if possible
        try:
            return self._deserializer_cache[key]
        except KeyError:
            pass

        # Otherwise create the appropriate deserializer and cache it for next
        # time
        assert inspect.isclass(value_type), value_type
        deserializer = self._create_class_deserializer(value_type)
        self._deserializer_cache[key] = deserializer

        return deserializer

    def _create_class_deserializer(
        self,
        value_type: Type,
    ) -> Callable[[Self, T, Type], Any]:
        # Case: The class has a custom deserialization method
        try:
            override_method = getattr(value_type, self._override_method_name)
        except AttributeError:
            pass
        else:
            serde_class_method = getattr(serde_class.Serde, self._override_method_name)

            if override_method.__func__ is not serde_class_method.__func__:
                return lambda self, value, _type: override_method(value, {})

        # Case: Enum
        if issubclass(value_type, enum.Enum):

            def deserialize_enum(self, value, _type):
                if not isinstance(value, str):
                    raise SerdeError(f"Expected enumeration string, got `{value}`")

                try:
                    py_name = case_convert.camel_case_to_all_upper(
                        value
                    )  # ValueError if not camel case
                    return value_type[py_name]  # ValueError if not in enum
                except KeyError:
                    raise SerdeError(f"Invalid enumeration value `{value}`") from None

            return deserialize_enum

        # Case: Base which is serialized `@as_child`
        if common.should_serialize_as_child(value_type):
            # Prepare a set of all possible classes
            child_classes_and_deserializers_by_doc_name = {
                case_convert.upper_camel_case_to_camel_case(cls.__name__): (
                    cls,
                    self._create_fieldwise_class_deserializer(cls),
                )
                for cls in common.all_subclasses(value_type, True)
            }

            def deserialize_as_child(self, value, _type):
                # Look up the real type
                try:
                    type_tag = value.pop("type")
                except KeyError:
                    raise SerdeError(f"Object is missing the `type` field") from None

                # Get the class
                try:
                    (
                        child_class,
                        child_class_deserializer,
                    ) = child_classes_and_deserializers_by_doc_name[type_tag]
                except KeyError:
                    raise SerdeError(
                        f"Encountered invalid type tag `{type_tag}`"
                    ) from None

                # Delegate to that class's deserializer
                return child_class_deserializer(self, value, child_class)

            return deserialize_as_child

        # Case: Regular old class
        return self._create_fieldwise_class_deserializer(value_type)

    def _create_fieldwise_class_deserializer(
        self, value_type: Type
    ) -> Callable[[Self, T, Type], Any]:
        deserializer = FieldwiseClassDeserializer()

        for py_name, doc_name, field_type in self._get_class_fields_and_deserializers(
            value_type
        ):
            deserializer.add_field(
                py_name,
                doc_name,
                field_type,
                self._get_deserializer(field_type),
            )

        return deserializer


class FieldwiseClassDeserializer:
    fields: List[Tuple[str, str, Type, Callable[[CachingDeserializer, Any, Type], Any]]]

    def __init__(self):
        self.fields = []

    def add_field(
        self,
        python_name: str,
        doc_name: str,
        field_type: Type,
        deserializer: Callable[[CachingDeserializer, Any, Type], Any],
    ):
        self.fields.append((python_name, doc_name, field_type, deserializer))

    def __call__(
        self,
        calling_deserializer: CachingDeserializer,
        raw: Any,
        value_type: Type,
    ) -> Any:
        # Make sure the raw value is a dict
        if not isinstance(raw, dict):
            raise uniserde.SerdeError(f"Expected object, got `{raw!r}`")

        # Create an instance of the class
        result = object.__new__(value_type)
        result_dict = vars(result)

        # Deserialize all fields
        for py_name, doc_name, field_type, deserializer in self.fields:
            # Get the raw value
            try:
                raw_value = raw.pop(doc_name)
            except KeyError:
                raise uniserde.SerdeError(f"Missing field `{doc_name!r}`") from None

            # Deserialize it
            parsed_value = deserializer(calling_deserializer, raw_value, field_type)

            # Store it
            result_dict[py_name] = parsed_value

        # Make sure there are no stray fields
        if len(raw) > 0:
            raise SerdeError(
                f"Superfluous object fields `{'`, `'.join(map(str, raw.keys()))}`"
            )

        return result
