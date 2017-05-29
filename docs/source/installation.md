# インストール／アンインストール

sshec2 は pip コマンドによりインストール、およびアンインストールを行うことができます。

## システム要件
### サポートOS
- macOS
- Ubuntu 12.04

他の OS では試験を行っていないため、動作確認できていませんが、Linux ディストリビューションで動作すると思います。

### サポート Python バージョン
- 2.7
- 3.3
- 3.4
- 3.5
- 3.6

2.6 系は動作しません。

### 依存パッケージ
- boto3
- botocore
- future

## インストール

pip コマンドを利用して、Github リポジトリから直接インストールします。PyPI には登録していません。

### インストール前
```
$ pip list
appdirs (1.4.3)
packaging (16.8)
pip (9.0.1)
pyparsing (2.2.0)
setuptools (35.0.2)
six (1.10.0)
wheel (0.24.0)
```

### インストール
```
$ pip install
pip install sshec2
Collecting sshec2
Collecting botocore==1.5.40 (from sshec2)
  Using cached botocore-1.5.40-py2.py3-none-any.whl
Collecting future (from sshec2)
Collecting boto3==1.4.4 (from sshec2)
  Using cached boto3-1.4.4-py2.py3-none-any.whl
Collecting python-dateutil<3.0.0,>=2.1 (from botocore==1.5.40->sshec2)
  Using cached python_dateutil-2.6.0-py2.py3-none-any.whl
Collecting jmespath<1.0.0,>=0.7.1 (from botocore==1.5.40->sshec2)
  Using cached jmespath-0.9.3-py2.py3-none-any.whl
Collecting docutils>=0.10 (from botocore==1.5.40->sshec2)
  Using cached docutils-0.13.1-py2-none-any.whl
Collecting s3transfer<0.2.0,>=0.1.10 (from boto3==1.4.4->sshec2)
  Using cached s3transfer-0.1.10-py2.py3-none-any.whl
Requirement already satisfied: six>=1.5 in /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages (from python-dateutil<3.0.0,>=2.1->botocore==1.5.40->sshec2)
Collecting futures<4.0.0,>=2.2.0; python_version == "2.6" or python_version == "2.7" (from s3transfer<0.2.0,>=0.1.10->boto3==1.4.4->sshec2)
  Using cached futures-3.1.1-py2-none-any.whl
Installing collected packages: python-dateutil, jmespath, docutils, botocore, future, futures, s3transfer, boto3, sshec2
Successfully installed boto3-1.4.4 botocore-1.5.40 docutils-0.13.1 future-0.16.0 futures-3.1.1 jmespath-0.9.3 python-dateutil-2.6.0 s3transfer-0.1.10 sshec2-0.1.0
```

### インストール後
```
$ pip list
appdirs (1.4.3)
boto3 (1.4.4)
botocore (1.5.40)
docutils (0.13.1)
future (0.16.0)
futures (3.1.1)
jmespath (0.9.3)
packaging (16.8)
pip (9.0.1)
pyparsing (2.2.0)
python-dateutil (2.6.0)
s3transfer (0.1.10)
setuptools (35.0.2)
six (1.10.0)
sshec2 (0.1.0)
wheel (0.24.0)
```

## アンインストール

pip コマンドを利用して、アンインストールします。

```
$ pip uninstall sshec2
Uninstalling sshec2-0.1.0:
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/bin/sshec2
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages/sshec2-0.1.0.dist-info/DESCRIPTION.rst
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages/sshec2-0.1.0.dist-info/INSTALLER
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages/sshec2-0.1.0.dist-info/METADATA
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages/sshec2-0.1.0.dist-info/RECORD
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages/sshec2-0.1.0.dist-info/WHEEL
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages/sshec2-0.1.0.dist-info/metadata.json
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages/sshec2-0.1.0.dist-info/top_level.txt
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages/sshec2/__init__.py
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages/sshec2/__init__.pyc
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages/sshec2/sshec2.py
  /Users/fujimoto.shinji/.pyenv/versions/2.7.9/envs/test/lib/python2.7/site-packages/sshec2/sshec2.pyc
Proceed (y/n)? y
  Successfully uninstalled sshec2-0.1.0
```
