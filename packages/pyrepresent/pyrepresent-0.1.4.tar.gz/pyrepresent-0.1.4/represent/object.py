# object.py

import inspect
import builtins
import types
import six
import datetime as dt
from itertools import chain
from typing import (
    Any, Optional, Union, Iterable, Type, Dict, Tuple
)

import pandas as pd
import numpy as np

from represent.indentation import indent
from represent.structures import (
    structures, HiddenStructure, StringWrapper, colorize,
    CircularReferenceStructure, DataStructure, TypeStructure,
    ObjectStructure, FunctionStructure, SetStructure,
    ListStructure, DictStructure
)

__all__ = [
    "to_string",
    "BaseModel",
    "Modifiers",
    "unwrap",
    "DataContainer",
    "HashableDict",
    "HashableSet",
    "HashableList",
    "FrozenHashable"
]

def is_bound_method(value: Any, /) -> bool:
    """
    Checks whether an object is a bound method or not.

    :param value: The object to check.

    :return: The boolean value.
    """

    try:
        return six.get_method_self(value) is not None

    except AttributeError:
        return False
    # end try
# end is_bound_method

class DataContainer(dict):
    """A class to represent a data container."""

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Sets the attribute.

        :param key: The key to the attribute.
        :param value: The value of the attribute.
        """

        self[key] = value

        super().__setattr__(key, value)
    # end __setattr__
# end DataContainer

class Modifiers(DataContainer):
    """A class to represent the modifiers of structures."""

    def __init__(
            self, *,
            assign: Optional[bool] = None,
            excluded: Optional[Iterable[Any]] = None,
            hidden: Optional[Iterable[Any]] = None,
            protected: Optional[bool] = None,
            properties: Optional[Union[bool, Iterable[str]]] = None,
            force: Optional[bool] = None,
            legalize: Optional[bool] = None,
            defined: Optional[bool] = None
    ) -> None:
        """
        Defines the class attributes.

        :param assign: The value to assign a type name to each commands' structure.
        :param excluded: The valid_values to exclude from the commands structure.
        :param properties: The value to extract properties.
        :param protected: The value to extract protected attributes.
        :param legalize: The value to legalize the written valid_values to be strings.
        :param hidden: The valid_values of hidden keywords.
        :param force: The value to force the settings of the parsing.
        :param defined: The value to show only defined valid_values.
        """

        super().__init__()

        if assign is None:
            assign = True
        # end if

        if protected is None:
            protected = False
        # end if

        if legalize is None:
            legalize = False
        # end if

        if force is None:
            force = False
        # end if

        if defined is None:
            defined = True
        # end if

        self.assign = assign
        self.protected = protected
        self.legalize = legalize
        self.force = force
        self.defined = defined

        self.properties = properties or []
        self.excluded = list(excluded or ['modifiers'])
        self.hidden = list(hidden or [])
    # end __init__
# end Modifiers

class BaseModel:
    """A class to represent a base model."""

    modifiers = Modifiers()

    def __str__(self) -> str:
        """
        Returns a string to represent the model commands and structure.

        :return: The string representation of the model.
        """

        return to_string(self)
    # end __str__
# end BaseModel

class FrozenHashable:
    """A hashable dict structure."""

    _cache = {}

    def __hash__(self) -> int:
        """
        Returns the hash of the signature for hashing the object.

        :return: The hash of the object.
        """

        return hash(self._signature)
    # end __hash__

    def __eq__(self, other: Any) -> bool:
        """
        Checks if the signatures of the objects are the same.

        :param other: The other object to compare.

        :return: The equality value.
        """

        if type(self) is not type(other):
            return NotImplemented
        # end if

        # noinspection PyProtectedMember
        return self._signature == other._signature
    # end __eq__

    def __str__(self) -> str:
        """
        Returns a string to represent the model commands and structure.

        :return: The string representation of the model.
        """

        return f"{type(self).__name__}({super().__str__()})"
    # end __str__

    def __repr__(self) -> str:
        """
        Returns a string to represent the model commands and structure.

        :return: The string representation of the model.
        """

        return f"{type(self).__name__}({super().__repr__()})"
    # end __repr__

    @property
    def _signature(self) -> Tuple:
        """
        Returns a hashable dict signature.

        :return: The signature of the object.
        """

        raise NotImplementedError
    # end __signature

    def _immutable(self, *args: Any, **kwargs: Any) -> None:
        """
        Collects any arguments and raises an error.

        :param args: Any positional arguments.
        :param kwargs: Any keyword arguments.
        """

        raise TypeError(f"{self} is an immutable object if type {type(self)}.")
    # end __immutable

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable
# end HashableDict

class HashableDict(DictStructure, FrozenHashable, dict):
    """A hashable dict structure."""

    @property
    def _signature(self) -> Tuple[Tuple[Any, Any], ...]:
        """
        Returns a hashable dict signature.

        :return: The signature of the object.
        """

        data = [(f"--id--", id(self))]

        if id(self) in self._cache:
            return tuple(self._cache[id(self)])
        # end if

        self._cache[id(self)] = data

        for key in self:
            value = self[key]

            for base, hashable_base in hashable_matches.items():
                if isinstance(key, base) and not isinstance(key, hashable_base):
                    try:
                        hash(key)

                    except TypeError:
                        key = hashable_base(key)
                    # end try
                # end if
            # end for

            for base, hashable_base in hashable_matches.items():
                if isinstance(value, base) and not isinstance(value, hashable_base):
                    try:
                        hash(value)

                    except TypeError:
                        value = hashable_base(value)
                    # end try
                # end if
            # end for

            data.append((key, value))
        # end for

        try:
            data.sort(key=lambda v: hash(v))

        except RecursionError:
            pass
        # end try

        return tuple(self._cache[id(self)])
    # end _signature

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        content = DictStructure.__str__(self)

        if self.__type__ is None:
            return HashableDict.__name__ + "(" + content + ")"
        # end if

        return content
    # end __str__
# end HashableDict

class HashableList(ListStructure, FrozenHashable, list):
    """A hashable list structure."""

    @property
    def _signature(self) -> Tuple[Any, ...]:
        """
        Returns a hashable dict signature.

        :return: The signature of the object.
        """

        data = [("--id--", id(self))]

        if id(self) in self._cache:
            return tuple(self._cache[id(self)])
        # end if

        self._cache[id(self)] = data

        for value in self:
            for base, hashable_base in hashable_matches.items():
                if isinstance(value, base) and not isinstance(value, hashable_base):
                    try:
                        hash(value)

                    except TypeError:
                        value = hashable_base(value)
                    # end try
                # end if
            # end for

            data.append(value)
        # end for

        try:
            data.sort(key=lambda v: hash(v))

        except RecursionError:
            pass
        # end try

        return tuple(self._cache[id(self)])
    # end _signature

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        content = ListStructure.__str__(self)

        if self.__type__ is None:
            return HashableList.__name__ + "(" + content + ")"
        # end if

        return content
    # end __str__
# end HashableDict

class HashableSet(SetStructure, FrozenHashable, set):
    """A hashable list structure."""

    @property
    def _signature(self) -> Tuple[Any, ...]:
        """
        Returns a hashable dict signature.

        :return: The signature of the object.
        """

        data = [("--id--", id(self))]

        if id(self) in self._cache:
            return tuple(self._cache[id(self)])
        # end if

        self._cache[id(self)] = data

        for value in self:
            for base, hashable_base in hashable_matches.items():
                if isinstance(value, base) and not isinstance(value, hashable_base):
                    try:
                        hash(value)

                    except TypeError:
                        value = hashable_base(value)
                    # end try
                # end if
            # end for

            data.append(value)
        # end for

        try:
            data.sort(key=lambda v: hash(v))

        except RecursionError:
            pass
        # end try

        return tuple(self._cache[id(self)])
    # end _signature

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        content = SetStructure.__str__(self)

        if self.__type__ is None:
            return HashableSet.__name__ + "(" + content + ")"
        # end if

        return content
    # end __str__
# end HashableDict

hashable_matches = {
    dict: HashableDict,
    list: HashableList,
    set: HashableSet
}

def unwrap(
        data: Any, /, *,
        hidden: Optional[Union[Dict[Any, Any], Iterable[Any]]] = None,
        assign: Optional[bool] = False,
        properties: Optional[bool] = False,
        protected: Optional[bool] = False,
        legalize: Optional[bool] = False,
        force: Optional[bool] = False,
        defined: Optional[bool] = None,
        excluded: Optional[Iterable[Union[str, Type]]] = None,
        ids: Optional[Dict[int, Any]] = None
) -> Any:
    """
    Unwraps the models to get the valid_values as dictionaries.

    :param assign: The value to assign a type name to each commands' structure.
    :param data: The commands to process.
    :param ids: The ids of the collected objects.
    :param excluded: The keys to exclude from the commands structure.
    :param properties: The value to extract properties.
    :param protected: The value to extract hidden attributes.
    :param legalize: The value to legalize the written valid_values to be strings.
    :param hidden: The valid_values of hidden keywords.
    :param force: The value to force the settings of the parsing.
    :param defined: The value to show only defined valid_values.

    :return: The dictionary of unwrapped objects.
    """

    if inspect.isclass(data):
        return TypeStructure(data)
    # end if

    if (
        isinstance(data, BaseModel) and
        hasattr(data, "modifiers") and
        isinstance(data.modifiers, Modifiers) and
        ids and (not force)
    ):
        modifiers = data.modifiers

        assign = modifiers.assign
        excluded = modifiers.excluded
        properties = modifiers.properties
        protected = modifiers.protected
        hidden = modifiers.hidden
        legalize = modifiers.legalize
        defined = modifiers.defined
    # end if

    ids = ids or {}

    if (not isinstance(hidden, dict)) and (hidden is not None):
        hide = True

    elif hidden is None:
        hide = False

        hidden = ()

    else:
        hide = False
    # end if

    if (data_id := id(data)) in ids:
        return ids[data_id]

    else:
        if isinstance(data, types.FunctionType):
            ids[data_id] = repr(data) if legalize else FunctionStructure(data)

            return ids[data_id]
        # end if

        ids[data_id] = (
            data if (
                (type(data).__name__ in dir(builtins) + dir(dt)) or
                (data is None)
            )
            else (
                (
                    repr(CircularReferenceStructure(data))
                    if legalize else (
                        StringWrapper(repr(CircularReferenceStructure(data)))
                    )
                ) if (repr(data) != repr(HiddenStructure()))
                else (data if legalize else StringWrapper(repr(data)))
            )
        )
    # end if

    assignment = None

    bound = False

    if isinstance(data, (pd.DataFrame, np.ndarray)):
        return ObjectStructure(data) if not (legalize and assign) else data

    elif isinstance(data, (HiddenStructure, StringWrapper)):
        return repr(data) if legalize else StringWrapper(repr(data))

    elif (
        inspect.isfunction(data) or
        inspect.ismethod(data) or
        inspect.isclass(data) or
        isinstance(
            data, (
                bool, int, float, str, dt.time,
                dt.timedelta, dt.datetime, dt.timezone
            )
        ) or
        (bound := is_bound_method(data)) or
        data is None
    ):
        if bound and legalize:
            data = repr(data)
        # end if

        return data

    elif hasattr(data, '__dict__') or hasattr(data, "__slots__"):
        assignment = data

        data = {
            **(data.__dict__ if hasattr(data, '__dict__') else {}),
            **(
                {
                    key: getattr(data, key)
                    for key in chain.from_iterable(
                        getattr(cls, '__slots__', [])
                        for cls in type(data).__mro__
                    ) if hasattr(data, key)
                }
                if hasattr(data, '__slots__') else {}
            ),
            **(
                {
                    name: getattr(data, name) for (name, value) in
                    inspect.getmembers(
                        type(data), lambda attribute: isinstance(
                            attribute, property
                        )
                    )
                    if (
                        properties and
                        (isinstance(properties, bool) or name in properties)
                    )
                } if properties else {}
            )
        }
    # end if

    results = None

    if isinstance(data, dict):
        results = {}

        for key, value in data.items():
            if (
                (
                    isinstance(key, str) and
                    (
                        (not key.startswith("_")) or
                        (assignment is None) or
                        protected
                    )
                ) or (not isinstance(key, str))
            ):
                try:
                    if isinstance(value, int):
                        bool_value = True

                    else:
                        bool_value = bool(value)
                    # end try

                except ValueError:
                    bool_value = True
                # end try

                if (
                    (
                        (excluded is not None) and
                        ((key in excluded) or (type(value) in excluded))
                    ) or
                    (
                        defined and
                        (not (isinstance(value, bool) or bool_value))
                    )
                ):
                    continue
                # end if

                if (
                    (hidden is not None) and
                    (key in hidden) and
                    (assignment is not None)
                ):
                    if not hide:
                        value = hidden[key]

                    else:
                        value = HiddenStructure()
                    # end if
                # end if

                base = type(key)

                key = unwrap(
                    key, assign=assign, ids=ids, excluded=excluded,
                    properties=properties, protected=protected,
                    hidden=hidden, legalize=legalize, force=force,
                    defined=defined
                )
                # end if

                if isinstance(key, dict):
                    try:
                        {key: None}

                    except TypeError:
                        key = HashableDict(key)
                        key.__type__ = base
                    # end try
                # end if

                results[key] = unwrap(
                    value, assign=assign, ids=ids, excluded=excluded,
                    properties=properties, protected=protected,
                    hidden=hidden, legalize=legalize, force=force,
                    defined=defined
                )
            # end if
        # end for

    elif isinstance(data, (tuple, list, set)):
        results = []

        for value in data:
            results.append(
                unwrap(
                    value, assign=assign, ids=ids, excluded=excluded,
                    properties=properties, protected=protected,
                    hidden=hidden, legalize=legalize, force=force,
                    defined=defined
                )
            )
        # end for

        results = type(data)(results)
    # end if

    if assign and (results is not None):
        results = structures[type(results)](results)
        results.__type__ = (
            type(assignment) if (assignment is not None) else None
        )

        if not legalize:
            results.__value__ = (
                assignment if (assignment is not None) else None
            )
        # end if
    # end if

    ids[data_id] = results

    return results
# end unwrap

def to_string(obj: Any, /, modifiers: Optional[Modifiers] = None) -> str:
    """
    Returns a string to represent the model commands and structure.

    :return: The string representation of the model.
    """

    if modifiers is None:
        if (
            isinstance(obj, BaseModel) and
            hasattr(obj, "modifiers") and
            isinstance(obj.modifiers, Modifiers)
        ):
            modifiers = obj.modifiers

        else:
            modifiers = Modifiers()
        # end if
    # end if

    data = indent(str(unwrap(obj, **modifiers)))

    if DataStructure.color:
        data = colorize(data)
    # end if

    return data
# end to_string