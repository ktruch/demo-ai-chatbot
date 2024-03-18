import os
import boto3
from pydantic_settings import BaseSettings
from atlassian import Confluence
import os
from dotenv import load_dotenv
load_dotenv()

page_id = 0000000

class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    app_name: str = "Demo app"
    AWS_KEY: str
    AWS_SECRET: str
    AWS_S3_BUCKET: str = "pdf-basic-app"

    @staticmethod
    def get_s3_client():
        return boto3.client(
            's3',
            aws_access_key_id=Settings().AWS_KEY,
            aws_secret_access_key=Settings().AWS_SECRET
        )
    
    @staticmethod
    def get_confluence_client():
        confluence = Confluence(
            url='https://my.site',
            username = os.environ('CONFLUENCE_USERNAME'),
            password = os.environ('CONFLUENCE_PASS'),
            verify_ssl = False
            )
        # page_html = confluence.get_page_by_id(page_id, "space,body.view,version,container")
        page_html = confluence.get_page_by_id(page_id, expand='body.storage')
        return print(page_html['body']['view']['value'])

    class Config:
        env_file = ".env"
        extra = "ignore"
