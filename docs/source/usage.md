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

## ログイン対象インスタンスのフィルタ表示

sshec2 の一覧表示は起動中の全ての EC2 インスタンスを表示します。ただし、EC2 が 100 台以上ある環境もあります。100 台以上ある場合、対象のインスタンスを探すのは大変です。そこでインスタンス名を入力することで部分一致したインスタンスのみに絞って再表示します。

```
$ sshec2
[ SELECT TARGET INSTANCE LIST ]
  0: instance000 (i-aaaaaaaaaaaaaaa) ap-northeast-1a
  1: instance001 (i-bbbbbbbbbbbbbbb) ap-northeast-1c
  2: instance002 (i-ccccccccccccccc) ap-northeast-1a
  3: instance003 (i-ddddddddddddddd) ap-northeast-1c
  4: instance004 (i-eeeeeeeeeeeeeee) ap-northeast-1a
input number ( if filter, input name part. if abort, input 'q' ) : instance001

[ SELECT TARGET INSTANCE LIST ]
  1: instance001 (i-bbbbbbbbbbbbbbb) ap-northeast-1c
```

数字だけの入力はフィルタできませんのでご注意ください。

## クレデンシャル

sshec2 は Boto3 を使用して実装しています。利用するクレデンシャルは Boto3 の仕様に準拠します。またオプション指定することで ```$HOME/.aws/credentials``` から任意のプロファイルを選択できます。

```
$ sshec2 -p profile1
[ SELECT TARGET INSTANCE LIST ]
  0: instance100 (i-aaaaaaaaaaaaaaa) us-east-1a
  1: instance101 (i-bbbbbbbbbbbbbbb) us-east-1b
  2: instance102 (i-ccccccccccccccc) us-east-1c
input number ( if filter, input name part. if abort, input 'q' ) : 
```

## リージョン

クレデンシャル同様、デフォルトリージョンも Boto3 の仕様に準拠します。またオプション指定することで任意のリージョンにアクセスすることも可能です。

```
$ sshec2 -r us-east-1
[ SELECT TARGET INSTANCE LIST ]
  0: instance100 (i-aaaaaaaaaaaaaaa) us-east-1a
  1: instance101 (i-bbbbbbbbbbbbbbb) us-east-1b
  2: instance102 (i-ccccccccccccccc) us-east-1c
input number ( if filter, input name part. if abort, input 'q' ) : 
```

## 多段 SSH 接続（踏み台サーバ経由）

インターネット越しにパブリック IP アドレスを持たない EC2 インスタンスへ SSH アクセスする時にパブリック IP アドレスを持つ Linux インスタンスを経由して、対象インスタンスへアクセスすることで、対象インスタンスへ直接コマンドを発行するように操作できます。

sshec2 では多段 SSH 接続をサポートしています。対象の踏み台サーバはインスタンス名で指定するパターン、SSH 接続先同様、インスタンスの一覧表示から選択するパターンがあります。

##### インスタンス名指定
```
$ sshec2 -b bastion
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

##### インスタンス一覧表示から選択
```
$ sshec2 --bastion
[ SELECT BASTION INSTANCE LIST ]
  0: instance000 (i-aaaaaaaaaaaaaaa) ap-northeast-1a
  1: instance001 (i-bbbbbbbbbbbbbbb) ap-northeast-1c
  2: instance002 (i-ccccccccccccccc) ap-northeast-1a
  3: instance003 (i-ddddddddddddddd) ap-northeast-1c
  4: instance004 (i-eeeeeeeeeeeeeee) ap-northeast-1a
input number ( if filter, input name part. if abort, input 'q' ) : 0
[ SELECT TARGET INSTANCE LIST ]
  0: instance000 (i-aaaaaaaaaaaaaaa) ap-northeast-1a
  1: instance001 (i-bbbbbbbbbbbbbbb) ap-northeast-1c
  2: instance002 (i-ccccccccccccccc) ap-northeast-1a
  3: instance003 (i-ddddddddddddddd) ap-northeast-1c
  4: instance004 (i-eeeeeeeeeeeeeee) ap-northeast-1a
input number ( if filter, input name part. if abort, input 'q' ) : 1
Last login: Fri May 26 10:48:08 2017 from xxxxxx.xx.xx.jp

       __|  __|_  )
       _|  (     /   Amazon Linux AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-ami/2016.09-release-notes/
21 package(s) needed for security, out of 55 available
Run "sudo yum update" to apply all updates.
Amazon Linux version 2017.03 is available.
[ec2-user@ip-172-31-0-101 ~]$
```

" to apply all updates.
Amazon Linux version 2017.03 is available.
[ec2-user@ip-172-31-0-100 ~]$
```

## 多段 SSH 接続（SOCKS プロキシ経由）

社内の環境からインターネットアクセスする時に SOCKS プロキシ経由でアクセスする環境では、オプションで SOCKS プロキシの URL を指定することで SOCKS プロキシ経由の SSH 接続を行うことができます。踏み台サーバ経由と併用することも可能です。

```
$ sshec2 -s 10.0.0.1
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

## VPN 接続

社内などの固定された環境以外からもアクセスする場合もあるかと思います。例えば、自宅から社内の SSL-VPN を経由して、ログインするケース。この場合に SSL-VPN へのルーティング設定を自動で追加する機能があります。

この機能は至ってシンプルで、SSH 接続行う前に ```sudo route add``` コマンドでルーティングに追加するだけです。オプションとして、VPN 接続するインタフェース名を指定します。

```
$ ifconfig
<snip>
utun0: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 2000
	inet6 fe80::b041:36a7:194a:f289%utun0 prefixlen 64 scopeid 0xa
	nd6 options=201<PERFORMNUD,DAD>
utun1: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::437e:50fd:5b30:7c1d%utun1 prefixlen 64 scopeid 0x10
	nd6 options=201<PERFORMNUD,DAD>
utun2: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::37e3:f358:fa1:4b0c%utun2 prefixlen 64 scopeid 0x11
	nd6 options=201<PERFORMNUD,DAD>
utun3: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1500
	inet 192.168.0.10 --> 192.168.0.10 netmask 0xffffffff
```

今回は ```utun3``` を利用します。

```
$ sshec2 -v utun3
[ SELECT TARGET INSTANCE LIST ]
  0: instance000 (i-aaaaaaaaaaaaaaa) ap-northeast-1a
  1: instance001 (i-bbbbbbbbbbbbbbb) ap-northeast-1c
  2: instance002 (i-ccccccccccccccc) ap-northeast-1a
  3: instance003 (i-ddddddddddddddd) ap-northeast-1c
  4: instance004 (i-eeeeeeeeeeeeeee) ap-northeast-1a
input number ( if filter, input name part. if abort, input 'q' ) : 0

Input sudo password if required sudo password.
Password:
```

対象インスタンスを選択した後にパスワード入力を求められます。このパスワード入力はローカル端末の sudo パスワードです。```route add``` コマンドは root 権限が必要なため、```sudo route add``` コマンドを実行しています。

```
add net 52.198.31.171: gateway utun3
Last login: Fri May 26 10:48:08 2017 from xxxxxx.xx.xx.jp

       __|  __|_  )
       _|  (     /   Amazon Linux AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-ami/2016.09-release-notes/
21 package(s) needed for security, out of 55 available
Run "sudo yum update

## SCP モード

sshec2 は EC2 インスタンスとローカル端末間で SCP によるファイル転送を行うことができます。オプションの指定によって、EC2 インスタンスからローカル端末、ローカル端末から EC2 インスタンスの双方向に転送できます。また SCP は recursive モードを有効にしているため、ディレクトリ単位で転送できます。

##### EC2 インスタンスからローカル端末
```
$ sshec2 --scp-from-ec2 --src /tmp/transfer.txt --dst ./
[ SELECT TARGET INSTANCE LIST ]
  0: instance000 (i-aaaaaaaaaaaaaaa) ap-northeast-1a
  1: instance001 (i-bbbbbbbbbbbbbbb) ap-northeast-1c
  2: instance002 (i-ccccccccccccccc) ap-northeast-1a
  3: instance003 (i-ddddddddddddddd) ap-northeast-1c
  4: instance004 (i-eeeeeeeeeeeeeee) ap-northeast-1a
input number ( if filter, input name part. if abort, input 'q' ) : 0
transfer.txt                                                                100%    5     0.1KB/s   00:00

$ ls transfer.txt
transfer.txt
```

##### ローカル端末から EC2 インスタンス
```
$ sshec2 --scp-to-ec2 --src ./transfer_dir --dst /tmp/
[ SELECT TARGET INSTANCE LIST ]
  0: instance000 (i-aaaaaaaaaaaaaaa) ap-northeast-1a
  1: instance001 (i-bbbbbbbbbbbbbbb) ap-northeast-1c
  2: instance002 (i-ccccccccccccccc) ap-northeast-1a
  3: instance003 (i-ddddddddddddddd) ap-northeast-1c
  4: instance004 (i-eeeeeeeeeeeeeee) ap-northeast-1a
input number ( if filter, input name part. if abort, input 'q' ) : 0
transfer.txt                                                                100%    5     0.0KB/s   00:00

$ sshec2 
Last login: Fri May 26 10:48:08 2017 from xxxxxx.xx.xx.jp

       __|  __|_  )
       _|  (     /   Amazon Linux AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-ami/2016.09-release-notes/
21 package(s) needed for security, out of 55 available
Run "sudo yum update" to apply all updates.
Amazon Linux version 2017.03 is available.
[ec2-user@ip-172-31-0-100 ~]$ ls /tmp/transfer_dir/
transfer.txt
```