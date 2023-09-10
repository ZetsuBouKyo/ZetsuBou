import json

from back.crud.async_gallery import elasticsearch_gallery_analyzer as gallery_analyzers
from back.crud.async_video import elasticsearch_video_analyzer as video_analyzers


def print_web_search_analyzers():
    docs = "\n"
    docs_gallery_analyzers = json.dumps(gallery_analyzers, indent=4, ensure_ascii=False)
    docs += docs_gallery_analyzers
    docs += "\n"
    docs_video_analyzers = json.dumps(video_analyzers, indent=4, ensure_ascii=False)
    docs += docs_video_analyzers
    print(docs)
