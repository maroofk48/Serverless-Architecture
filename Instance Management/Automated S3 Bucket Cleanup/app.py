import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'my-cleanup-bucket123'


def lambda_handler(event, context):

    # Calculate cutoff date (30 days ago)
    cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=5)

    response = s3.list_objects_v2(Bucket='my-cleanup-bucket123')

    if 'Contents' not in response:
        print("Bucket is empty.")
        return

    for obj in response['Contents']:

        object_key = obj['Key']
        last_modified = obj['LastModified']

        if last_modified < cutoff_date:

            s3.delete_object(
                Bucket='my-cleanup-bucket123',
                Key=object_key
            )

            print(f"Deleted: {object_key}")

    return {
        'statusCode': 200,
        'body': 'Cleanup completed successfully.'
    }
