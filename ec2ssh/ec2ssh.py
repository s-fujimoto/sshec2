#!/usr/bin/env python

import subprocess
import os
import argparse
try:
    import boto3
except ImportError:
    print('*******************************')
    print('ERROR : Please install boto3. Please exec following commad.')
    print('pip install boto3')
    print('*******************************')
    import sys
    sys.exit(1)

DEFAULT_USERNAME = 'ec2-user'
DEFAULT_KEY_PATH = '~/.ssh/{}.pem'

SSH_OPTION = '-o StrictHostKeyChecking=no'

def parse_args():
    parser = argparse.ArgumentParser(description='Simple argparse CLI')
    parser.add_argument('-k', '--key-path', dest='key_path', help='Specify private key path', default=os.environ.get('KEY_PATH'), required=False)
    parser.add_argument('-u', '--username', dest='username', help='Specify login user name', default=os.environ.get('USERNAME'), required=False)
    parser.add_argument('-b', '--bastion-name', dest='bastion_name', help='Specify bastion instance name', default=os.environ.get('BASTION_NAME'), required=False)
    parser.add_argument('-e', '--bastion-key-path', dest='bastion_key_path', help='Specify bastion private key path', default=os.environ.get('BASTION_KEY_PATH'), required=False)
    parser.add_argument('-s', '--bastion-username', dest='bastion_username', help='Specify bastion user name', default=os.environ.get('BASTION_USERNAME'), required=False)
    parser.add_argument('-p', '--profile', dest='profile', help='Specify profile name for AWS credentials', default=os.environ.get('AWS_PROFILE'), required=False)
    return parser.parse_args()

def get_instance_name(instance):
    tags = instance.get('Tags')
    if not tags:
        return ''
    
    name_tags = [ tag for tag in tags if tag['Key'] == 'Name' ]

    if not name_tags:
        return ''

    return name_tags[0]['Value']


def describe_instances(profile, bastion_name):
    session = boto3.Session(profile_name=profile)
    ec2 = session.client('ec2')
    result = ec2.describe_instances(Filters=[{'Name':'instance-state-code', 'Values':['16']}])
    desc_instances = [
        instance
        for reservation in result['Reservations']
        for instance in reservation['Instances']
    ]
    sorted_instances = sorted(desc_instances, key=lambda i:get_instance_name(i))
    instances = [
        (num, instance)
        for num, instance in enumerate(sorted_instances)
    ]

    display_instances(instances)

    bastion_instance = None
    if bastion_name:
        bastion_instance = [ instance[1]
            for instance in instances
            if get_instance_name(instance[1]) == bastion_name ][0]
        if not bastion_instance:
            raise Exception("Don't exist specify bastion instance.")

    return bastion_instance, instances


def display_instances(instances):
    subprocess.call('clear')
    print('[ TARGET INSTANCE LIST ]')
    if not instances:
        print('instance include inputed name does not exist')

    for i in instances:
        print('\033[30;43m{0:3}\033[0m: {1} ({2})'.format(i[0], get_instance_name(i[1]), i[1]['InstanceId']))


def search_instances(instances, number):
    display_instances([
        instance
        for instance in instances
        if number in get_instance_name(instance[1]) 
    ])


def validate_input(instances, number):
    try:
        number = int(number)
    except ValueError:
        return False
    return 0 <= number < len(instances)


def _generate_access(instance, key_path, username, public=True):
    if not username:
        username = DEFAULT_USERNAME
    
    if not key_path:
        key_name = instance['KeyName']
        key_path = DEFAULT_KEY_PATH.format(key_name)
    
    if public:
        host = instance['PublicIpAddress']
    else:
        host = instance['PrivateIpAddress']

    return '-i {} {}@{} {}'.format(key_path, username, host, SSH_OPTION)


def connect(instance, key_path, username, bastion_instance, bastion_key_path, bastion_username):
    commands = ['ssh']

    ### bastion
    if bastion_instance:
        commands.extend(['-o', 'ProxyCommand="ssh -W %h:%p {}"'.format(
            _generate_access(bastion_instance, bastion_key_path, bastion_username))])
    
    ### target
    commands.append(_generate_access(instance, key_path, username, bastion_instance==None))

    subprocess.call(" ".join(commands), shell=True)


def main():
    args = parse_args()
    
    bastion_instance, instances = describe_instances(args.profile, args.bastion_name)
    # instance = read_input(instances)

    number = input('input number ( if filter, input name part ) : ')

    while not validate_input(instances, number):
        search_instances(instances, number)
        number = input('input number ( if filter, input name part ) : ')
    
    instance = instances[int(number)][1]

    connect(instance, args.key_path, args.username, bastion_instance, args.bastion_key_path, args.bastion_username)


if __name__ == '__main__':
    main()
