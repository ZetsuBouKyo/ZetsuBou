import json
from pathlib import Path

import pytz
import typer

from back.settings import Setting, setting
from lib.typer import ZetsuBouTyper

_help = """
Manipulate the setting.
"""
app = ZetsuBouTyper(name="setting", help=_help)


@app.command()
def print_docker_envs():
    """
    Print the docker environment variables from Python code.
    """
    setting = Setting()
    env_prefix = setting.Config.env_prefix
    setting = setting.model_dump()
    keys = list(setting.keys())
    keys.sort()
    for key in keys:
        env_key = env_prefix + key
        env_key = env_key.upper()
        env_value = setting[key]
        if env_value is None:
            env_value = "null"
        env = f"{env_key}: ${{{env_key}:-{env_value}}}"
        print(env)


@app.command()
def print_setting():
    """
    Print setting in the form of JSON.
    """
    print(setting.json(indent=4))


@app.command()
def generate_timezone_options(out: str = typer.Argument(..., help="Output path.")):
    """
    Create a timezone JSON file.
    """
    out_path = Path(out)
    with out_path.open(mode="w") as fp:
        json.dump(pytz.all_timezones, fp)


@app.command()
def generate_interface(
    out: str = typer.Option(
        default="./front/src/interface/setting.ts", help="Output path."
    )
):
    """
    Generate Typescript interfaces from the Python `Setting` class.
    """
    lines = []
    schema = Setting.model_json_schema()

    title = schema.get("title", None)
    if title is None:
        return

    properties = schema.get("properties", None)
    if properties is None:
        return

    definitions = schema.get("$defs", None)
    for enum_name, enum_property in definitions.items():
        if not enum_name.endswith("Enum"):
            continue
        enums = enum_property.get("enum", None)
        if enums is None:
            e = enum_property.get("const", None)
            if e is None:
                continue
            enums = [e]

        lines.append(f"export enum {enum_name} {{")
        for e in enums:
            if type(e) is str:
                lines.append(f'  {e.title()} = "{e}",')
        lines.append("}")
        lines.append("")

    lines.append(f"export interface {title} {{")
    for property_name, property in properties.items():
        property_type = property.get("type", None)
        if property_type is None:
            axx_of = property.get("allOf", None)
            if axx_of is None:
                axx_of = property.get("anyOf", None)

            ref = None
            t = None
            for a in axx_of:
                r = a.get("$ref", None)
                if r is not None:
                    ref = r
                    break

                t = a.get("type", None)
                if t is not None and t != "null":
                    property_type = t
                    break

            if ref is not None:
                if ref is None:
                    print(property_name)
                    continue
                ref_key = Path(ref).name
                if not ref_key.endswith("Enum"):
                    continue

                property_enum = definitions.get(ref_key, None)
                if property_enum is None:
                    continue
                property_type = ref_key

        if property_type == "integer":
            property_type = "number"

        lines.append(f"  {property_name}?: {property_type};")

    lines.append("}")
    lines.append("")

    out_path = Path(out)
    with out_path.open(mode="w") as fp:
        lines_str = "\n".join(lines)
        fp.write(lines_str)
