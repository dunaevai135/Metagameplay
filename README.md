metagameplayClientServerExample
===


# Init
```
python -m pip install virtualenv
virtualenv venv
source venv/bin/activate
python -m pip install --upgrade pip

python -m pip install grpcio
python -m pip install grpcio-tools


python -m grpc_tools.protoc -I./proto --python_out=. --pyi_out=. --grpc_python_out=. ./proto/metagameplay.proto

```

```
sqlite3

```