from typing import Any, Dict


def get_example(*params: str, base: Dict[str, Any] = {}) -> Dict[str, Any]:
    example = {}
    for param in params:
        p = base.get(param, None)
        if p is None:
            continue
        example[param] = p

    return example
