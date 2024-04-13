from typing import Any, Dict


def get_subset_dict(*params: str, base: Dict[str, Any] = {}) -> Dict[str, Any]:
    """
    Return a Dict[str, Any] object which is the subset of base.
    """
    example = {}
    for param in params:
        p = base.get(param, None)
        if p is None:
            continue
        example[param] = p

    return example
