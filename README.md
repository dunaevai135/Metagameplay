metagameplayClientServerExample
===
консольное приложение, которое представляет собой упрощенную модель экономики игры.

Приложение состоит из 2 компонентов: Game Server и Game Client.

# Run
### on host
```
python -m pip install virtualenv
virtualenv venv
source venv/bin/activate
python -m pip install --upgrade pip

python -m pip install -r requirements.txt

python -m grpc_tools.protoc -I./proto --python_out=. --pyi_out=. --grpc_python_out=. ./proto/metagameplay.proto

```
### using docker
build:
```
docker build -t myimage .
```

run server:
```
docker run -p 50051:50051 myimage
```

run client:
```
docker run -it --network host myimage python client.py
```
