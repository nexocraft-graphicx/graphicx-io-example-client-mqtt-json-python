# graphicx-io-example-client-mqtt-json-python

## Configure the software

To adjust all necessary parameters in the configuration file simply use following command in the CLI of the Raspberry Pi:

```
python3 config.py
```

If python 3.4 or higher happens to be the default, this could also be just:

```
python config.py
```

The little script (config.py) will ask you for following parameters and adjusts the configuration file:

- Tenant ID
- Device Identifier
- MQTT Broker Host
- MQTT Broker Port
- MQTT username
- MQTT password
- MQTT Client ID

If you are not yet familiar with these parameters please read the [Quickstart Guide of graphicx.io](https://helpcenter.graphicx.io/en/support/solutions/79000057338).

The MQTT Client ID is usually a unique ID per IoT Device in case there is only one MQTT Client on the Device.

If use_led_matrix is the string 'true' or 'True' the program will draw an elegant X on the LED-Matrix. The color of the X depends on the current status. It is neutral during start of the program including initially connecting to the MQTT Broker. It is a highlight color during taking and sending measurements. It is yellow on exit due to an interrupt. It is red when there is a failure.

Note: If the configuration file does not yet exist, it will be created. If it already exists, each current value will be presented and you will be asked if you want to keep or change it. 

## Start to send MQTT messages with measurement data

Once you reached this step, the only remain task is to start the program and thus send real temperature and humidity data to the graphicx.io portal. Enter the following command in the CLI of the Raspberry Pi:

```
python3 main.py
```

If python 3.4 or higher happens to be the default, this could also be just:

```
python main.py
```

The script will start to connect and send data.

