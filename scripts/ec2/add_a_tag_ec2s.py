import boto3

# このスクリプトは、すべてのEC2インスタンスに特定のタグを付与します。
# すでにそのタグキーを持っている場合は変更を加えず、タグキーが存在しない場合はタグを付与します。
# タグが無く新規に付与する場合、タグの値は 'null' に設定されます。
# This script adds a specific tag to all EC2 instances.
# If the tag key already exists, no changes are made.
# If the tag key does not exist, it adds the tag with the value set to 'null'.

def tag_instance(instance_id, tag_key, tag_value):
    ec2 = boto3.client('ec2')
    # 既存のタグを取得
    tags = ec2.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [instance_id]}, {'Name': 'key', 'Values': [tag_key]}])
    if not tags['Tags']:
        # タグが存在しない場合、新しいタグを作成
        ec2.create_tags(Resources=[instance_id], Tags=[{'Key': tag_key, 'Value': tag_value}])

def main():
    ec2 = boto3.client('ec2')
    # すべてのインスタンスを取得
    response = ec2.describe_instances()
    instances = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]

    # 各インスタンスにタグを付与
    tag_key = 'YourTagKey'
    tag_value = 'null'
    for instance_id in instances:
        tag_instance(instance_id, tag_key, tag_value)

    print("タグ付与が完了しました。")

if __name__ == "__main__":
    main()