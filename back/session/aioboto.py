from aiobotocore.session import AioSession, ClientCreatorContext


class S3Session(AioSession):
    def __init__(
        self,
        session_vars=None,
        event_hooks=None,
        include_builtin_handlers=True,
        profile=None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        endpoint_url: str = None,
        region_name: str = None,
    ):
        super().__init__(session_vars, event_hooks, include_builtin_handlers, profile)
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.region_name = region_name

    def create_s3_client(self):
        return ClientCreatorContext(
            self._create_client(
                "s3",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                endpoint_url=self.endpoint_url,
                region_name=self.region_name,
            )
        )
