import datetime
from argparse import Namespace
import subprocess

import pytest
from dateutil.tz import tzutc

from sshec2 import sshec2

try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock


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
            {'Key': 'KEY2', 'Value': 'VALUE2'},
            {'Key': 'Name', 'Value': 'INSTANCE002'},
            {'Key': 'KEY3', 'Value': 'VALUE3'}],
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
            {'Key': 'KEY1', 'Value': 'VALUE1'}
        ],
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
        'VirtualizationType': 'hvm',
        'VpcId': 'vpc-xxxxxxxxx'
    }
]


get_instance_name_data = [
    (instances_data[0], 'INSTANCE000'),
    (instances_data[1], 'INSTANCE001'),
    (instances_data[2], 'INSTANCE002'),
    (instances_data[3], ''),
    (instances_data[4], ''),
]


@pytest.mark.parametrize("instance,expected", get_instance_name_data)
def test_get_instance_name(instance, expected):
    assert sshec2.get_instance_name(instance) == expected


validate_data = [
    (instances_data, 0, True),
    (instances_data, 1, True),
    (instances_data, 2, True),
    (instances_data, -1, False),
    (instances_data, 3, True),
    (instances_data, 4, True),
    (instances_data, 5, False),
    (instances_data, 6, False),
    (instances_data, 'a', False),
]


@pytest.mark.parametrize("instances,number,expected", validate_data)
def test_validate_input(instances, number, expected):
    assert sshec2.validate_input(instances, number) == expected


def test_system_exit_validate_input():
    with pytest.raises(SystemExit):
        sshec2.validate_input(instances_data, 'q')


setting_bastion_data = [
    (instances_data, 'INSTANCE000', '0.0.0.0'),
    (instances_data, 'INSTANCE001', '1.1.1.1'),
    (instances_data, '', 'test'),
]


@pytest.mark.parametrize("instances,bastion_name,expected", setting_bastion_data)
def test_setting_bastion(instances, bastion_name, expected):
    with patch('sshec2.sshec2.select_instance', lambda instances, target: {'PublicIpAddress': 'test'}):
        bastion = sshec2.setting_bastion(instances, bastion_name)
        assert bastion['PublicIpAddress'] == expected


system_exit_setting_bastion_data = [
    (instances_data, 'abc'),
    ([
        {'Tags': [{'Key': 'Name', 'Value': 'instance1'}]},
        {'Tags': [{'Key': 'Name', 'Value': 'instance1'}]}
    ], 'instance1'),
]


@pytest.mark.parametrize("instances,bastion_name", system_exit_setting_bastion_data)
def test_system_exit_setting_bastion(instances, bastion_name):
    with pytest.raises(SystemExit):
        sshec2.setting_bastion(instances, bastion_name)


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


socks_proxy_commands_data = [
    (instances_data[0], '10.0.0.1:1080', '-o ProxyCommand="nc -x 10.0.0.1:1080 0.0.0.0 %p"'),
]


@pytest.mark.parametrize("instance, socks_proxy_url,expected", socks_proxy_commands_data)
def test_socks_proxy_commands(instance, socks_proxy_url, expected):
    assert sshec2.socks_proxy_commands(instance, socks_proxy_url) == expected


bastion_commands_data = [
    (instances_data[1], instances_data[0], None, None, None, ['-o', 'ProxyCommand="ssh  -W 192.168.1.1:%p -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0"']),
    (instances_data[2], instances_data[1], '~/.ssh/test.pem', None, None, ['-o', 'ProxyCommand="ssh  -W 192.168.2.2:%p -i ~/.ssh/test.pem ec2-user@1.1.1.1"']),
    (instances_data[0], instances_data[2], None, 'test', None, ['-o', 'ProxyCommand="ssh  -W 192.168.0.0:%p -i ~/.ssh/keypair2.pem test@2.2.2.2"']),
    (instances_data[1], instances_data[0], None, None, None, ['-o', 'ProxyCommand="ssh  -W 192.168.1.1:%p -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0"']),
]


@pytest.mark.parametrize("target_instance,bastion_instance,key_path,username,socks_proxy_url,expected", bastion_commands_data)
def test_bastion_commands(target_instance, bastion_instance, key_path, username, socks_proxy_url, expected):
    assert sshec2.bastion_commands(target_instance, bastion_instance, key_path, username, socks_proxy_url) == expected


generate_scp_command_data = [
    (instances_data[0], None, None, None, None, None, 'from.txt', '/to/', True, False, None, 'scp -r -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0:from.txt /to/'),
    (instances_data[1], '~/.ssh/test.pem', None, None, None, None, 'from.txt', '/to/', True, False, None, 'scp -r -i ~/.ssh/test.pem ec2-user@1.1.1.1:from.txt /to/'),
    (instances_data[2], None, 'test', None, None, None, 'from.txt', '/to/', True, False, None, 'scp -r -i ~/.ssh/keypair2.pem test@2.2.2.2:from.txt /to/'),
    (instances_data[0], None, None, instances_data[1], None, None, 'from.txt', '/to/', True, False, None, 'scp -r -o ProxyCommand="ssh  -W 192.168.0.0:%p -i ~/.ssh/keypair1.pem ec2-user@1.1.1.1" -i ~/.ssh/keypair0.pem ec2-user@192.168.0.0:from.txt /to/'),
    (instances_data[0], None, None, instances_data[1], None, None, 'from.txt', '/to/', False, True, None, 'scp -r -o ProxyCommand="ssh  -W 192.168.0.0:%p -i ~/.ssh/keypair1.pem ec2-user@1.1.1.1" -i ~/.ssh/keypair0.pem from.txt ec2-user@192.168.0.0:/to/'),
]


@pytest.mark.parametrize("instance,key_path,username,bastion_instance,bastion_key_path,bastion_username,src_path,dst_path,scp_from,scp_to,socks_proxy_url,expected", generate_scp_command_data)
def test_generate_scp_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username, src_path, dst_path, scp_from, scp_to, socks_proxy_url, expected):
    assert sshec2.generate_scp_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username, src_path, dst_path, scp_from, scp_to, socks_proxy_url) == expected


generate_ssh_command_data = [
    (instances_data[0], None, None, None, None, None, None, 'ssh -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0'),
    (instances_data[1], '~/.ssh/test.pem', None, None, None, None, None, 'ssh -i ~/.ssh/test.pem ec2-user@1.1.1.1'),
    (instances_data[2], None, 'test', None, None, None, None, 'ssh -i ~/.ssh/keypair2.pem test@2.2.2.2'),
    (instances_data[0], None, None, instances_data[1], None, None, None,
     'ssh -o ProxyCommand="ssh  -W 192.168.0.0:%p -i ~/.ssh/keypair1.pem ec2-user@1.1.1.1" -i ~/.ssh/keypair0.pem ec2-user@192.168.0.0'),
    (instances_data[0], None, None, None, None, None, '10.0.0.1:1080',
     'ssh -o ProxyCommand="nc -x 10.0.0.1:1080 0.0.0.0 %p" -i ~/.ssh/keypair0.pem ec2-user@0.0.0.0'),
    (instances_data[0], None, None, instances_data[1], None, None, '10.0.0.1:1080',
     'ssh -o ProxyCommand="ssh -o ProxyCommand=\\"nc -x 10.0.0.1:1080 1.1.1.1 %p\\" -W 192.168.0.0:%p -i ~/.ssh/keypair1.pem ec2-user@1.1.1.1" -i ~/.ssh/keypair0.pem ec2-user@192.168.0.0'),
]


@pytest.mark.parametrize("instance,key_path,username,bastion_instance,bastion_key_path,bastion_username,socks_proxy_url,expected", generate_ssh_command_data)
def test_generate_ssh_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username, socks_proxy_url, expected):
    assert sshec2.generate_ssh_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username, socks_proxy_url) == expected


def mock_parse_args(expected):
    return Namespace(bastion_name='bastion')


@patch('argparse.ArgumentParser.parse_args', mock_parse_args)
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
    assert len(sshec2.describe_instances(None, None)) == 3


display_instances_data = [
    (instances_data, 'TARGET', ''),
    (instances_data, 'BASTION', ''),
    (instances_data, 'TARGET', 'INSTANCE'),
]


@pytest.mark.parametrize("instances,target,keyword", display_instances_data)
def test_display_instances(instances, target, keyword):
    sshec2.display_instances(instances, target, keyword)


select_instance_data = [
    (1, instances_data[1]),
    # ('a', instances_data[2])
]


@pytest.mark.parametrize("input_value,expected", select_instance_data)
def test_select_instance(input_value, expected):
    with patch('sshec2.sshec2.get_input', lambda: input_value):
        assert sshec2.select_instance(instances_data, 'TARGET') == expected


add_vpn_route_data = [
    ('test', instances_data[0])
]


@pytest.mark.parametrize("vif,instance", add_vpn_route_data)
def test_add_vpn_route(vif, instance):
    with patch('subprocess.call', lambda a, shell: a):
        sshec2.add_vpn_route(vif, instance)


main_data = [
    (True, 'INSTANCE000', True, True, False),
    (False, 'INSTANCE000', False, False, False),
]


@pytest.mark.parametrize("debug,bastion_name,vif,scp_from,scp_to", main_data)
def test_main(debug, bastion_name, vif, scp_from, scp_to):
    sshec2.parse_args = MagicMock(debug=debug, bastion_name=bastion_name, vif=vif, scp_from=scp_from, scp_to=scp_to)
    sshec2.describe_instances = MagicMock(return_value=instances_data)
    sshec2.setting_bastion = MagicMock(return_value=instances_data[0])
    sshec2.select_instance = MagicMock(return_value=instances_data[1])
    sshec2.add_vpn_route = MagicMock()
    sshec2.generate_scp_command = MagicMock(return_value='scp')
    sshec2.generate_ssh_command = MagicMock(return_value='ssh')
    subprocess.call = MagicMock()
    sshec2.main()
