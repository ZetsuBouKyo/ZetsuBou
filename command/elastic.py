import typer
from back.model.elastic import AnalyzerEnum
from back.session.elastic import elastic_client, init_index
from rich import print_json

_help = """
Manipulate the Elasticsearch.
"""
app = typer.Typer(name="elastic", help=_help)


@app.command()
def delete(index: str = typer.Option(default=None, help="The name of the index.")):
    """
    Delete the index.
    """

    if index is None:
        return
    if not elastic_client.ping():
        return
    if elastic_client.indices.exists(index=index):
        elastic_client.indices.delete(index=index, ignore=[400, 404])


@app.command()
def list_indices():
    """
    List the indices.
    """

    indices = elastic_client.indices.get_alias().keys()
    for index in indices:
        print(index)


@app.command()
def init():
    """
    Initialize the indices if the index does not exist.
    """

    init_index()


@app.command()
def analyze(
    text: str = typer.Argument(..., help="Text for analyzing."),
    analyzer: AnalyzerEnum = typer.Option(
        default=AnalyzerEnum.DEFAULT.value, help="Analyzer name."
    ),
):
    """
    Analyze the text string and return the resulting tokens.
    """
    print(f"analyzer: {analyzer}")
    print(f"text: {text}")
    body = {"text": text, "analyzer": analyzer}
    resp = elastic_client.indices.analyze(body=body)
    print_json(data=resp)
