import datetime
from argparse import Namespace

import mock
import pytest
from dateutil.tz import tzutc

from sshec2 import sshec2

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


instances_data = [
    {
        'AmiLaunchIndex': 0,
        'Architecture': 'x86_64',
        'BlockDeviceMappings': [{
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 22, tzinfo=tzutc()),
                'DeleteOnTermination': True,
                'Status': 'attached',
                'VolumeId': 'vol-000000000000'}}],
        'ClientToken': 'xxxxxxxxxxxxx',
        'EbsOptimized': False,
        'EnaSupport': True,
        'Hypervisor': 'xen',
        'IamInstanceProfile': {
            'Arn': 'arn:aws:iam::xxxxxxxxxx:instance-profile/xxxxxxxxxxxx',
            'Id': 'xxxxxxxxxxxxxx'},
        'ImageId': 'ami-2443b745',
        'InstanceId': 'i-000000000000',
        'InstanceType': 't2.nano',
        'KeyName': 'keypair0',
        'LaunchTime': datetime.datetime(2017, 3, 16, 3, 37, 33, tzinfo=tzutc()),
        'Monitoring': {'State': 'disabled'},
        'NetworkInterfaces': [{
            'Association': {
                'IpOwnerId': 'xxxxxxxxx',
                'PublicDnsName': 'ec2-0-0-0-0.ap-northeast-1.compute.amazonaws.com',
                'PublicIp': '0.0.0.0'},
            'Attachment': {
                'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 21, tzinfo=tzutc()),
                'AttachmentId': 'eni-attach-00000000',
                'DeleteOnTermination': True,
                'DeviceIndex': 0,
                'Status': 'attached'},
            'Description': 'Primary network interface',
            'Groups': [
                {'GroupId': 'sg-xxxxxxx', 'GroupName': 'default'},
                {'GroupId': 'sg-xxxxxxxxx', 'GroupName': 'ssh'}],
            'Ipv6Addresses': [],
            'MacAddress': 'xx:xx:xx:xx:xx:xx',
            'NetworkInterfaceId': 'eni-xxxxxxxxx',
            'OwnerId': 'xxxxxxxxxx',
            'PrivateDnsName': 'ip-192-168-0-0.ap-northeast-1.compute.internal',
            'PrivateIpAddress': '192.168.0.0',
            'PrivateIpAddresses': [{
                'Association': {
                    'IpOwnerId': 'xxxxxxxxx',
                    'PublicDnsName': 'ec2-0-0-0-0.ap-northeast-1.compute.amazonaws.com',
                    'PublicIp': '0.0.0.0'},
                'Primary': True,
                'PrivateDnsName': 'ip-192-168-0-0.ap-northeast-1.compute.internal',
                'PrivateIpAddress': '192.168.0.0'}],
            'SourceDestCheck': False,
            'Status': 'in-use',
            'SubnetId': 'subnet-xxxxxxxx',
            'VpcId': 'vpc-xxxxxxx'}],
        'Placement': {
            'AvailabilityZone': 'ap-northeast-1a',
            'GroupName': '',
            'Tenancy': 'default'},
        'PrivateDnsName': 'ip-192-168-0-0.ap-northeast-1.compute.internal',
        'PrivateIpAddress': '192.168.0.0',
        'ProductCodes': [],
        'PublicDnsName': 'ec2-0-0-0-0.ap-northeast-1.compute.amazonaws.com',
        'PublicIpAddress': '0.0.0.0',
        'RootDeviceName': '/dev/xvda',
        'RootDeviceType': 'ebs',
        'SecurityGroups': [
            {'GroupId': 'sg-xxxxxxxx', 'GroupName': 'default'},
            {'GroupId': 'sg-xxxxxxx', 'GroupName': 'ssh'}],
        'SourceDestCheck': False,
        'State': {'Code': 16, 'Name': 'running'},
        'StateTransitionReason': '',
        'SubnetId': 'subnet-xxxxxxxxx',
        'Tags': [
            {'Key': 'KEY1', 'Value': 'VALUE1'},
            {'Key': 'Name', 'Value': 'INSTANCE000'}],
        'VirtualizationType': 'hvm',
        'VpcId': 'vpc-xxxxxxxxx'
    },
    {
        'AmiLaunchIndex': 0,
        'Architecture': 'x86_64',
        'BlockDeviceMappings': [{
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 22, tzinfo=tzutc()),
                'DeleteOnTermination': True,
                'Status': 'attached',
                'VolumeId': 'vol-000000000000'}}],
        'ClientToken': 'xxxxxxxxxxxxx',
        'EbsOptimized': False,
        'EnaSupport': True,
        'Hypervisor': 'xen',
        'IamInstanceProfile': {
            'Arn': 'arn:aws:iam::xxxxxxxxxx:instance-profile/xxxxxxxxxxxx',
            'Id': 'xxxxxxxxxxxxxx'},
        'ImageId': 'ami-2443b745',
        'InstanceId': 'i-111111111111',
        'InstanceType': 't2.nano',
        'KeyName': 'keypair1',
        'LaunchTime': datetime.datetime(2017, 3, 16, 3, 37, 33, tzinfo=tzutc()),
        'Monitoring': {'State': 'disabled'},
        'NetworkInterfaces': [{
            'Association': {
                'IpOwnerId': 'xxxxxxxxx',
                'PublicDnsName': 'ec2-1-1-1-1.ap-northeast-1.compute.amazonaws.com',
                'PublicIp': '1.1.1.1'},
            'Attachment': {
                'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 21, tzinfo=tzutc()),
                'AttachmentId': 'eni-attach-00000000',
                'DeleteOnTermination': True,
                'DeviceIndex': 0,
                'Status': 'attached'},
            'Description': 'Primary network interface',
            'Groups': [
                {'GroupId': 'sg-xxxxxxx', 'GroupName': 'default'},
                {'GroupId': 'sg-xxxxxxxxx', 'GroupName': 'ssh'}],
            'Ipv6Addresses': [],
            'MacAddress': 'xx:xx:xx:xx:xx:xx',
            'NetworkInterfaceId': 'eni-xxxxxxxxx',
            'OwnerId': 'xxxxxxxxxx',
            'PrivateDnsName': 'ip-192-168-1-1.ap-northeast-1.compute.internal',
            'PrivateIpAddress': '192.168.1.1',
            'PrivateIpAddresses': [{
                'Association': {
                    'IpOwnerId': 'xxxxxxxxx',
                    'PublicDnsName': 'ec2-1-1-1-1.ap-northeast-1.compute.amazonaws.com',
                    'PublicIp': '1.1.1.1'},
                'Primary': True,
                'PrivateDnsName': 'ip-192-168-1-1.ap-northeast-1.compute.internal',
                'PrivateIpAddress': '192.168.1.1'}],
            'SourceDestCheck': False,
            'Status': 'in-use',
            'SubnetId': 'subnet-xxxxxxxx',
            'VpcId': 'vpc-xxxxxxx'}],
        'Placement': {
            'AvailabilityZone': 'ap-northeast-1a',
            'GroupName': '',
            'Tenancy': 'default'},
        'PrivateDnsName': 'ip-192-168-1-1.ap-northeast-1.compute.internal',
        'PrivateIpAddress': '192.168.1.1',
        'ProductCodes': [],
        'PublicDnsName': 'ec2-1-1-1-1.ap-northeast-1.compute.amazonaws.com',
        'PublicIpAddress': '1.1.1.1',
        'RootDeviceName': '/dev/xvda',
        'RootDeviceType': 'ebs',
        'SecurityGroups': [
            {'GroupId': 'sg-xxxxxxxx', 'GroupName': 'default'},
            {'GroupId': 'sg-xxxxxxx', 'GroupName': 'ssh'}],
        'SourceDestCheck': False,
        'State': {'Code': 16, 'Name': 'running'},
        'StateTransitionReason': '',
        'SubnetId': 'subnet-xxxxxxxxx',
        'Tags': [
            {'Key': 'KEY1', 'Value': 'VALUE1'},
            {'Key': 'Name', 'Value': 'INSTANCE001'}],
        'VirtualizationType': 'hvm',
        'VpcId': 'vpc-xxxxxxxxx'
    },
    {
        'AmiLaunchIndex': 0,
        'Architecture': 'x86_64',
        'BlockDeviceMappings': [{
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 22, tzinfo=tzutc()),
                'DeleteOnTermination': True,
                'Status': 'attached',
                'VolumeId': 'vol-000000000000'}}],
        'ClientToken': 'xxxxxxxxxxxxx',
        'EbsOptimized': False,
        'EnaSupport': True,
        'Hypervisor': 'xen',
        'IamInstanceProfile': {
            'Arn': 'arn:aws:iam::xxxxxxxxxx:instance-profile/xxxxxxxxxxxx',
            'Id': 'xxxxxxxxxxxxxx'},
        'ImageId': 'ami-2443b745',
        'InstanceId': 'i-000000000000',
        'InstanceType': 't2.nano',
        'KeyName': 'keypair2',
        'LaunchTime': datetime.datetime(2017, 3, 16, 3, 37, 33, tzinfo=tzutc()),
        'Monitoring': {'State': 'disabled'},
        'NetworkInterfaces': [{
            'Association': {
                'IpOwnerId': 'xxxxxxxxx',
                'PublicDnsName': 'ec2-2-2-2-2.ap-northeast-1.compute.amazonaws.com',
                'PublicIp': '2.2.2.2'},
            'Attachment': {
                'AttachTime': datetime.datetime(2016, 8, 29, 13, 39, 21, tzinfo=tzutc()),
                'AttachmentId': 'eni-attach-00000000',
                'DeleteOnTermination': True,
                'DeviceIndex': 0,
                'Status': 'attached'},
            'Description': 'Primary network interface',
            'Groups': [
                {'GroupId': 'sg-xxxxxxx', 'GroupName': 'default'},
                {'GroupId': 'sg-xxxxxxxxx', 'GroupName': 'ssh'}],
            'Ipv6Addresses': [],
            'MacAddress': 'xx:xx:xx:xx:xx:xx',
            'NetworkInterfaceId': 'eni-xxxxxxxxx',
            'OwnerId': 'xxxxxxxxxx',
            'PrivateDnsName': 'ip-192-168-2-2.ap-northeast-1.compute.internal',
            'PrivateIpAddress': '192.168.2.2',
            'PrivateIpAddresses': [{
                'Association': {
                    'IpOwnerId': 'xxxxxxxxx',
                    'PublicDnsName': 'ec2-2-2-2-2.ap-northeast-1.compute.amazonaws.com',
                    'PublicIp': '2.2.2.2'},
                'Primary': True,
                'PrivateDnsName': 'ip-192-168-2-2.ap-northeast-1.compute.internal',
                'PrivateIpAddress': '192.168.2.2'}],
            'SourceDestCheck': False,
            'Status': 'in-use',
            'SubnetId': 'subnet-xxxxxxxx',
            'VpcId': 'vpc-xxxxxxx'}],
        'Placement': {
            'AvailabilityZone': 'ap-northeast-1a',
            'GroupName': '',
            'Tenancy': 'default'},
        'PrivateDnsName': 'ip-192-168-2-2.ap-northeast-1.compute.internal',
        'PrivateIpAddress': '192.168.2.2',
        'ProductCodes': [],
        'PublicDnsName': 'ec2-2-2-2-2.ap-northeast-1.compute.amazonaws.com',
        'PublicIpAddress': '2.2.2.2',
        'RootDeviceName': '/dev/xvda',
        'RootDeviceType': 'ebs',
        'SecurityGroups': [
            {'GroupId': 'sg-xxxxxxxx', 'GroupName': 'default'},
            {'GroupId': 'sg-xxxxxxx', 'GroupName': 'ssh'}],
        'SourceDestCheck': False,
        'State': {'Code': 16, 'Name': 'running'},
        'StateTransitionReason': '',
        'SubnetId': 'subnet-xxxxxxxxx',
        'Tags': [
            {'Key': 'KEY1', 'Value': 'VALUE1'},
            {'Key': 'Name', 'Value': 'INSTANCE002'}],
        'VirtualizationType': 'hvm',
        'VpcId': 'vpc-xxxxxxxxx'
    }
]


@pytest.mark.parametrize("instance,expected", [(i, 'INSTANCE00' + str(num)) for num, i in enumerate(instances_data)])
def test_get_instance_name(instance, expected):
    assert sshec2.get_instance_name(instance) == expected


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
    assert sshec2.validate_input(instances, number) == expected


setting_bastion_data = [
    (instances_data, 'INSTANCE000', '0.0.0.0'),
    (instances_data, 'INSTANCE001', '1.1.1.1'),
]


@pytest.mark.parametrize("instances,bastion_name,expected", setting_bastion_data)
def test_setting_bastion(instances, bastion_name, expected):
    bastion = sshec2.setting_bastion(instances, bastion_name)
    assert bastion['PublicIpAddress'] == expected


get_key_path_data = [
    (instances_data[0], None, '~/.ssh/keypair0.pem'),
    (instances_data[1], '~/.ssh/aaaaaa.pem', '~/.ssh/aaaaaa.pem'),
]


@pytest.mark.parametrize("instance,key_path,expected", get_key_path_data)
def test_get_key_path(instance, key_path, expected):
    assert sshec2.get_key_path(instance, key_path) == expected


get_username_data = [
    (None, 'ec2-user'),
    ('root', 'root'),
]


@pytest.mark.parametrize("username,expected", get_username_data)
def test_get_username(username, expected):
    assert sshec2.get_username(username) == expected


get_host_data = [
    (instances_data[2], True, '2.2.2.2'),
    (instances_data[0], False, '192.168.0.0'),
]


@pytest.mark.parametrize("instance,public,expected", get_host_data)
def test_get_host(instance, public, expected):
    assert sshec2.get_host(instance, public) == expected


target_command_data = [
    (instances_data[1], None, None, True, '-i ~/.ssh/keypair1.pem ec2-user@1.1.1.1'),
    (instances_data[2], '~/.ssh/test.pem', None, True, '-i ~/.ssh/test.pem ec2-user@2.2.2.2'),
    (instances_data[0], None, 'test', True, '-i ~/.ssh/keypair0.pem test@0.0.0.0'),
    (instances_data[1], None, None, False, '-i ~/.ssh/keypair1.pem ec2-user@192.168.1.1'),
]


@pytest.mark.parametrize("instance,key_path,username,public,expected", target_command_data)
def test_target_command(instance, key_path, username, public, expected):
    assert sshec2.target_command(instance, key_path, username, public) == expected


bastion_commands_data = [
    (instances_data[0], None, None, ['-o', 'ProxyCommand="ssh -W %h:%p -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0"']),
    (instances_data[1], '~/.ssh/test.pem', None, ['-o', 'ProxyCommand="ssh -W %h:%p -i ~/.ssh/test.pem ec2-user@1.1.1.1"']),
    (instances_data[2], None, 'test', ['-o', 'ProxyCommand="ssh -W %h:%p -i ~/.ssh/keypair2.pem test@2.2.2.2"']),
    (instances_data[0], None, None, ['-o', 'ProxyCommand="ssh -W %h:%p -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0"']),
]


@pytest.mark.parametrize("instance,key_path,username,expected", bastion_commands_data)
def test_bastion_commands(instance, key_path, username, expected):
    assert sshec2.bastion_commands(instance, key_path, username) == expected


generate_scp_command_data = [
    (instances_data[0], None, None, None, None, None, 'from.txt', '/to/', True, False, 'scp -r -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0:from.txt /to/'),
    (instances_data[1], '~/.ssh/test.pem', None, None, None, None, 'from.txt', '/to/', True, False, 'scp -r -i ~/.ssh/test.pem ec2-user@1.1.1.1:from.txt /to/'),
    (instances_data[2], None, 'test', None, None, None, 'from.txt', '/to/', True, False, 'scp -r -i ~/.ssh/keypair2.pem test@2.2.2.2:from.txt /to/'),
    (instances_data[0], None, None, instances_data[1], None, None, 'from.txt', '/to/', True, False, 'scp -r -o ProxyCommand="ssh -W %h:%p -i ~/.ssh/keypair1.pem ec2-user@1.1.1.1" -i ~/.ssh/keypair0.pem ec2-user@192.168.0.0:from.txt /to/'),
]


@pytest.mark.parametrize("instance,key_path,username,bastion_instance,bastion_key_path,bastion_username,src_path,dst_path,scp_from,scp_to,expected", generate_scp_command_data)
def test_generate_scp_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username, src_path, dst_path, scp_from, scp_to, expected):
    assert sshec2.generate_scp_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username, src_path, dst_path, scp_from, scp_to) == expected


generate_ssh_command_data = [
    (instances_data[0], None, None, None, None, None, 'ssh -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0'),
    (instances_data[1], '~/.ssh/test.pem', None, None, None, None, 'ssh -i ~/.ssh/test.pem ec2-user@1.1.1.1'),
    (instances_data[2], None, 'test', None, None, None, 'ssh -i ~/.ssh/keypair2.pem test@2.2.2.2'),
    (instances_data[0], None, None, instances_data[1], None, None, 'ssh -o ProxyCommand="ssh -W %h:%p -i ~/.ssh/keypair1.pem ec2-user@1.1.1.1" -i ~/.ssh/keypair0.pem ec2-user@192.168.0.0'),
]


@pytest.mark.parametrize("instance,key_path,username,bastion_instance,bastion_key_path,bastion_username,expected", generate_ssh_command_data)
def test_generate_ssh_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username, expected):
    assert sshec2.generate_ssh_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username) == expected


def mock_parse_args(expected):
    return Namespace(bastion_name='bastion')


@mock.patch('argparse.ArgumentParser.parse_args', mock_parse_args)
def test_parse_args():
    assert sshec2.parse_args().bastion_name == 'bastion'


response = {'Reservations': [
    {'ReservationId': 'r-xxxxxxxxxxxxx', 'OwnerId': 'xxxxxxxxxxxxxxxx', 'Groups': [], 'Instances': [{
        'InstanceId': 'i-xxxxxxxxxxxxx', 'ImageId': 'ami-xxxxxxxxxxxxxxx', 'State': {'Code': 80, 'Name': 'stopped'},
        'PrivateDnsName': 'ip-.ap-northeast-1.compute.internal', 'PublicDnsName': '', 'StateTransitionReason': 'User initiated (2017-04-16 02:49:36 GMT)',
        'KeyName': 'xxxxxxxxx', 'AmiLaunchIndex': 0, 'ProductCodes': [], 'InstanceType': 'm3.medium', 'LaunchTime': '',
        'Placement': {'AvailabilityZone': 'ap-northeast-1a', 'GroupName': '', 'Tenancy': 'default'}, 'Monitoring': {'State': 'disabled'},
        'SubnetId': 'subnet-xxxxxxxxxxx', 'VpcId': 'vpc-xxxxxxxxx', 'PrivateIpAddress': '', 'StateReason': {
            'Code': 'Client.UserInitiatedShutdown', 'Message': 'Client.UserInitiatedShutdown: User initiated shutdown'},
        'Architecture': 'x86_64', 'RootDeviceType': 'ebs', 'RootDeviceName': '/dev/xvda',
        'BlockDeviceMappings': [{'DeviceName': '/dev/xvda', 'Ebs': {'VolumeId': 'vol-xxxxxxxxxx', 'Status': 'attached', 'AttachTime': '', 'DeleteOnTermination': True}}],
        'VirtualizationType': 'hvm', 'ClientToken': 'xxxxxxxxxxxx', 'Tags': [{'Key': 'Name', 'Value': 'xxxxxxxxx'}], 'SecurityGroups': [
            {'GroupName': 'default', 'GroupId': 'sg-xxxxxxxxxxxxxx'},
            {'GroupName': 'xxxx', 'GroupId': 'sg-xxxxxxxxx'},
            {'GroupName': 'xxxx', 'GroupId': 'sg-xxxxxxxxxx'},
            {'GroupName': 'ssh', 'GroupId': 'sg-xxxxxxxxxxxx'}],
        'SourceDestCheck': True, 'Hypervisor': 'xen', 'NetworkInterfaces': [{
            'NetworkInterfaceId': 'eni-xxxxxxxxxxx', 'SubnetId': 'subnet-xxxxxxxxxx', 'VpcId': 'vpc-xxxxxxxxxxx', 'Description': 'Primary network interface', 'OwnerId': 'xxxxxxxxxx',
            'Status': 'in-use', 'MacAddress': 'xxxxxxxxxx', 'PrivateIpAddress': 'xxxxxxxxx', 'PrivateDnsName': 'ip-xxxxxxx.ap-northeast-1.compute.internal', 'SourceDestCheck': True,
            'Groups': [{'GroupName': 'default', 'GroupId': 'sg-xxxxxxxxxx'}, {'GroupName': 'xxxx', 'GroupId': 'sg-xxxxxxxx'}, {'GroupName': 'xxxxxxxx', 'GroupId': 'sg-xxxxxxxxx'}, {'GroupName': 'ssh', 'GroupId': 'sg-xxxxxxxxxx'}],
            'Attachment': {'AttachmentId': 'eni-attach-xxxxxxxxxx', 'DeviceIndex': 0, 'Status': 'attached', 'AttachTime': '', 'DeleteOnTermination': True},
            'PrivateIpAddresses': [{'PrivateIpAddress': 'xxxxxxxxxxx', 'PrivateDnsName': 'ip-xxxxxxxx.ap-northeast-1.compute.internal', 'Primary': True}], 'Ipv6Addresses': []}],
        'IamInstanceProfile': {'Arn': 'arn:aws:iam::xxxxxxxxx:instance-profile/xxxxxxxxxxxx', 'Id': 'xxxxxxxxxxxxxxxxx'}, 'EbsOptimized': False, 'EnaSupport': True}]},
    {'ReservationId': 'r-xxxxxxxxxxxxx', 'OwnerId': 'xxxxxxxxxxxx', 'Groups': [], 'Instances': [{
        'InstanceId': 'i-xxxxxxxxxxxxxx', 'ImageId': 'ami-xxxxxxxxx', 'State': {'Code': 80, 'Name': 'stopped'},
        'PrivateDnsName': 'ip-xxxx.ap-northeast-1.compute.internal', 'PublicDnsName': '', 'StateTransitionReason': 'User initiated (2017-03-24 11:02:17 GMT)',
        'KeyName': 'xxxxxxxxxxx', 'AmiLaunchIndex': 0, 'ProductCodes': [], 'InstanceType': 'm3.medium', 'LaunchTime': '',
        'Placement': {'AvailabilityZone': 'ap-northeast-1a', 'GroupName': '', 'Tenancy': 'default'}, 'Monitoring': {'State': 'disabled'},
        'SubnetId': 'subnet-xxxxxxxxx', 'VpcId': 'vpc-xxxxxxxxxx', 'PrivateIpAddress': 'xxxxxxxxx', 'StateReason': {
            'Code': 'Client.UserInitiatedShutdown', 'Message': 'Client.UserInitiatedShutdown: User initiated shutdown'},
        'Architecture': 'x86_64', 'RootDeviceType': 'ebs', 'RootDeviceName': '/dev/xvda',
        'BlockDeviceMappings': [{'DeviceName': '/dev/xvda', 'Ebs': {'VolumeId': 'vol-xxxxxxxxxxxx', 'Status': 'attached', 'AttachTime': '', 'DeleteOnTermination': True}}],
        'VirtualizationType': 'hvm', 'ClientToken': 'xxxxxxxxxxx', 'Tags': [{'Key': 'Name', 'Value': 'xxxxxxxx'}], 'SecurityGroups': [
            {'GroupName': 'default', 'GroupId': 'sg-xxxxxxx'},
            {'GroupName': 'ssh', 'GroupId': 'sg-xxxxxxx'},
            {'GroupName': 'web', 'GroupId': 'sg-xxxxxxxxxx'}],
        'SourceDestCheck': True, 'Hypervisor': 'xen', 'NetworkInterfaces': [{
            'NetworkInterfaceId': 'eni-xxxxxxxxxx', 'SubnetId': 'subnet-xxxxxxx', 'VpcId': 'vpc-xxxxxxxxx', 'Description': 'Primary network interface', 'OwnerId': 'xxxxxxxxx',
            'Status': 'in-use', 'MacAddress': 'xxxxxx', 'PrivateIpAddress': 'xxxxxxxxx', 'PrivateDnsName': 'ip-xxxxxxxxxxap-northeast-1.compute.internal', 'SourceDestCheck': True,
            'Groups': [{'GroupName': 'default', 'GroupId': 'sg-xxxxxxxxxx'}, {'GroupName': 'ssh', 'GroupId': 'sg-xxxxxxxx'}, {'GroupName': 'web', 'GroupId': 'sg-xxxxxxxxx'}],
            'Attachment': {'AttachmentId': 'eni-attach-xxxxxxxx', 'DeviceIndex': 0, 'Status': 'attached', 'AttachTime': '', 'DeleteOnTermination': True},
            'PrivateIpAddresses': [{'PrivateIpAddress': 'xxxxxxxxxxx', 'PrivateDnsName': 'ip-xxxxxxxxx.ap-northeast-1.compute.internal', 'Primary': True}], 'Ipv6Addresses': []}],
        'IamInstanceProfile': {'Arn': 'arn:aws:iam::xxxxxxxxxx:instance-profile/xxxxxxxxx', 'Id': 'xxxxxxxxxxx'}, 'EbsOptimized': False, 'EnaSupport': True}]},
    {'ReservationId': 'r-xxxxxxxxx', 'OwnerId': 'xxxxxxxxx', 'Groups': [], 'Instances': [{
        'InstanceId': 'i-xxxxxxx', 'ImageId': 'ami-xxxxxxxxxx', 'State': {'Code': 16, 'Name': 'running'},
        'PrivateDnsName': 'ip-xxxxxxxx.ap-northeast-1.compute.internal', 'PublicDnsName': 'xxxxxxxx.ap-northeast-1.compute.amazonaws.com', 'StateTransitionReason': '',
        'KeyName': 'xxxxxxxxxx', 'AmiLaunchIndex': 0, 'ProductCodes': [], 'InstanceType': 't2.nano', 'LaunchTime': '',
        'Placement': {'AvailabilityZone': 'ap-northeast-1a', 'GroupName': '', 'Tenancy': 'default'}, 'Monitoring': {'State': 'disabled'},
        'SubnetId': 'subnet-xxxxxxxx', 'VpcId': 'vpc-xxxxxxxxx', 'PrivateIpAddress': 'xxxxxxxxx', 'PublicIpAddress': 'xxxxxxxxx',
        'Architecture': 'x86_64', 'RootDeviceType': 'ebs', 'RootDeviceName': '/dev/xvda',
        'BlockDeviceMappings': [{'DeviceName': '/dev/xvda', 'Ebs': {'VolumeId': 'vol-xxxxxxxxxx', 'Status': 'attached', 'AttachTime': '', 'DeleteOnTermination': True}}],
        'VirtualizationType': 'hvm', 'ClientToken': 'xxxxxxxxxxx', 'Tags': [{'Key': 'xxxxxxxx', 'Value': 'true'}, {'Key': 'Name', 'Value': 'nat'}], 'SecurityGroups': [
            {'GroupName': 'default', 'GroupId': 'sg-xxxxxxxx'},
            {'GroupName': 'ssh', 'GroupId': 'sg-xxxxxxxxx'}],
        'SourceDestCheck': False, 'Hypervisor': 'xen', 'NetworkInterfaces': [{
            'NetworkInterfaceId': 'eni-xxxxxxx', 'SubnetId': 'subnet-xxxxxxxxx', 'VpcId': 'vpc-xxxxxxx', 'Description': 'Primary network interface', 'OwnerId': 'xxxxxxxxxx',
            'Status': 'in-use', 'MacAddress': 'xxxxxxxxx', 'PrivateIpAddress': 'xxxxxxxx', 'PrivateDnsName': 'ip-xxxxxxxx.ap-northeast-1.compute.internal', 'SourceDestCheck': False,
            'Groups': [{'GroupName': 'default', 'GroupId': 'sg-xxxxxxxx'}, {'GroupName': 'ssh', 'GroupId': 'sg-xxxxxxxxx'}],
            'Attachment': {'AttachmentId': 'eni-attach-xxxxxxxxxxc6f9e26c', 'DeviceIndex': 0, 'Status': 'attached', 'AttachTime': '', 'DeleteOnTermination': True},
            'Association': {'PublicIp': 'xxxxxxxx', 'PublicDnsName': 'ec2-xxxxxxxx.ap-northeast-1.compute.amazonaws.com', 'IpOwnerId': 'xxxxxxxxxx'},
            'PrivateIpAddresses': [{'PrivateIpAddress': 'xxxxxxxxx', 'PrivateDnsName': 'ip-xxxxxxxxxxx.ap-northeast-1.compute.internal', 'Primary': True,
                                    'Association': {'PublicIp': 'xxxxxxxxxx', 'PublicDnsName': 'ec2-xxxxxxxx.ap-northeast-1.compute.amazonaws.com', 'IpOwnerId': 'xxxxxxx'}}], 'Ipv6Addresses': []}],
        'IamInstanceProfile': {'Arn': 'arn:aws:iam::xxxxxxxxxxxxx:instance-profile/xxxxxxxxx', 'Id': 'xxxxxxxx'}, 'EbsOptimized': False, 'EnaSupport': True}]}],
    'ResponseMetadata': {'RequestId': 'xxxxxxxxx', 'HTTPStatusCode': 200, 'HTTPHeaders': {
        'content-type': 'text/xml;charset=UTF-8', 'transfer-encoding': 'chunked', 'vary': 'Accept-Encoding', 'date': 'Tue, 30 May 2017 08:05:47 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}


def mock_session(client):
    session = MagicMock()
    session.client.return_value = client
    return lambda **kwargs: session


def test_describe_instances(monkeypatch):
    ec2 = MagicMock()
    ec2.describe_instances.return_value = response
    monkeypatch.setattr('boto3.Session', mock_session(ec2))
    assert len(sshec2.describe_instances('None')) == 3
