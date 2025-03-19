import boto3
import csv

def list_ec2_instances_with_public_ip():
    # EC2クライアントの作成
    ec2_client = boto3.client('ec2')

    # インスタンスの情報を取得
    response = ec2_client.describe_instances()

    # CSVファイルの作成
    with open('ec2_instances.csv', 'w', newline='') as csvfile:
        fieldnames = ['Instance ID', 'Name', 'Public IP', 'Owner', 'Service']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                public_ip = instance.get('PublicIpAddress', 'Null')

                # タグの初期値
                name = 'Null'
                owner = 'Null'
                service = 'Null'

                if 'Tags' in instance:
                    tags = {tag['Key']: tag['Value'] for tag in instance['Tags']}
                    name = tags.get('Name', 'Null')
                    owner = tags.get('Owner', 'Null')
                    service = tags.get('Service', 'Null')

                writer.writerow({
                    'Instance ID': instance_id,
                    'Name': name,
                    'Public IP': public_ip,
                    'Owner': owner,
                    'Service': service
                })

if __name__ == "__main__":
    list_ec2_instances_with_public_ip()