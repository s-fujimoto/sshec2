import pytest
import datetime
from dateutil.tz import tzutc
from ec2ssh import ec2ssh

instances_data = [
    {'AmiLaunchIndex': 0,
        'Architecture': 'x86_64',
        'BlockDeviceMappings': [{'DeviceName': '/dev/xvda',
            'Ebs': {'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 22, tzinfo=tzutc()),
            'DeleteOnTermination': True,
            'Status': 'attached',
            'VolumeId': 'vol-000000000000'}}],
        'ClientToken': 'xxxxxxxxxxxxx',
        'EbsOptimized': False,
        'EnaSupport': True,
        'Hypervisor': 'xen',
        'IamInstanceProfile': {'Arn': 'arn:aws:iam::xxxxxxxxxx:instance-profile/xxxxxxxxxxxx',
        'Id': 'xxxxxxxxxxxxxx'},
        'ImageId': 'ami-2443b745',
        'InstanceId': 'i-000000000000',
        'InstanceType': 't2.nano',
        'KeyName': 'keypair0',
        'LaunchTime': datetime.datetime(2017, 3, 16, 3, 37, 33, tzinfo=tzutc()),
        'Monitoring': {'State': 'disabled'},
        'NetworkInterfaces': [{'Association': {'IpOwnerId': 'xxxxxxxxx',
            'PublicDnsName': 'ec2-0-0-0-0.ap-northeast-1.compute.amazonaws.com',
            'PublicIp': '0.0.0.0'},
            'Attachment': {'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 21, tzinfo=tzutc()),
            'AttachmentId': 'eni-attach-00000000',
            'DeleteOnTermination': True,
            'DeviceIndex': 0,
            'Status': 'attached'},
            'Description': 'Primary network interface',
            'Groups': [{'GroupId': 'sg-xxxxxxx', 'GroupName': 'default'},
            {'GroupId': 'sg-xxxxxxxxx', 'GroupName': 'ssh'}],
            'Ipv6Addresses': [],
            'MacAddress': 'xx:xx:xx:xx:xx:xx',
            'NetworkInterfaceId': 'eni-xxxxxxxxx',
            'OwnerId': 'xxxxxxxxxx',
            'PrivateDnsName': 'ip-192-168-0-0.ap-northeast-1.compute.internal',
            'PrivateIpAddress': '192.168.0.0',
            'PrivateIpAddresses': [{'Association': {'IpOwnerId': 'xxxxxxxxx',
            'PublicDnsName': 'ec2-0-0-0-0.ap-northeast-1.compute.amazonaws.com',
            'PublicIp': '0.0.0.0'},
            'Primary': True,
            'PrivateDnsName': 'ip-192-168-0-0.ap-northeast-1.compute.internal',
            'PrivateIpAddress': '192.168.0.0'}],
            'SourceDestCheck': False,
            'Status': 'in-use',
            'SubnetId': 'subnet-xxxxxxxx',
            'VpcId': 'vpc-xxxxxxx'}],
        'Placement': {'AvailabilityZone': 'ap-northeast-1a',
        'GroupName': '',
        'Tenancy': 'default'},
        'PrivateDnsName': 'ip-192-168-0-0.ap-northeast-1.compute.internal',
        'PrivateIpAddress': '192.168.0.0',
        'ProductCodes': [],
        'PublicDnsName': 'ec2-0-0-0-0.ap-northeast-1.compute.amazonaws.com',
        'PublicIpAddress': '0.0.0.0',
        'RootDeviceName': '/dev/xvda',
        'RootDeviceType': 'ebs',
        'SecurityGroups': [{'GroupId': 'sg-xxxxxxxx', 'GroupName': 'default'},
        {'GroupId': 'sg-xxxxxxx', 'GroupName': 'ssh'}],
        'SourceDestCheck': False,
        'State': {'Code': 16, 'Name': 'running'},
        'StateTransitionReason': '',
        'SubnetId': 'subnet-xxxxxxxxx',
        'Tags': [{'Key': 'KEY1', 'Value': 'VALUE1'},
        {'Key': 'Name', 'Value': 'INSTANCE000'}],
        'VirtualizationType': 'hvm',
        'VpcId': 'vpc-xxxxxxxxx'
    },
    {'AmiLaunchIndex': 0,
        'Architecture': 'x86_64',
        'BlockDeviceMappings': [{'DeviceName': '/dev/xvda',
            'Ebs': {'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 22, tzinfo=tzutc()),
            'DeleteOnTermination': True,
            'Status': 'attached',
            'VolumeId': 'vol-000000000000'}}],
        'ClientToken': 'xxxxxxxxxxxxx',
        'EbsOptimized': False,
        'EnaSupport': True,
        'Hypervisor': 'xen',
        'IamInstanceProfile': {'Arn': 'arn:aws:iam::xxxxxxxxxx:instance-profile/xxxxxxxxxxxx',
        'Id': 'xxxxxxxxxxxxxx'},
        'ImageId': 'ami-2443b745',
        'InstanceId': 'i-111111111111',
        'InstanceType': 't2.nano',
        'KeyName': 'keypair1',
        'LaunchTime': datetime.datetime(2017, 3, 16, 3, 37, 33, tzinfo=tzutc()),
        'Monitoring': {'State': 'disabled'},
        'NetworkInterfaces': [{'Association': {'IpOwnerId': 'xxxxxxxxx',
            'PublicDnsName': 'ec2-1-1-1-1.ap-northeast-1.compute.amazonaws.com',
            'PublicIp': '1.1.1.1'},
            'Attachment': {'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 21, tzinfo=tzutc()),
            'AttachmentId': 'eni-attach-00000000',
            'DeleteOnTermination': True,
            'DeviceIndex': 0,
            'Status': 'attached'},
            'Description': 'Primary network interface',
            'Groups': [{'GroupId': 'sg-xxxxxxx', 'GroupName': 'default'},
            {'GroupId': 'sg-xxxxxxxxx', 'GroupName': 'ssh'}],
            'Ipv6Addresses': [],
            'MacAddress': 'xx:xx:xx:xx:xx:xx',
            'NetworkInterfaceId': 'eni-xxxxxxxxx',
            'OwnerId': 'xxxxxxxxxx',
            'PrivateDnsName': 'ip-192-168-1-1.ap-northeast-1.compute.internal',
            'PrivateIpAddress': '192.168.1.1',
            'PrivateIpAddresses': [{'Association': {'IpOwnerId': 'xxxxxxxxx',
            'PublicDnsName': 'ec2-1-1-1-1.ap-northeast-1.compute.amazonaws.com',
            'PublicIp': '1.1.1.1'},
            'Primary': True,
            'PrivateDnsName': 'ip-192-168-1-1.ap-northeast-1.compute.internal',
            'PrivateIpAddress': '192.168.1.1'}],
            'SourceDestCheck': False,
            'Status': 'in-use',
            'SubnetId': 'subnet-xxxxxxxx',
            'VpcId': 'vpc-xxxxxxx'}],
        'Placement': {'AvailabilityZone': 'ap-northeast-1a',
        'GroupName': '',
        'Tenancy': 'default'},
        'PrivateDnsName': 'ip-192-168-1-1.ap-northeast-1.compute.internal',
        'PrivateIpAddress': '192.168.1.1',
        'ProductCodes': [],
        'PublicDnsName': 'ec2-1-1-1-1.ap-northeast-1.compute.amazonaws.com',
        'PublicIpAddress': '1.1.1.1',
        'RootDeviceName': '/dev/xvda',
        'RootDeviceType': 'ebs',
        'SecurityGroups': [{'GroupId': 'sg-xxxxxxxx', 'GroupName': 'default'},
        {'GroupId': 'sg-xxxxxxx', 'GroupName': 'ssh'}],
        'SourceDestCheck': False,
        'State': {'Code': 16, 'Name': 'running'},
        'StateTransitionReason': '',
        'SubnetId': 'subnet-xxxxxxxxx',
        'Tags': [{'Key': 'KEY1', 'Value': 'VALUE1'},
        {'Key': 'Name', 'Value': 'INSTANCE001'}],
        'VirtualizationType': 'hvm',
        'VpcId': 'vpc-xxxxxxxxx'
    },
    {'AmiLaunchIndex': 0,
        'Architecture': 'x86_64',
        'BlockDeviceMappings': [{'DeviceName': '/dev/xvda',
            'Ebs': {'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 22, tzinfo=tzutc()),
            'DeleteOnTermination': True,
            'Status': 'attached',
            'VolumeId': 'vol-000000000000'}}],
        'ClientToken': 'xxxxxxxxxxxxx',
        'EbsOptimized': False,
        'EnaSupport': True,
        'Hypervisor': 'xen',
        'IamInstanceProfile': {'Arn': 'arn:aws:iam::xxxxxxxxxx:instance-profile/xxxxxxxxxxxx',
        'Id': 'xxxxxxxxxxxxxx'},
        'ImageId': 'ami-2443b745',
        'InstanceId': 'i-000000000000',
        'InstanceType': 't2.nano',
        'KeyName': 'keypair2',
        'LaunchTime': datetime.datetime(2017, 3, 16, 3, 37, 33, tzinfo=tzutc()),
        'Monitoring': {'State': 'disabled'},
        'NetworkInterfaces': [{'Association': {'IpOwnerId': 'xxxxxxxxx',
            'PublicDnsName': 'ec2-2-2-2-2.ap-northeast-1.compute.amazonaws.com',
            'PublicIp': '2.2.2.2'},
            'Attachment': {'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 21, tzinfo=tzutc()),
            'AttachmentId': 'eni-attach-00000000',
            'DeleteOnTermination': True,
            'DeviceIndex': 0,
            'Status': 'attached'},
            'Description': 'Primary network interface',
            'Groups': [{'GroupId': 'sg-xxxxxxx', 'GroupName': 'default'},
            {'GroupId': 'sg-xxxxxxxxx', 'GroupName': 'ssh'}],
            'Ipv6Addresses': [],
            'MacAddress': 'xx:xx:xx:xx:xx:xx',
            'NetworkInterfaceId': 'eni-xxxxxxxxx',
            'OwnerId': 'xxxxxxxxxx',
            'PrivateDnsName': 'ip-192-168-2-2.ap-northeast-1.compute.internal',
            'PrivateIpAddress': '192.168.2.2',
            'PrivateIpAddresses': [{'Association': {'IpOwnerId': 'xxxxxxxxx',
            'PublicDnsName': 'ec2-2-2-2-2.ap-northeast-1.compute.amazonaws.com',
            'PublicIp': '2.2.2.2'},
            'Primary': True,
            'PrivateDnsName': 'ip-192-168-2-2.ap-northeast-1.compute.internal',
            'PrivateIpAddress': '192.168.2.2'}],
            'SourceDestCheck': False,
            'Status': 'in-use',
            'SubnetId': 'subnet-xxxxxxxx',
            'VpcId': 'vpc-xxxxxxx'}],
        'Placement': {'AvailabilityZone': 'ap-northeast-1a',
        'GroupName': '',
        'Tenancy': 'default'},
        'PrivateDnsName': 'ip-192-168-2-2.ap-northeast-1.compute.internal',
        'PrivateIpAddress': '192.168.2.2',
        'ProductCodes': [],
        'PublicDnsName': 'ec2-2-2-2-2.ap-northeast-1.compute.amazonaws.com',
        'PublicIpAddress': '2.2.2.2',
        'RootDeviceName': '/dev/xvda',
        'RootDeviceType': 'ebs',
        'SecurityGroups': [{'GroupId': 'sg-xxxxxxxx', 'GroupName': 'default'},
        {'GroupId': 'sg-xxxxxxx', 'GroupName': 'ssh'}],
        'SourceDestCheck': False,
        'State': {'Code': 16, 'Name': 'running'},
        'StateTransitionReason': '',
        'SubnetId': 'subnet-xxxxxxxxx',
        'Tags': [{'Key': 'KEY1', 'Value': 'VALUE1'},
        {'Key': 'Name', 'Value': 'INSTANCE002'}],
        'VirtualizationType': 'hvm',
        'VpcId': 'vpc-xxxxxxxxx'
    },
]

@pytest.mark.parametrize("instance,expected", [(i, 'INSTANCE00'+str(num)) for num, i in enumerate(instances_data)])
def test_get_instance_name(instance, expected):
    assert ec2ssh.get_instance_name(instance) == expected

validate_data = [
    (instances_data, 0, True),
    (instances_data, 1, True),
    (instances_data, 2, True),
    (instances_data, -1, False),
    (instances_data, 3, False),
    (instances_data, 4, False),
]

@pytest.mark.parametrize("instances,number,expected", validate_data)
def test_validate_input(instances, number, expected):
    assert ec2ssh.validate_input(instances, number) == expected

setting_bastion_data = [
    (instances_data, 'INSTANCE000', False, '0.0.0.0'),
    (instances_data, 'INSTANCE001', False, '1.1.1.1'),
]

@pytest.mark.parametrize("instances,bastion_name,bastion,expected", setting_bastion_data)
def test_setting_bastion(instances, bastion_name, bastion, expected):
    bastion = ec2ssh.setting_bastion(instances, bastion_name, bastion)
    assert bastion['PublicIpAddress'] == expected

get_key_path_data = [
    (instances_data[0], None, '~/.ssh/keypair0.pem'),
    (instances_data[1], '~/.ssh/aaaaaa.pem', '~/.ssh/aaaaaa.pem'),
]

@pytest.mark.parametrize("instance,key_path,expected", get_key_path_data)
def test_get_key_path(instance, key_path, expected):
    assert ec2ssh.get_key_path(instance, key_path) == expected

get_username_data = [
    (instances_data[0], None, 'ec2-user'),
    (instances_data[1], 'root', 'root'),
]

@pytest.mark.parametrize("instance,username,expected", get_username_data)
def test_get_username(instance, username, expected):
    assert ec2ssh.get_username(instance, username) == expected

get_host_data = [
    (instances_data[2], True, '2.2.2.2'),
    (instances_data[0], False, '192.168.0.0'),
]

@pytest.mark.parametrize("instance,public,expected", get_host_data)
def test_get_host(instance, public, expected):
    assert ec2ssh.get_host(instance, public) == expected

target_command_data = [
    (instances_data[1], None, None, True, '-i ~/.ssh/keypair1.pem ec2-user@1.1.1.1'),
    (instances_data[2], '~/.ssh/test.pem', None, True, '-i ~/.ssh/test.pem ec2-user@2.2.2.2'),
    (instances_data[0], None, 'test', True, '-i ~/.ssh/keypair0.pem test@0.0.0.0'),
    (instances_data[1], None, None, False, '-i ~/.ssh/keypair1.pem ec2-user@192.168.1.1'),
]

@pytest.mark.parametrize("instance,key_path,username,public,expected", target_command_data)
def test_target_command(instance, key_path, username, public, expected):
    assert ec2ssh.target_command(instance, key_path, username, public) == expected

bastion_commands_data = [
    (instances_data[0], None, None, ['-o', 'ProxyCommand="ssh -W %h:%p -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0"']),
    (instances_data[1], '~/.ssh/test.pem', None, ['-o', 'ProxyCommand="ssh -W %h:%p -i ~/.ssh/test.pem ec2-user@1.1.1.1"']),
    (instances_data[2], None, 'test', ['-o', 'ProxyCommand="ssh -W %h:%p -i ~/.ssh/keypair2.pem test@2.2.2.2"']),
    (instances_data[0], None, None, ['-o', 'ProxyCommand="ssh -W %h:%p -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0"']),
]

@pytest.mark.parametrize("instance,key_path,username,expected", bastion_commands_data)
def test_bastion_commands(instance, key_path, username, expected):
    assert ec2ssh.bastion_commands(instance, key_path, username) == expected

generate_scp_command_data = [
    (instances_data[0], None, None, None, None, None, 'from.txt', '/to/', True, False, 'scp -r -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0:from.txt /to/'),
    (instances_data[1], '~/.ssh/test.pem', None, None, None, None, 'from.txt', '/to/', True, False, 'scp -r -i ~/.ssh/test.pem ec2-user@1.1.1.1:from.txt /to/'),
    (instances_data[2], None, 'test', None, None, None, 'from.txt', '/to/', True, False, 'scp -r -i ~/.ssh/keypair2.pem test@2.2.2.2:from.txt /to/'),
    (instances_data[0], None, None, instances_data[1], None, None, 'from.txt', '/to/', True, False, 'scp -r -o ProxyCommand="ssh -W %h:%p -i ~/.ssh/keypair1.pem ec2-user@1.1.1.1" -i ~/.ssh/keypair0.pem ec2-user@192.168.0.0:from.txt /to/'),
]

@pytest.mark.parametrize("instance,key_path,username,bastion_instance,bastion_key_path,bastion_username,src_path,dst_path,scp_from,scp_to,expected", generate_scp_command_data)
def test_generate_scp_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username, src_path, dst_path, scp_from, scp_to, expected):
    assert ec2ssh.generate_scp_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username, src_path, dst_path, scp_from, scp_to) == expected

generate_ssh_command_data = [
    (instances_data[0], None, None, None, None, None, 'ssh -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0'),
    (instances_data[1], '~/.ssh/test.pem', None, None, None, None, 'ssh -i ~/.ssh/test.pem ec2-user@1.1.1.1'),
    (instances_data[2], None, 'test', None, None, None, 'ssh -i ~/.ssh/keypair2.pem test@2.2.2.2'),
    (instances_data[0], None, None, instances_data[1], None, None, 'ssh -o ProxyCommand="ssh -W %h:%p -i ~/.ssh/keypair1.pem ec2-user@1.1.1.1" -i ~/.ssh/keypair0.pem ec2-user@192.168.0.0'),
]

@pytest.mark.parametrize("instance,key_path,username,bastion_instance,bastion_key_path,bastion_username,expected", generate_ssh_command_data)
def test_generate_ssh_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username, expected):
    assert ec2ssh.generate_ssh_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username) == expected
