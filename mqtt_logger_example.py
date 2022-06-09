import time
import socks
import paho.mqtt.client as mqtt

# ==============================================================================================
# MQTT Logger Example
# This is an auxiliary program provided alongside main.py
# that subscribes to an MQTT Topic and prints each received message.
# If you want to study the example for publishing data please start in main.py.
#
# This MQTT logger example can be used to debug whether in an MQTT topic messages are arriving.
# It can be used as an alternative to the tool MQTT Explorer for example.
#
# To use this program please replace the configuration values below locally.


# ----- Configuration is hardcoded for now -----

MQTT_BROKER_ADDRESS = "replace_me__MQTT_BROKER_ADDRESS"
MQTT_BROKER_PORT = 8883
MQTT_TOPIC = "replace_me__MQTT_TOPIC"
MQTT_CLIENT_ID = "replace_me__MQTT_CLIENT_ID"
MQTT_CLIENT_USERNAME = "replace_me__MQTT_CLIENT_USERNAME"
MQTT_CLIENT_PASSWORD = "replace_me__MQTT_CLIENT_PASSWORD"


# ----- Instantiate the MQTT Client -----

# we set the MQTT v3.1.1 clean session flag to true since this MQTT Client will only publish
mqtt_client = mqtt.Client(MQTT_CLIENT_ID, True, None, mqtt.MQTTv311, "tcp")
# mqtt_client = mqtt.Client("raspidemo1_mqtt_client", None, None, mqtt.MQTTv5, "tcp")


# ----- Translate connection status of the MQTT Client -----

connection_status = [
    "Connection successful",
    "Connection refused – incorrect protocol version",
    "Connection refused – invalid client identifier",
    "Connection refused – server unavailable",
    "Connection refused – bad username or password",
    "Connection refused – not authorised",
    "Connection status not initialised"
]

# ----- Variable to track the connection status of the MQTT Client -----

connection_code = -1


# ----- Define and set the event callbacks in the MQTT Client -----

def on_connect(client, userdata, flags, rc):
    global connection_code
    connection_code = rc
    print("MQTT Logger Example on_connect - Connection code: " + str(rc) + " " + connection_status[connection_code])
    if (connection_code == 0):
        print("MQTT Logger Example on_connect - Subscribing to " + MQTT_TOPIC)
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_TOPIC)
        print("MQTT Logger Example on_connect - Subscribed to " + MQTT_TOPIC)


def on_message(client, userdata, msg):
    print(str(msg.payload))


def on_publish(client, obj, mid):
    # Just implemented out of curiosity. Will not happen since no message is published.
    print("MQTT Logger Example on_publish - Published mid: " + str(mid))


def on_disconnect(client, userdata, rc):
    global connection_code
    connection_code = rc
    if rc != 0:
        print("MQTT Logger Example on_disconnect - Connection code: " + str(rc) + " " + connection_status[
            connection_code])


def on_log(client, obj, level, string):
    print("MQTT Logger Example on_log - " + string)


mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.on_message = on_message
mqtt_client.on_log = on_log
mqtt_client.on_disconnect = on_disconnect


# ----- Functions to connect and disconnect -----

def connect_mqtt():
    try:
        print("MQTT Logger Example connect_mqtt - Configuring MQTT Client.")

        # this makes the MQTT Client behave like a web browser regarding TLS
        # see paho API documentation for details
        # https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php
        mqtt_client.tls_set(None, None, None, mqtt.ssl.CERT_REQUIRED, mqtt.ssl.PROTOCOL_TLSv1_2, None)
        mqtt_client.tls_insecure_set(False)

        mqtt_client.username_pw_set(MQTT_CLIENT_USERNAME, MQTT_CLIENT_PASSWORD)
        mqtt_client.reconnect_delay_set(1, 60)
        mqtt_client.message_retry_set(10)

        print("MQTT Logger Example connect_mqtt - Connecting MQTT Client.")
        mqtt_client.connect_async(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT, 30)
    except:
        raise ValueError(
            "Failed to connect to the MQTT Broker. Please check the configuration of the MQTT Client.")


def disconnect_mqtt():
    print("MQTT Logger Example disconnect_mqtt - If not yet done stopping MQTT Client gracefully."
          + " This takes a few seconds.")
    mqtt_client.loop_stop()
    # give the network traffic some time to cease and thus the internal loop-thread of the MQTT Client to stop
    time.sleep(10)
    mqtt_client.disconnect()
    # give the MQTT Client some time to disconnect
    time.sleep(5)


# ----- Main -----


def main():
    time.sleep(1)
    try:
        # connect to MQTT Broker
        connect_mqtt()
        # give the MQTT Client some time to initially try to connect
        time.sleep(5)
        # If you run a network loop using loop_start() or loop_forever()
        # then re-connections are automatically handled for you.
        mqtt_client.loop_forever(20.0, 1, True)
        # examine if we are now connected
        print("MQTT Logger Example main - Connection code: "
              + str(connection_code) + " " + connection_status[connection_code])
        if (connection_code != 0):
            print("MQTT Logger Example main - Connecting failed.")
            time.sleep(10)
            pass
        else:
            print("MQTT Logger Example main - Connected.")
    except (KeyboardInterrupt):
        print("MQTT Logger Example main - KeyboardInterrupt caught in main.")
        disconnect_mqtt()
    except (SystemExit):
        print("MQTT Logger Example main - SystemExit caught in main.")
        disconnect_mqtt()
    except:
        raise
    finally:
        print("MQTT Logger Example main - Exiting from main.")
        disconnect_mqtt()
        time.sleep(10)


if __name__ == "__main__":
    main()
