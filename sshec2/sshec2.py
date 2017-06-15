from __future__ import print_function

import argparse
import logging
import os
import subprocess
import sys
from builtins import input

import boto3

DEFAULT_USERNAME = 'ec2-user'
DEFAULT_KEY_PATH = '~/.ssh/{}.pem'
INPUT_MESSAGE = 'input number ( if filter, input name part. if abort, input \'q\' ) : '

LOGGER = logging.getLogger('sshec2')
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logging.StreamHandler(sys.stdout))


def parse_args():
    parser = argparse.ArgumentParser(description='Simple argparse CLI')
    parser.add_argument('-k', '--key-path', dest='key_path', help='Specify private key path', default=os.environ.get('SSHEC2_KEY_PATH'), required=False)
    parser.add_argument('-u', '--username', dest='username', help='Specify login user name', default=os.environ.get('SSHEC2_USERNAME'), required=False)
    parser.add_argument('--bastion', dest='bastion', help='Enabled selecting bastion mode', action="store_true", required=False)
    parser.add_argument('-b', '--bastion-name', dest='bastion_name', help='Specify bastion instance name', default=os.environ.get('SSHEC2_BASTION_NAME'), required=False)
    parser.add_argument('-e', '--bastion-key-path', dest='bastion_key_path', help='Specify bastion private key path', default=os.environ.get('SSHEC2_BASTION_KEY_PATH'), required=False)
    parser.add_argument('-s', '--bastion-username', dest='bastion_username', help='Specify bastion user name', default=os.environ.get('SSHEC2_BASTION_USERNAME'), required=False)
    parser.add_argument('-p', '--profile', dest='profile', help='Specify profile name for AWS credentials', default=os.environ.get('SSHEC2_AWS_PROFILE'), required=False)
    parser.add_argument('-v', '--vpn-interface', dest='vif', help='Specify interface name for vpn', default=os.environ.get('SSHEC2_VPN_INTERFACE'), required=False)
    parser.add_argument('-r', '--region', dest='region', help='Specify region name', default=os.environ.get('SSHEC2_AWS_REGION'), required=False)
    parser.add_argument('--scp-to-ec2', dest='scp_to', help='SCP from local to EC2 mode', action="store_true", required=False)
    parser.add_argument('--scp-from-ec2', dest='scp_from', help='SCP from EC2 to local mode', action="store_true", required=False)
    parser.add_argument('--src', dest='src_path', help='Specify source path', required=False)
    parser.add_argument('--dst', dest='dst_path', help='Specify target path', required=False)
    parser.add_argument('--debug', dest='debug', help='logging debug mode', action="store_true", required=False)
    return parser.parse_args()


def get_instance_name(instance):
    tags = instance.get('Tags')
    if not tags:
        return ''

    name_tags = [tag for tag in tags if tag['Key'] == 'Name']

    if not name_tags:
        return ''

    return name_tags[0]['Value']


def describe_instances(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.client('ec2')
    result = ec2.describe_instances(Filters=[{'Name': 'instance-state-code', 'Values': ['16']}])
    desc_instances = [
        instance
        for reservation in result['Reservations']
        for instance in reservation['Instances']
    ]
    instances = sorted(desc_instances, key=get_instance_name)

    return instances


def display_instances(instances, target, keyword=''):
    subprocess.call('clear')
    print('[ SELECT {} INSTANCE LIST ]'.format(target))

    for num, instance in enumerate(instances):
        if keyword in get_instance_name(instance) and (target == 'TARGET' or (target == 'BASTION' and instance.get('PublicIpAddress'))):
            print('\033[30;43m{0:3}\033[0m: {1} ({2}) {3}'.format(num, get_instance_name(instance), instance['InstanceId'], instance['Placement']['AvailabilityZone']))


def validate_input(instances, number):
    if number == 'q':
        sys.exit(0)
    try:
        number = int(number)
    except ValueError:
        return False
    return 0 <= number < len(instances)


def setting_bastion(instances, bastion_name):
    if bastion_name:
        bastion_instances = [
            instance
            for instance in instances
            if get_instance_name(instance) == bastion_name]
        if not bastion_instances:
            print("[WARN] Don't exist specified name instance.")
            sys.exit(1)
        elif len(bastion_instances) > 1:
            print("[WARN] Specified name instance exists two or more.")
            sys.exit(1)
        return bastion_instances[0]
    return select_instance(instances, 'BASTION')


def get_input():
    return input(INPUT_MESSAGE)


def select_instance(instances, target):
    display_instances(instances, target)
    number = get_input()

    while not validate_input(instances, number):
        display_instances(instances, target, number)
        number = get_input()
    return instances[int(number)]


def add_vpn_route(vif, instance):
    ip_address = instance['PublicIpAddress']
    proc = subprocess.Popen('netstat -rn', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = proc.communicate()
    if ip_address not in out.decode('utf-8'):
        print('Input sudo password if required sudo password.')
        subprocess.call('sudo route add {}/32 -interface {}'.format(ip_address, vif), shell=True)


def get_key_path(instance, key_path):
    if not key_path:
        key_name = instance['KeyName']
        key_path = DEFAULT_KEY_PATH.format(key_name)
    return key_path


def get_username(username):
    if not username:
        username = DEFAULT_USERNAME
    return username


def get_host(instance, public=True):
    if public:
        return instance['PublicIpAddress']
    return instance['PrivateIpAddress']


def target_command(instance, key_path, username, public=True):
    return '-i {} {}@{}'.format(
        get_key_path(instance, key_path),
        get_username(username),
        get_host(instance, public)
    )


def bastion_commands(instance, key_path, username):
    return ['-o', 'ProxyCommand="ssh -W %h:%p {}"'.format(target_command(instance, key_path, username))]


def generate_scp_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username, src_path, dst_path, scp_from, scp_to):
    commands = ['scp', '-r']

    # bastion
    if bastion_instance:
        commands.extend(bastion_commands(bastion_instance, bastion_key_path, bastion_username))

    # target
    commands.extend(['-i', get_key_path(instance, key_path)])
    if scp_from:
        commands.extend([
            '{}@{}:{}'.format(
                get_username(username),
                get_host(instance, bastion_instance is None),
                src_path),
            dst_path])
    elif scp_to:
        commands.extend([
            src_path,
            '{}@{}:{}'.format(
                get_username(username),
                get_host(instance, bastion_instance is None),
                dst_path)])
    return " ".join(commands)


def generate_ssh_command(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username):
    commands = ['ssh']

    # bastion
    if bastion_instance:
        commands.extend(bastion_commands(bastion_instance, bastion_key_path, bastion_username))

    # target
    commands.append(target_command(instance, key_path, username, bastion_instance is None))

    return " ".join(commands)


def main():
    args = parse_args()

    if args.debug:
        LOGGER.setLevel(logging.DEBUG)

    instances = describe_instances(args.profile, args.region)

    # bastion setting
    bastion_instance = None
    if args.bastion_name or args.bastion:
        bastion_instance = setting_bastion(instances, args.bastion_name)

    # target
    instance = select_instance(instances, 'TARGET')

    # add vpn route
    if args.vif:
        add_vpn_route(args.vif, bastion_instance if bastion_instance else instance)

    # connect
    if args.scp_from or args.scp_to:
        command = generate_scp_command(
            instance, args.key_path, args.username, bastion_instance, args.bastion_key_path,
            args.bastion_username, args.src_path, args.dst_path, args.scp_from, args.scp_to)
    else:
        command = generate_ssh_command(
            instance, args.key_path, args.username, bastion_instance, args.bastion_key_path,
            args.bastion_username)

    LOGGER.debug(command)
    subprocess.call(command, shell=True)
