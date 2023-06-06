import json
import time
from pathlib import Path

import typer
from back.crud.async_tag import CrudTag
from back.db.crud import CrudTagAttribute, CrudTagToken
from back.db.model import TagAttributeCreate, TagTokenCreate
from back.model.tag import TagInsert
from tqdm import tqdm

from command.utils import sync


def load_json(fpath: Path):
    with fpath.open(mode="r") as fp:
        data = json.load(fp)
    return data


_help = """
Manipulate the tag.
"""
app = typer.Typer(name="tag", help=_help)


@app.command()
@sync
async def dump(
    out: str = typer.Argument(..., help="The repository for the output JSON files."),
    force: bool = typer.Option(default=False, help="Overwrite the output JSON files."),
):
    """
    Dump the tag into JSON file.
    """

    out = Path(out)
    if not out.is_dir():
        return

    tags_path = out / "tag.json"
    if not force and tags_path.exists():
        return

    attrs_path = out / "attribute.json"
    if not force and attrs_path.exists():
        return

    async def get_attributes():
        print("get tag attributes ...")
        attrs = []
        skip = 0
        limit = 100
        rows = await CrudTagAttribute.get_rows_order_by_id(skip=skip, limit=limit)
        while rows:
            for row in tqdm(rows):
                attrs.append(row.dict())
            skip += limit
            rows = await CrudTagAttribute.get_rows_order_by_id(skip=skip, limit=limit)
        return attrs

    attrs = await get_attributes()
    with attrs_path.open(mode="w") as fp:
        json.dump(attrs, fp, indent=4, ensure_ascii=False)

    async def get_tags():
        print("get tags ...")
        crud = CrudTag()
        tags = []
        skip = 0
        limit = 100
        rows = await CrudTagToken.get_rows_order_by_id(skip=skip, limit=limit)
        while rows:
            for row in tqdm(rows):
                tag = await crud.get_interpretation_by_id(row.id)
                tags.append(tag.dict())
            skip += limit
            rows = await CrudTagToken.get_rows_order_by_id(skip=skip, limit=limit)
        return tags

    tags = await get_tags()
    with tags_path.open(mode="w") as fp:
        json.dump(tags, fp, indent=4, ensure_ascii=False)


@app.command()
@sync
async def load(
    attr: str = typer.Argument(..., help="The JSON file of the attributes."),
    tag: str = typer.Argument(..., help="The JSON file of the tags."),
):
    """
    Load the tag into JSON file.
    """

    async def is_ok():
        rows = await CrudTagToken.get_rows_order_by_id()
        if len(rows) > 0:
            return False
        return True

    async def insert_attr(attr_table, attr_data):
        print("insert tag attributes ...")
        for attr in tqdm(attr_data):
            name = attr["name"]
            row = await CrudTagAttribute.get_row_by_name(name)
            if row is None:
                row = await CrudTagAttribute.create(TagAttributeCreate(name=name))
            attr_table[name] = row.id

    async def insert_token(token_table, tag_data):
        print("insert tag tokens ...")
        for tag in tqdm(tag_data):
            id = tag["id"]
            name = tag["name"]
            row = await CrudTagToken.create(TagTokenCreate(name=name))
            token_table[id] = row.id

    def get_inserted_tag(token_table, attr_table, tag: dict):
        id = token_table[tag["id"]]
        name = tag["name"]
        category_ids = [token_table[c["id"]] for c in tag["categories"]]
        synonym_ids = [token_table[s["id"]] for s in tag["synonyms"]]
        attributes = {attr_table[a["name"]]: a["value"] for a in tag["attributes"]}

        return TagInsert(
            id=id,
            name=name,
            category_ids=category_ids,
            synonym_ids=synonym_ids,
            attributes=attributes,
        )

    async def insert_tag(crud: CrudTag, token_table, attr_table, tag_data):
        print("insert tags ...")
        for tag in tqdm(tag_data):
            inserted_tag = get_inserted_tag(token_table, attr_table, tag)
            await crud.insert(inserted_tag)

    attr = Path(attr)
    if not attr.exists():
        return

    tag = Path(tag)
    if not tag.exists():
        return

    ok = await is_ok()
    if not ok:
        print("TagToken table is not empty.")
        return

    attr_table = {}
    attr_data = load_json(attr)
    token_table = {}
    tag_data = load_json(tag)

    await insert_attr(attr_table, attr_data)
    print(f"tag attributes: {attr_table}")

    t1 = time.time()
    await insert_token(token_table, tag_data)
    t2 = time.time()
    crud = CrudTag()
    await insert_tag(crud, token_table, attr_table, tag_data)
    t3 = time.time()

    print(f"insert tag: {t2-t1} seconds")
    print(f"insert tag: {t3-t2} seconds")
