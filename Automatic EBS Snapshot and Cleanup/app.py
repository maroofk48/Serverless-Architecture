import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = "vol-03c62b7bdd8f146ba"

def lambda_handler(event, context):

    # Create Snapshot
    response = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description=f"Automated backup of {VOLUME_ID}"
    )

    snapshot_id = response['SnapshotId']

    print(f"Created Snapshot: {snapshot_id}")

    # Calculate retention date
    retention_date = datetime.now(timezone.utc) - timedelta(days=30)

    # Find snapshots owned by current account
    snapshots = ec2.describe_snapshots(
        OwnerIds=['self']
    )['Snapshots']

    deleted_snapshots = []

    for snapshot in snapshots:

        start_time = snapshot['StartTime']

        if start_time < retention_date:

            try:
                ec2.delete_snapshot(
                    SnapshotId=snapshot['SnapshotId']
                )

                deleted_snapshots.append(
                    snapshot['SnapshotId']
                )

                print(
                    f"Deleted Snapshot: {snapshot['SnapshotId']}"
                )

            except Exception as e:

                print(
                    f"Could not delete {snapshot['SnapshotId']}: {str(e)}"
                )

    return {
        "created_snapshot": snapshot_id,
        "deleted_snapshots": deleted_snapshots
    }
