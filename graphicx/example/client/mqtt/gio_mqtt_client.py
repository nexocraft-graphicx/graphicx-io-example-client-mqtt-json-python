import time
import paho.mqtt.client as mqtt

from graphicx.example.client.mqtt import gio_mqtt_client_config_holder

# ----- Log -----

print("Initializing MQTT Client.")

# ----- Configuration -----

config_data = gio_mqtt_client_config_holder.get_config_data()
mqtt_broker_host = config_data["mqtt_broker_host"]
mqtt_broker_port = int(config_data["mqtt_broker_port"])
mqtt_client_id = config_data["mqtt_client_id"]
mqtt_client_username = config_data["mqtt_client_username"]
mqtt_client_password = config_data["mqtt_client_password"]

# ----- Instantiate the MQTT Client -----

# we set the MQTT v3.1.1 clean session flag to true since this MQTT Client will only publish
mqttc = mqtt.Client(mqtt_client_id, True, None, mqtt.MQTTv311, "tcp")
# mqttc = mqtt.Client("raspidemo1_mqtt_client", None, None, mqtt.MQTTv5, "tcp")


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
    print("MQTT Client on_connect - Connection code: " + str(rc) + " " + connection_status[connection_code])


def on_publish(client, obj, mid):
    print("MQTT Client on_publish - Published mid: " + str(mid))


def on_disconnect(client, userdata, rc):
    global connection_code
    connection_code = rc
    if rc != 0:
        print("MQTT Client on_disconnect - Connection code: " + str(rc) + " " + connection_status[connection_code])


def on_log(client, obj, level, string):
    print("MQTT Client on_log - " + string)


mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_log = on_log
mqttc.on_disconnect = on_disconnect


# ----- Functions to connect and disconnect -----

def connect_mqtt():
    try:
        print("Configuring MQTT Client.")

        # this makes the MQTT Client behave like a web browser regarding TLS
        # see paho API documentation for details
        # https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php
        mqttc.tls_set(None, None, None, mqtt.ssl.CERT_REQUIRED, mqtt.ssl.PROTOCOL_TLSv1_2, None)
        mqttc.tls_insecure_set(False)

        mqttc.username_pw_set(mqtt_client_username, mqtt_client_password)
        mqttc.reconnect_delay_set(1, 60)
        mqttc.message_retry_set(10)

        print("Connecting MQTT Client and starting its internal loop thread" +
              " that automatically handles initial connect, retries of initial connect, reconnects.")
        mqttc.connect_async(mqtt_broker_host, mqtt_broker_port, 30)
        # If you run a network loop using loop_start() or loop_forever()
        # then re-connections are automatically handled for you.
        mqttc.loop_start()
        # give the MQTT Client some time to initially connect
        time.sleep(10)
    except:
        raise ValueError(
            "Failed to connect to the MQTT Broker. Please check the configuration of the MQTT Client.")


def disconnect_mqtt():
    print("If not yet done stopping MQTT Client gracefully.")
    mqttc.loop_stop()
    # give the network traffic some time to cease and thus the internal loop-thread of the MQTT Client to stop
    time.sleep(10)
    mqttc.disconnect()
    # give the MQTT Client some time to connect
    time.sleep(10)
