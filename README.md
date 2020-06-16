# UDP SERVER

This UDP server receives the information sent by our sensors and write them in a DB.

# Install and run

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

Run the server with:
`./run server`

Test the server running a test client with:
`./run client`



# Packet structure
We will use struct https://docs.python.org/3/library/struct.html#struct-alignment

### Sensors

https://cdn-shop.adafruit.com/datasheets/1899_HTU21D.pdf

### Humidity and Temperature

Field       Type            Storage size    Format
--------------------------------------------------
Humidity    Unsigned char   (1 byte)        B
Temperature Signed char     (1 byte)        b
Hardware ID -               -               -


# Notes
What happen if connectivity is lost by 6 hours, save in buffer and change mode to deep sleeps?
