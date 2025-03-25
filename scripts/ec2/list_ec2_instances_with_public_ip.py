import boto3
import csv
import argparse
def list_ec2_instances_with_public_ip(output_format):
    # EC2クライアントの作成
    ec2_client = boto3.client('ec2')
    # インスタンスの情報を取得
    response = ec2_client.describe_instances()
    fieldnames = ['Instance ID', 'Name', 'Service', 'Public IP', 'Owner', ] 
    if output_format == 'csv':
        # CSVファイルの作成
        with open('ec2_instances.csv', 'w', newline='') as csvfile:
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
    elif output_format == 'stdout':
        # 標準出力に出力
        print(f"{'Instance ID':<20} {'Name':<20} {'Public IP':<20} {'Owner':<20} {'Service':<20}")
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
                print(f"{instance_id:<20} {name:<20} {public_ip:<20} {owner:<20} {service:<20}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List EC2 instances with public IP addresses.')
    parser.add_argument('--output', choices=['csv', 'stdout'], default='stdout', help='Output format: csv or stdout')
    args = parser.parse_args()
    list_ec2_instances_with_public_ip(args.output)