from collections import defaultdict
from typing import Any, Generic, List, Optional, TypeVar, Union

_KT = TypeVar("_KT")  # Key type.
_VT = TypeVar("_VT")  # Value type.


class OneToOneMap:
    """
    Restructure a list of dict to a one-to-one dict.
    """

    def __init__(self, data: List[dict], key_name: str, value_name: str):
        self.raw_data = data
        self._key_to_value = {}
        self._value_to_key = {}
        for d in data:
            key = d.get(key_name, None)
            value = d.get(value_name, None)
            if self._key_to_value.get(key, None) is not None:
                raise ValueError("The mapping of the data should be 1:1")
            if self._value_to_key.get(value, None) is not None:
                raise ValueError("The mapping of the data should be 1:1")
            self._key_to_value[key] = value
            self._value_to_key[value] = key

    def get_value(self, key: Any) -> Optional[Any]:
        return self._key_to_value.get(key, None)

    def get_key(self, value: Any) -> Optional[Any]:
        return self._value_to_key.get(value, None)


class BiDict(dict, Generic[_KT, _VT]):
    def __setitem__(self, key: Union[_KT, _VT], value: Union[_KT, _VT]):
        if key == value:
            raise ValueError(f"key: {key} and value: {value} should not be the same.")

        if key is None or value is None:
            raise ValueError(f"key or value should not be None.")

        if key in self and value in self:
            return

        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __getitem__(self, key: Union[_KT, _VT]) -> Union[_KT, _VT, None]:
        try:
            value = dict.__getitem__(self, key)
            return value
        except KeyError:
            return None

    def __delitem__(self, key: Union[_KT, _VT]):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self) -> int:
        return dict.__len__(self) // 2
