

def create_topic_name(tenant_identifier, device_identifier):
    topic = (
            "tenant/" + tenant_identifier + "/ts/in/" + device_identifier
    )
    #    print("\nMQTT topic: " + topic)
    return topic


def publish_ts(connection_status,
               connection_code,
               mqttc,
               tenant_identifier,
               device_identifier,
               time_epochmillis,
               payload):
    if (connection_code == 0):
        topic = create_topic_name(tenant_identifier, device_identifier)
        mqttc.publish(topic, payload, 1, False)
    else:
        print("\nDisconnected from MQTT Broker. " + connection_status[connection_code] +
              " Thus cannot publish data at " + str(time_epochmillis))
