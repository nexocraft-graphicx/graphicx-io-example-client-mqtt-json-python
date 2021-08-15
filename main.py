# -*- coding: utf-8 -*-
import os.path
import threading
import time
import os

from graphicx.example.client.mqtt import ts_values_generator
from graphicx.example.client.mqtt import gio_mqtt_client_config_holder
from graphicx.example.client.mqtt import gio_mqtt_client
from graphicx.example.client.mqtt import gio_json_default_format
from graphicx.example.client.mqtt import gio_mqtt_publish

# ----- Configuration -----

config_data = gio_mqtt_client_config_holder.get_config_data()
mqtt_topic_prefix = config_data["mqtt_topic_prefix"]
device_identifier = config_data["device_identifier"]
format_id = config_data["format_id"]
compression_id = config_data["compression_id"]
mqtt_broker_host = config_data["mqtt_broker_host"]
mqtt_broker_port = int(config_data["mqtt_broker_port"])
mqtt_client_username = config_data["mqtt_client_username"]
mqtt_client_password = config_data["mqtt_client_password"]
mqtt_client_id = config_data["mqtt_client_id"]


# ----- Timer for regularly measuring and sending values to graphicx.io -----

def our_loop_in_one_thread():
    try:
        # time.time() returns EpochSeconds
        next_round = time.time()
        # the main loop
        while True:
            # take the current timestamp
            time_epochmillis = int(time.time() * 1000)
            # get some data to publish
            # in this example we do not use a module to gather sensor values
            # but instead we use a data source that simply generates some data
            source_ts = ts_values_generator.generate_ts_values_at(time_epochmillis)
            # serialize the data in one of the available formats
            json_payload = gio_json_default_format.create_json_payload_dict(source_ts)
            # publish the data
            gio_mqtt_publish.publish_ts(gio_mqtt_client.connection_status,
                                        gio_mqtt_client.connection_code,
                                        gio_mqtt_client.mqttc,
                                        mqtt_topic_prefix,
                                        device_identifier,
                                        time_epochmillis,
                                        json_payload)
            # next call in 30 seconds
            next_round = next_round + 30
            seconds_to_sleep = max(0.0, next_round - time.time())
            time.sleep(seconds_to_sleep)
    except (KeyboardInterrupt):
        print("KeyboardInterrupt caught in our loop.")
    except (SystemExit):
        print("SystemExit caught in our loop.")
        gio_mqtt_client.disconnect_mqtt()
    except:
        raise
    finally:
        gio_mqtt_client.disconnect_mqtt()
        os._exit(1)


# ----- Functions -----


def main():
    time.sleep(1)
    try:
        print(
            "mqtt_topic_prefix = " + mqtt_topic_prefix + "\n" +
            "device_identifier = " + device_identifier + "\n" +
            "format_id = " + format_id + "\n" +
            "compression_id = " + compression_id + "\n" +
            "mqtt_broker_host = " + mqtt_broker_host + "\n" +
            "mqtt_broker_port = " + str(mqtt_broker_port) + "\n" +
            "mqtt_client_username = " + mqtt_client_username + "\n" +
            "mqtt_client_id = " + mqtt_client_id + "\n"
        )
        # connect to MQTT Broker
        gio_mqtt_client.connect_mqtt()
        # examine if we are now connected
        if (gio_mqtt_client.connection_code != 0):
            print("Could not connect to MQTT Broker within 10 seconds." +
                  " Exiting program so that it will be restarted.\n")
            time.sleep(10)
            pass
        else:
            print("Starting our loop in another thread.\n")
            thread_to_execute_loop = threading.Thread(target=our_loop_in_one_thread)
            thread_to_execute_loop.daemon = True
            thread_to_execute_loop.start()
            while True:
                # let the main thread sleep while the other thread is executing the loop
                time.sleep(10)
    except (KeyboardInterrupt):
        print("KeyboardInterrupt caught in main.")
        gio_mqtt_client.disconnect_mqtt()
    except (SystemExit):
        print("SystemExit caught in main.")
        gio_mqtt_client.disconnect_mqtt()
    except:
        raise
    finally:
        print("Exiting from main.")
        gio_mqtt_client.disconnect_mqtt()
        time.sleep(10)


if __name__ == "__main__":
    main()
