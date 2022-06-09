# graphicx-io-example-client-mqtt-json-python

Example MQTT Client for sending time series data to graphicx.io with

* Protocol: MQTT
* Payload Format: nexocraft wireformat (protobuf 3 compressed with zstandard)
* Language: python

This example under Apache License 2.0 helps you develop your own client.

You can also configure and run it for testing purposes.

## Project structure

Note that next to the Example MQTT client for sending time series data to graphicx.io
which has its entry point in main.py
this repository also contains the separate independent file mqtt_logger_example.py
which is just a very simple program to subscribe to an MQTT topic and print each received message.

## Prerequisites

MQTT Broker should be reachable - In order to connect to an MQTT Broker such as mqtt.graphicx.io this program needs to be executed in an environment with Internet access, or in case you are in a scenario with VPN, the configured MQTT Broker needs to be reachable there. In case you do not yet know whether this prerequisite is given, you could either wait until you reach the point where this program tries to reach the MQTT Broker, or you could try to check the reachability using commands such as netcat, for example as in `nc -v -z -4 mqtt_broker_host mqtt_broker_port`.

python - python 3.10 or higher is needed. Consider using a virtual python environment in order to avoid version conflicts within say your system python environment. See https://docs.python.org/3/tutorial/venv.html for more information if you are not yet familiar with virtual python environments. In case you are using an IDE such as PyCharm, the IDE can most probably manage virtual python environments for you as well.

pip - In your python environment the python package manager pip should be available. You might not need to install it, maybe you just should upgrade it. See https://pip.pypa.io/en/stable/installing/ for more information.

## Install python Modules this program depends on

To install python modules which this python program depends on in your python environment, use the following command:

```
pip install -r requirements.txt
```

## Configure

To adjust all necessary parameters in the configuration file simply use following command in the CLI:

```
python scripts/create_or_update_config.py
```

The script will ask you for following parameters and adjusts the configuration file:

- MQTT Broker Host (usually mqtt.graphicx.io, unless you would be told a different hostname and unless you'd use a VPN)
- MQTT Broker Port (usually 8883, if you need a non-TLS port this can be arranged e.g. via a VPN)
- MQTT username
- MQTT password
- MQTT Client ID
- MQTT Topic

Note: The script creates the file config_local.json which will be read by the main program. If the configuration file does not yet exist, it will be created. If it already exists, each current configuration parameter value will be presented and you will be asked if you want to keep or change it. 

## Run

Once you reached this step, the only remain task is to start the program and thus send real temperature and humidity data to the graphicx.io portal.

Use the following command:

```
python main.py
```

The script will start to connect and send data.

