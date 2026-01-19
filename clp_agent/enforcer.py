import boto3

# 🚨 SAFETY SWITCH — DO NOT TURN OFF YET
DRY_RUN = False

ec2 = boto3.client("ec2")


def enforce_death_contract(resource_id, death_contract):
    print("[DEATH CONTRACT]")

    if death_contract == "TERMINATE":
        if DRY_RUN:
            print(f"[DRY RUN] Would terminate EC2 {resource_id}")
        else:
            ec2.terminate_instances(InstanceIds=[resource_id])
            print(f"EC2 {resource_id} terminated.")

    elif death_contract == "SNAPSHOT_TERMINATE":
        if DRY_RUN:
            print(f"[DRY RUN] Would snapshot and terminate EC2 {resource_id}")
        else:
            print("Creating snapshot...")
            volumes = ec2.describe_instances(
                InstanceIds=[resource_id]
            )["Reservations"][0]["Instances"][0]["BlockDeviceMappings"]

            for v in volumes:
                volume_id = v["Ebs"]["VolumeId"]
                ec2.create_snapshot(
                    VolumeId=volume_id,
                    Description=f"CLP snapshot for {resource_id}"
                )

            ec2.terminate_instances(InstanceIds=[resource_id])
            print(f"EC2 {resource_id} snapshotted and terminated.")

    elif death_contract == "ARCHIVE":
        print(f"[DRY RUN] Would archive resource {resource_id}")

    else:
        print(f"Unknown death contract for {resource_id}")
