# ec2ssh

SSH login utility for Amazon EC2 instance. Test only OSX.

![](https://raw.githubusercontent.com/s-fujimoto/ec2ssh/master/ec2ssh.gif)

### Features
- ssh login 
- display instance list (only running status instances)
    - Name tag and instance ID
- search and filter instance by name
- access via specify bastion
- access via vpn connection
- specify key name
- specify username
- transfer file via scp
    - from EC2 to local
    - from local to EC2

### Option
Command option. Option setting is available for Environment.

```
$ ec2ssh --help
usage: ec2ssh [-h] [-k KEY_PATH] [-u USERNAME] [--bastion] [-b BASTION_NAME]
              [-e BASTION_KEY_PATH] [-s BASTION_USERNAME] [-p PROFILE]
              [-v VIF] [-r REGION] [--scp-to-ec2] [--scp-from-ec2]
              [--source-path SOURCE_PATH] [--target-path TARGET_PATH]
              [--debug]

Simple argparse CLI

optional arguments:
  -h, --help            show this help message and exit
  -k KEY_PATH, --key-path KEY_PATH
                        Specify private key path
  -u USERNAME, --username USERNAME
                        Specify login user name
  --bastion             Enabled selecting bastion mode
  -b BASTION_NAME, --bastion-name BASTION_NAME
                        Specify bastion instance name
  -e BASTION_KEY_PATH, --bastion-key-path BASTION_KEY_PATH
                        Specify bastion private key path
  -s BASTION_USERNAME, --bastion-username BASTION_USERNAME
                        Specify bastion user name
  -p PROFILE, --profile PROFILE
                        Specify profile name for AWS credentials
  -v VIF, --vpn-interface VIF
                        Specify interface name for vpn
  -r REGION, --region REGION
                        Specify region name
  --scp-to-ec2          SCP from local to EC2 mode
  --scp-from-ec2        SCP from EC2 to local mode
  --source-path SOURCE_PATH
                        Specify source path
  --target-path TARGET_PATH
                        Specify target path
  --debug               logging debug mode
```

```-k, --key-path```  
Specify private key file path. 
* Default ```$HOME/.ssh/<<INSTANCE_KEY_PAIR_NAME>>.pem```
* ENVIRONMENT_KEY : ```KEY_PATH```

```-u, --username```  
Specify login username.
* Default ```ec2-user```
* ENVIRONMENT_KEY : ```EC2SSH_USERNAME```

```-p, --profile```  
Specify aws credential profile name.
aws credential file is ```$HOME/.aws/credential```
* ENVIRONMENT_KEY : ```EC2SSH_AWS_PROFILE```

```--bastion```
Select bastion mode.

```-b, --bastion-name```  
If ssh access via bastion, specify bastion instance name.
* ENVIRONMENT_KEY : ```EC2SSH_BASTION_NAME```

```-e, --bastion-key-path```  
If ssh access via bastion, specify bastion private key file path.
* Default ```$HOME/.ssh/<<BASTION_INSTANCE_KEY_PAIR_NAME>>.pem```
* ENVIRONMENT_KEY : ```EC2SSH_BASTION_KEY_PATH```

```-s, --bastion-username```  
If ssh access via bastion, specify bastion login username.
* Default ```ec2-user```
* ENVIRONMENT_KEY : ```EC2SSH_BASTION_USERNAME```

```-v, --vpn-interface```  
If ssh access via vpn connection, specify vpn interface name.
* ENVIRONMENT_KEY : ```EC2SSH_VPN_INTERFACE```

```-r, --region```
Region name of logging in EC2 instances.
ex. ap-northeast-1, us-east-1 etc
* ENVIRONMENT_KEY : ```EC2SSH_AWS_REGION```

```--scp-to-ec2```
SCP from local to EC2 mode

```--scp-from-ec2```
SCP from EC2 to local mode

```--src-path```
**SCP Mode option** Specify source path

```--dst-path```
**SCP Mode option** Specify target path

```--debug```
logging debug mode

### Usage
Only exec command ```ec2ssh```

#### Use not default profile (AWS credential)
ec2ssh using default profile is ```default```.  
ec2ssh is able to not default profile. ec2ssh searches profile name in ```~/.aws/credentials```.   

For example...  
- profile name : profile1

```
$ ec2ssh -p profile1
```

#### via bastion
Nested SSH login. 
Local -(public access)-> Bastion -(private aceess)-> Target

For example...
- Bastion instance name : bastion
- Bastion instance key pair path : ~/.ssh/bastion.pem
- Bastion instance user name : root

```
$ ec2ssh -b bastion -e ~/.ssh/bastion.pem -s root 
```

#### via vpn connection
Access via vpn connection. Add target instance having public ip address rule to local routing table. Exec ```sudo route add <target_ip>/32 -interface <vpn_interface_name>```  
Local -(VPN routing)-> Bastion

For example...  
- VPN interface name : utun2

```
$ ifconfig
<snip>
utun2: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1500
	inet 192.168.0.100 --> 192.168.0.100 netmask 0xffffffff

$ ec2ssh -v utun2
<select target instance number>
Input sudo password if required sudo password.
Password: <input sudo password>
```

#### SCP Mode
Transfer directory or file by SCP command. Exec (From local to EC2).  
```scp -r <source_path> <target_ip>:<destination_path>```  
Support to transfer via bastion.

For example transfer to EC2 from local.

- Source File : README.md
- Destination Directory : /tmp/

```
$ ec2ssh --scp-to --src README.md --dst /tmp/
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