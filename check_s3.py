from botocore.exceptions import ClientError
from config import settings
import boto3

s3 = boto3.client(
    "s3",
    region_name=settings.s3_region,
    aws_access_key_id=(
        settings.s3_access_key_id.get_secret_value()
        if settings.s3_access_key_id else None
    ),
    aws_secret_access_key=(
        settings.s3_secret_access_key.get_secret_value()
        if settings.s3_secret_access_key else None
    ),
    endpoint_url=settings.s3_endpoint_url,
)

try:
    response = s3.list_objects_v2(
        Bucket=settings.s3_bucket_name,
        Prefix="profile_pics/",
    )

    objects = response.get("Contents", [])

    if not objects:
        print("No profile pictures found in S3.")
    else:
        print(f"Found {len(objects)} objects:")
        for obj in objects:
            print(obj["Key"], obj["Size"], "bytes")

except ClientError as e:
    print("ERROR:", e.response["Error"]["Code"])
    print("MESSAGE:", e.response["Error"]["Message"])