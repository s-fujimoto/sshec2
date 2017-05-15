# ec2ssh

SSH login utility for Amazon EC2 instance.

![](https://raw.githubusercontent.com/s-fujimoto/ec2ssh/master/ec2ssh.gif)

### Features
- display instance list (only running status instances)
    - Name tag and instance ID
- search and filter instance by name
- access via specify bastion
- specify key name
- specify username

### Option
```
$ ec2ssh --help
usage: ec2ssh [-h] [-k KEY_PATH] [-u USERNAME] [-b BASTION_NAME]
              [-e BASTION_KEY_PATH] [-s BASTION_USERNAME] [-p PROFILE]

Simple argparse CLI

optional arguments:
  -h, --help            show this help message and exit
  -k KEY_PATH, --key-path KEY_PATH
                        Specify private key path
  -u USERNAME, --username USERNAME
                        Specify login user name
  -b BASTION_NAME, --bastion-name BASTION_NAME
                        Specify bastion instance name
  -e BASTION_KEY_PATH, --bastion-key-path BASTION_KEY_PATH
                        Specify bastion private key path
  -s BASTION_USERNAME, --bastion-username BASTION_USERNAME
                        Specify bastion user name
  -p PROFILE, --profile PROFILE
                        Specify profile name for AWS credentials
```

### Installation
Install from github repository.

```
$ pip install git+https://github.com/s-fujimoto/ec2ssh
```

```
$ pip list
boto3 (1.4.4)
botocore (1.5.40)
docutils (0.13.1)
ec2ssh (0.0.1)
jmespath (0.9.2)
pip (9.0.1)
python-dateutil (2.6.0)
s3transfer (0.1.10)
setuptools (28.8.0)
six (1.10.0)
```

### Uninstallation
Uninstall from pip packages

```
$ pip uninstall ec2ssh
```