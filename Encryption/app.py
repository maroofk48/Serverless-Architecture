import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):

    s3 = boto3.client('s3')

    response = s3.list_buckets()

    unencrypted_buckets = []

    for bucket in response['Buckets']:
        bucket_name = bucket['Name']

        try:
            s3.get_bucket_encryption(Bucket=bucket_name)

        except ClientError as e:

            error_code = e.response['Error']['Code']

            if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                unencrypted_buckets.append(bucket_name)

        except Exception as e:
            print(f"Error checking {bucket_name}: {str(e)}")

    if unencrypted_buckets:
        print("Buckets without server-side encryption:")
        for bucket in unencrypted_buckets:
            print(bucket)
    else:
        print("All buckets have server-side encryption enabled.")

    return {
        "statusCode": 200,
        "unencrypted_buckets": unencrypted_buckets
    }
