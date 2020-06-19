# UDP SERVER

This UDP server receives the information sent by our sensors and write them in a DB.

# Install

1- Using `pyenv`, create a new virtualenv like:
`pyenv virtualenv 3.9-dev lanza`

2- Install requirements:
`pip3 install -r requirements.txt`

# Code / Contribute

* Install [pre-commit](https://pre-commit.com/#install):
  * (If Linux) 
  ```bash
  $ [sudo] pip install pre-commit
  ```
  * (If OS X) 
  ```bash
  $ brew install pre-commit
  ```

* Install hooks:

  ```bash
  $ pre-commit install --hook-type pre-push -f
  ```


# Run

Run the server using a `DummySensorProtocol` with:
`./start`

Available `SensorProtocols` are:

- `DummySensorProtocol`
- `RedisPublisherSensorProtocol`
- `RESTApiSensorProtocol`

To listen on all interfaces using the `RedisPublisherSensorProtocol` excecute:
```bash
UDPSERVER_HOST=0.0.0.0 UDPSERVER_PROTOCOL="RedisPublisherSensorProtocol" ./start
```

