from typing import Any, List, Optional


class OneToOneMap:
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
