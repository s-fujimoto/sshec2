# 使用方法

このページでは sshec2 のユースケースに応じた一般的な使用方法をご紹介します。

## コマンドオプション

```
$ sshec2 --help
usage: sshec2 [-h] [-k KEY_PATH] [-u USERNAME] [--bastion] [-b BASTION_NAME]
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

## ログイン対象インスタンスの一覧表示・選択・SSH 接続

sshec2 の基本機能は起動中の EC2 インスタンスを一覧表示し、番号を選択することで選択したインスタンスへ SSH 接続します。  

```
$ sshec2
[ SELECT TARGET INSTANCE LIST ]
  0: instance000 (i-aaaaaaaaaaaaaaa) ap-northeast-1a
  1: instance001 (i-bbbbbbbbbbbbbbb) ap-northeast-1c
  2: instance002 (i-ccccccccccccccc) ap-northeast-1a
  3: instance003 (i-ddddddddddddddd) ap-northeast-1c
  4: instance004 (i-eeeeeeeeeeeeeee) ap-northeast-1a
input number ( if filter, input name part. if abort, input 'q' ) : 0
Last login: Fri May 26 10:48:08 2017 from xxxxxx.xx.xx.jp

       __|  __|_  )
       _|  (     /   Amazon Linux AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-ami/2016.09-release-notes/
21 package(s) needed for security, out of 55 available
Run "sudo yum update" to apply all updates.
Amazon Linux version 2017.03 is available.
[ec2-user@ip-172-31-0-100 ~]$
```

