import json

import typer
from back.crud.s3 import CrudS3
from rich import print_json

from command.utils import sync

_help = """
Manipulate the S3 service.

To prevent the keys from showing in the terminal, the default value of following options
 show `None` in help section.

* --aws-access-key-id: Default value is `setting.s3_aws_access_key_id`.
* --aws-secret-access-key: Default value is `setting.s3_aws_secret_access_key`.
* --endpoint-url: Default value is `setting.s3_endpoint_url`.

"""  # noqa

app = typer.Typer(name="s3", help=_help)


@app.command()
@sync
async def generate_presigned_url(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    object_name: str = typer.Argument(..., help="Object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
    expires_in: int = typer.Option(default=3600, help="Time in seconds."),
):
    crud = CrudS3(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    )
    print(
        await crud.generate_presigned_url(
            bucket_name, object_name, expires_in=expires_in
        )
    )


@app.command()
@sync
async def list(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    prefix: str = typer.Argument(..., help="Prefix, object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    crud = CrudS3(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    )
    resp = await crud.list(bucket_name, prefix)
    print(resp)
    print(f"total: {len(resp)}")


@app.command()
@sync
async def exists(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    prefix: str = typer.Argument(..., help="Prefix, object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    crud = CrudS3(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    )
    resp = await crud.exists(bucket_name, prefix)
    print(resp)


@app.command()
@sync
async def get_object(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    object_name: str = typer.Argument(..., help="Prefix, object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    crud = CrudS3(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    )

    resp = await crud.get_object(bucket_name, object_name)
    print(resp)


@app.command()
@sync
async def put_json(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    object_name: str = typer.Argument(..., help="Prefix, object name or key."),
    json_string: str = typer.Argument(..., help="JSON string."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    crud = CrudS3(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    )

    data = json.loads(json_string)
    print_json(data=data)

    resp = await crud.put_json(bucket_name, object_name, data)
    print(resp)


@app.command()
@sync
async def delete(
    bucket_name: str = typer.Argument(..., help="Bucket name."),
    prefix: str = typer.Argument(..., help="Prefix, object name or key."),
    aws_access_key_id: str = typer.Option(
        default=None,
        help="AWS access key id or MinIO user name. Default value is `setting.s3_aws_access_key_id`.",  # noqa
    ),
    aws_secret_access_key: str = typer.Option(
        default=None,
        help="AWS secret access key or MinIO user password. Default value is `setting.s3_aws_secret_access_key`.",  # noqa
    ),
    endpoint_url: str = typer.Option(
        default=None,
        help="Endpoint url. Default value is `setting.s3_endpoint_url`.",
    ),
    region_name: str = typer.Option(
        default="ap-northeast-1-tpe-1", help="Region name."
    ),
):
    crud = CrudS3(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
        is_from_setting_if_none=True,
    )

    resp = await crud.delete(bucket_name, prefix)
    print(resp)
