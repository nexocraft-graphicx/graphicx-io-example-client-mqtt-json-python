

def publish_ts(connection_status,
               connection_code,
               mqtt_client,
               mqtt_topic,
               now,
               payload):
    if (connection_code == 0):
        # first publish to our new MQTT API using our new wire format
        mqtt_client.publish("c/NEXOCRAFT_PLASTICS_DEMO", payload, 1, False)
    else:
        print("\nDisconnected from MQTT Broker. " + connection_status[connection_code] +
              " Thus cannot publish data at " + str(now))
