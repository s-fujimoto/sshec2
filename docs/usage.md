# Usage

このページでは ec2ssh のユースケースに応じた一般的な使い方をご紹介します。

## Usage

```
$ ec2ssh --help
usage: ec2ssh [-h] [-k KEY_PATH] [-u USERNAME] [--bastion] [-b BASTION_NAME]
              [-e BASTION_KEY_PATH] [-s BASTION_USERNAME] [-p PROFILE]
              [-v VIF] [-r REGION] [--scp-to-ec2] [--scp-from-ec2]
              [--src SRC_PATH] [--dst DST_PATH] [--debug]

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
  --src SRC_PATH        Specify source path
  --dst DST_PATH        Specify target path
  --debug               logging debug mode
```

## ログイン対象インスタンスの一覧表示・選択

Amazon EC2 インスタンスは

```
$ ec2ssh

```