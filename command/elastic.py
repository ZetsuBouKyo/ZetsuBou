from back.session.elastic import elastic_client, init_index


class Elastic:
    """Operations for Elasticsearch in ZetsuBou."""

    def delete(self, index: str = None):
        if index is None:
            return
        if not elastic_client.ping():
            return
        if elastic_client.indices.exists(index=index):
            elastic_client.indices.delete(index=index, ignore=[400, 404])

    def list(self):
        indices = elastic_client.indices.get_alias().keys()
        for index in indices:
            print(index)

    def init(self):
        init_index()
