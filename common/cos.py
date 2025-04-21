from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from project import settings

region = settings.QCLOUD_STORAGE_OPTION['Region']
secret_id = settings.QCLOUD_STORAGE_OPTION['SecretId']
secret_key = settings.QCLOUD_STORAGE_OPTION['SecretKey']
bucket = settings.QCLOUD_STORAGE_OPTION['Bucket']

cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
cos_client = CosS3Client(cos_config)