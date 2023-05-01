from collections import defaultdict
from urllib.parse import unquote

from fastapi import Request


def get_tags_and_labels_by_query_params(request: Request):
    tags = defaultdict(list)
    labels = []

    for k, v in request.query_params.items():
        if k.startswith("label"):
            v = unquote(v)
            labels.append(v)
        elif k.startswith("tag_field"):
            tail = k[len("tag_field") :]
            key = f"tag_value{tail}"
            tag_value = request.query_params.get(key, None)
            if tag_value is None:
                continue

            tag_value = unquote(tag_value)
            v = unquote(v)
            tags[v].append(tag_value)
    return tags, labels
