import json

import typer
from rich import print_json

from back.session.storage.async_s3 import (
    AsyncS3Session,
    delete,
    exists,
    generate_presigned_url,
    get_object,
    get_source,
    iter,
    list_all,
    list_filenames,
    put_json,
)
from lib.typer import ZetsuBouTyper

_help = """
Manipulate the S3 service.

To prevent the keys from showing in the terminal, the default value of following options
 show `None` in help section.

* --aws-access-key-id: Default value is `setting.storage_s3_aws_access_key_id`.
* --aws-secret-access-key: Default value is `setting.storage_s3_aws_secret_access_key`.
* --endpoint-url: Default value is `setting.storage_s3_endpoint_url`.

"""  # noqa

app = ZetsuBouTyper(name="s3", help=_help)


@app.command(name="generate-presigned-url")
async def _generate_presigned_url(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    object_name: str = typer.Argument(..., help="Object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.storage_s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.storage_s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.storage_s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
    expires_in: int = typer.Option(default=3600, help="Time in seconds."),
):
    async with AsyncS3Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    ) as session:
        print(
            await generate_presigned_url(
                session.client, bucket_name, object_name, expires_in=expires_in
            )
        )


@app.command(name="list")
async def _list(
    bucket_name: str = typer.Argument(default="", help="Bucket name."),
    prefix: str = typer.Argument(default="", help="Prefix, object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.storage_s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.storage_s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.storage_s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    async with AsyncS3Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    ) as session:
        resp = await list_all(session.client, bucket_name, prefix)
        print(resp)
        print(f"total: {len(resp)}")


@app.command(name="list-filenames")
async def _list_filenames(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    prefix: str = typer.Argument(..., help="Prefix, object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.storage_s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.storage_s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.storage_s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    async with AsyncS3Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    ) as session:
        resp = await list_filenames(session.client, bucket_name, prefix)
        print_json(data=resp)
        print(f"total: {len(resp)}")


@app.command()
async def get_storage_stat(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    prefix: str = typer.Argument(..., help="Prefix, object name or key."),
    depth: int = typer.Argument(..., help="Depth of path."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.storage_s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.storage_s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.storage_s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    async with AsyncS3Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    ) as session:
        source = get_source(bucket_name, prefix)
        resp = await session.get_storage_stat(source, depth)
        print(resp)


@app.command(name="list-nested-sources")
async def _list_nested_sources(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    prefix: str = typer.Argument(..., help="Prefix, object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.storage_s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.storage_s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.storage_s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    async with AsyncS3Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    ) as session:
        source = get_source(bucket_name, prefix)
        resp = await session.list_nested_sources(source)
        for s in resp:
            print(s)
        print(f"total: {len(resp)}")


@app.command(name="exists")
async def _exists(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    prefix: str = typer.Argument(..., help="Prefix, object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.storage_s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.storage_s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.storage_s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    async with AsyncS3Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    ) as session:
        resp = await exists(session.client, bucket_name, prefix)
        print(resp)


@app.command(name="get-object")
async def _get_object(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    object_name: str = typer.Argument(..., help="Prefix, object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.storage_s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.storage_s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.storage_s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    async with AsyncS3Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    ) as session:
        resp = await get_object(session.client, bucket_name, object_name)
        print(resp)


@app.command(name="put-json")
async def _put_json(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    object_name: str = typer.Argument(..., help="Prefix, object name or key."),
    json_string: str = typer.Argument(..., help="JSON string."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.storage_s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.storage_s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.storage_s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    async with AsyncS3Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    ) as session:
        data = json.loads(json_string)
        print_json(data=data)

        resp = await put_json(session.client, bucket_name, object_name, data)
        print(resp)


@app.command(name="delete")
async def _delete(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    prefix: str = typer.Argument(..., help="Prefix, object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.storage_s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.storage_s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.storage_s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    async with AsyncS3Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    ) as session:
        resp = await delete(session.client, bucket_name, prefix)
        print(resp)


@app.command(name="iter")
async def _iter(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    prefix: str = typer.Argument(..., help="Prefix, object name or key."),
    depth: int = typer.Argument(..., help="Depth of path."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.storage_s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.storage_s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.storage_s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    async with AsyncS3Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    ) as session:

        async def nested_iter():
            async for obj in iter(session.client, bucket_name, prefix, depth):
                if obj is not None:
                    yield obj

        async for obj in nested_iter():
            print(obj)
