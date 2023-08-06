# object.py

import inspect
import builtins
import types
import six
from dataclasses import dataclass, field
import datetime as dt
from itertools import chain
from typing import (
    Any, Optional, Union, Iterable, Type, Dict
)

import pandas as pd
import numpy as np

from represent.indentation import indent
from represent.colors import colorize
from represent.structures import (
    structures, HiddenStructure, StringWrapper,
    CircularReferenceStructure, TypeStructure,
    ObjectStructure, FunctionStructure, hashable_structures
)

__all__ = [
    "to_string",
    "BaseModel",
    "Modifiers",
    "unwrap"
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

@dataclass(kw_only=True, repr=False, slots=True)
class Modifiers(dict):
    """A class to represent the modifiers of structures."""

    assign: bool = True
    protected: bool = False
    force: bool = False
    legalize: bool = False
    defined: bool = True
    color: bool = True

    excluded: Iterable[Any] = field(default_factory=lambda: ['modifiers'])
    hidden: Iterable[Any] = field(default_factory=lambda: [])
    properties: Union[bool, Iterable[str]] = field(default_factory=lambda: [])

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Sets the attribute.

        :param key: The key to the attribute.
        :param value: The value of the attribute.
        """

        self[key] = value

        object.__setattr__(self, key, value)
    # end __setattr__
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

def extract_attributes(data: Any, /) -> Dict[str, Any]:
    """
    Gets all attributes of an object.

    :param data: The object.

    :return: The attributes of the object.
    """

    return {
        **(data.__dict__ if hasattr(data, '__dict__') else {}),
        **(
            {
                key: getattr(data, key)
                for key in chain.from_iterable(
                    getattr(cls, '__slots__', [])
                    for cls in type(data).__mro__
                ) if hasattr(data, key)
            } if hasattr(data, '__slots__') else {}
        )
    }
# end extract_attributes

def extract_properties(
        data: Any, /, properties: Optional[Iterable[str]] = None
) -> Dict[str, Any]:
    """
    Gets all properties of an object.

    :param data: The object.
    :param properties: The properties to extract.

    :return: The properties of the object.
    """

    return {
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
    }
# end extract_properties

def extract_data(
        data: Any, /, properties: Optional[Iterable[str]] = None
) -> Dict[str, Any]:
    """
    Gets all attributes and properties of an object.

    :param data: The object.
    :param properties: The properties to extract.

    :return: The properties of the object.
    """

    return {
        **extract_attributes(data),
        **(
            extract_properties(data)
            if properties else {}
        )
    }
# end extract_data

def is_protected(
        key: Any,
        assignment: Optional[Any] = None,
        protected: Optional[bool] = None
) -> bool:
    """
    Checks if a key should be allowed.

    :param key: The key to validate.
    :param assignment: The value for the key.
    :param protected: The protected values.

    :return: The validation value.
    """

    return not (
        (
            isinstance(key, str) and
            (
                (not key.startswith("_")) or
                (assignment is None) or
                protected
            )
        ) or (not isinstance(key, str))
    )
# end is_protected

def is_excluded(
        key: Any,
        value: Any,
        excluded: Optional[Iterable[Any]] = None,
        defined: Optional[bool] = None
) -> bool:
    """
    Checks if a key should be allowed.

    :param key: The key to validate.
    :param value: The value for the key.
    :param excluded: The excluded values.
    :param defined: The value to show only defined valid_values.

    :return: The validation value.
    """

    try:
        if isinstance(value, int):
            bool_value = True

        else:
            bool_value = bool(value)
        # end try

    except ValueError:
        bool_value = True
        # end try

    return (
        (
            (excluded is not None) and
            ((key in excluded) or (type(value) in excluded))
        ) or
        (
            defined and
            (not (isinstance(value, bool) or bool_value))
        )
    )
# end is_excluded

def is_hidden(
        key: Any,
        assignment: Optional[Any] = None,
        hidden: Optional[Union[Dict[Any, Any], Iterable[Any]]] = None
) -> bool:
    """
    Checks if the value of the key should be hidden.

    :param key: The key object.
    :param assignment: The assignment value of the object.
    :param hidden: The hidden values.

    :return: The boolean flag.
    """

    return (
        (hidden is not None) and
        (key in hidden) and
        (assignment is not None)
    )
# end is_hidden

def hidden_value(
        key: Any,
        hide: Optional[bool] = None,
        hidden: Optional[Union[Dict[Any, Any], Iterable[Any]]] = None
) -> Any:
    """
    Returns the hidden value for the given value.

    :param key: The key object.
    :param hide: The value to hide the object.
    :param hidden: The hidden values.

    :return: The hidden value.
    """

    if not hide:
        return hidden[key]

    else:
        return HiddenStructure()
    # end if
# end hidden_value

def early_cache(
        data: Any, /, *, ids: Dict[int, Any], legalize: Optional[bool] = False
) -> None:
    """
    Caches the object data early in the ids.

    :param data: The object.
    :param ids: The ids cache dictionary.
    :param legalize: The value to legalize the output.
    """
    data_id = id(data)

    if isinstance(data, types.FunctionType):
        ids[data_id] = repr(data) if legalize else FunctionStructure(data)

        return ids[data_id]
        # end if

    if (
        (type(data).__name__ in dir(builtins) + dir(dt)) or
        (data is None)
    ):
        ids[data_id] = data

    elif repr(data) != repr(HiddenStructure()):
        ids[data_id] = (
            repr(CircularReferenceStructure(data))
            if legalize else
            StringWrapper(repr(CircularReferenceStructure(data)))
        )

    else:
        ids[data_id] = (data if legalize else StringWrapper(repr(data)))
    # end if
# end early_cache

def unwrap(
        data: Any, /, *,
        assign: Optional[bool] = False,
        protected: Optional[bool] = False,
        legalize: Optional[bool] = False,
        force: Optional[bool] = False,
        defined: Optional[bool] = None,
        color: Optional[bool] = None,
        properties: Optional[Union[bool, Iterable[str]]] = False,
        hidden: Optional[Union[Dict[Any, Any], Iterable[Any]]] = None,
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
    :param color: The valur to color the object.
    :param legalize: The value to legalize the written valid_values to be strings.
    :param hidden: The valid_values of hidden keywords.
    :param force: The value to force the settings of the parsing.
    :param defined: The value to show only defined valid_values.

    :return: The dictionary of unwrapped objects.
    """

    if inspect.isclass(data):
        return TypeStructure(data)
    # end if

    if isinstance(
        data, (
            bool, int, float, str, dt.time,
            dt.timedelta, dt.datetime, dt.timezone
        )
    ):
        return data
    # end if

    if (
        (hasattr(data, "modifiers") or hasattr(type(data), "modifiers")) and
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
        color = modifiers.color
    # end if

    if (
        inspect.isfunction(data) or
        inspect.ismethod(data)
    ):
        if is_bound_method(data) and legalize:
            return repr(data)
        # end if

        return FunctionStructure(data)
    # end if

    if isinstance(data, (pd.DataFrame, np.ndarray)):
        return ObjectStructure(data) if not (legalize and assign) else data
    # end if

    if isinstance(data, (HiddenStructure, StringWrapper)):
        return repr(data) if legalize else StringWrapper(repr(data))
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
        early_cache(data, ids=ids, legalize=legalize)
    # end if

    assignment = None

    if hasattr(data, '__dict__') or hasattr(data, "__slots__"):
        assignment = data

        data = extract_data(data, properties=properties)
    # end if

    results = None

    if isinstance(data, dict):
        results = {}

        for key, value in data.items():
            if (
                is_protected(key=key, protected=protected, assignment=assignment) or
                is_excluded(key=key, value=value, excluded=excluded, defined=defined)
            ):
                continue
            # end if

            if is_hidden(key=key, assignment=assignment, hidden=hidden):
                value = hidden_value(key=key, hide=hide, hidden=hidden)
            # end if

            key = unwrap(
                key, assign=assign, ids=ids, excluded=excluded,
                properties=properties, protected=protected,
                hidden=hidden, legalize=legalize, force=force,
                defined=defined, color=color
            )
            # end if

            results[key] = unwrap(
                value, assign=assign, ids=ids, excluded=excluded,
                properties=properties, protected=protected,
                hidden=hidden, legalize=legalize, force=force,
                defined=defined, color=color
            )
        # end for

    elif isinstance(data, (tuple, list, set)):
        results = []

        for value in data:
            results.append(
                unwrap(
                    value, assign=assign, ids=ids, excluded=excluded,
                    properties=properties, protected=protected,
                    hidden=hidden, legalize=legalize, force=force,
                    defined=defined, color=color
                )
            )
        # end for

        results = type(data)(results)
    # end if

    if assign and (results is not None):
        if type(results) in hashable_structures:
            results = hashable_structures[type(results)](results)

        else:
            results = structures[type(results)](results)
        # end if

        if assignment is not None:
            results.__type__ = assignment

            if not legalize:
                results.__value__ = assignment
            # end if
        # end if

        results.__color__ = color
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

    if modifiers.color:
        data = colorize(data)
    # end if

    return data
# end to_string