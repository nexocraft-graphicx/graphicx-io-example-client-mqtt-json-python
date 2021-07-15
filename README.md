# graphicx-io-example-client-mqtt-json-python

Example MQTT Client for sending time series data to graphicx.io with

* Protocol: MQTT
* Payload Format: JSON
* Language: python

This example under Apache License 2.0 helps you develop your own client.

You can also configure and run it for testing purposes.

## Prerequisite

To connect to an MQTT Broker such as mqtt.graphicx.io this program needs to be executed in an environment with Internet access, or in case you are in a scenario with VPN, the configured MQTT Broker needs to be reachable there.

python 3.4 or higher is needed. Consider using a virtual python environment in order to avoid version conflicts within say your system python environment. See https://docs.python.org/3/tutorial/venv.html for more information if you are not yet familiar with virtual python environments. In case you are using an IDE such as PyCharm, the IDE can most probably manage virtual python environments for you as well.

## Configure

To adjust all necessary parameters in the configuration file simply use following command in the CLI:

```
python3 scripts/create_or_update_config.py
```

If python 3.4 or higher happens to be the default:

```
python scripts/create_or_update_config.py
```

The script will ask you for following parameters and adjusts the configuration file:

- Tenant ID (usually vod, but this is subject to be improved)
- Device Identifier (the external ID of your Device as currently saved in graphicx.io, alternatively its UUID in graphicx.io)
- MQTT Broker Host (usually mqtt.graphicx.io, unless you would be told a different hostname and unless you'd use a VPN)
- MQTT Broker Port (usually 8883, if you need a non-TLS port this can be arranged e.g. via a VPN)
- MQTT username
- MQTT password
- MQTT Client ID (usually a UUID)

If you are not yet familiar how these parameters are defined or how to obtain their values in your case, please read the [Quickstart Guide of graphicx.io](https://helpcenter.graphicx.io/en/support/solutions/79000057338). The MQTT parameters are defined as per MQTT protocol.

Note: The script creates the file config_local.json which will be read by the main program. If the configuration file does not yet exist, it will be created. If it already exists, each current configuration parameter value will be presented and you will be asked if you want to keep or change it. 

## Run

Once you reached this step, the only remain task is to start the program and thus send real temperature and humidity data to the graphicx.io portal.

Use the following command:

```
python3 main.py
```

If python 3.4 or higher happens to be the default:

```
python main.py
```

The script will start to connect and send data.

