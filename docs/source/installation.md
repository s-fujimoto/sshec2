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
```

### インストール後
```
pip list
appdirs (1.4.3)
boto3 (1.4.4)
botocore (1.5.40)
docutils (0.13.1)
sshec2 (0.1.0)
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
wheel (0.24.0)
```

## アンインストール

pip コマンドを利用して、アンインストールします。

```
```
