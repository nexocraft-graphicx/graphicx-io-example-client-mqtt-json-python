# -*- coding: utf-8 -*-
import json


def initialise_json_data_dict():
    # function for using JSON format TsChannelsFloatSeriesJSON
    data_dict = {'1': [], '2': [], '3': []}
    # will use three Channels, one for each datapoint
    return data_dict


def add_float_series_point_to_json_data_dict(data_dict, channel, time_epochmillis, value):
    # function for using JSON format TsChannelsFloatSeriesJSON
    float_series_point = {"time": time_epochmillis, "value": value}
    data_dict[str(channel)].append(float_series_point)
    return data_dict


def create_json_payload_dict(source_ts):
    time_epochmillis = source_ts[0][1]
    temperature_index = source_ts[0][0]
    temperature_value  = source_ts[0][2]
    relative_humidity_index = source_ts[1][0]
    relative_humidity_value  = source_ts[1][2]
    air_pressure_index = source_ts[2][0]
    air_pressure_value  = source_ts[2][2]

    # function for using JSON format TsChannelsFloatSeriesJSON
    try:
        data_dict = initialise_json_data_dict()
        add_float_series_point_to_json_data_dict(data_dict,
                                                 temperature_index,
                                                 time_epochmillis,
                                                 temperature_value)
        add_float_series_point_to_json_data_dict(data_dict,
                                                 relative_humidity_index,
                                                 time_epochmillis,
                                                 relative_humidity_value)
        add_float_series_point_to_json_data_dict(data_dict,
                                                 air_pressure_index,
                                                 time_epochmillis,
                                                 air_pressure_value)
        payload_dict = {'data': data_dict}
        payload_json = json.dumps(payload_dict)
        # if this would not use the simple default payload format (see graphicx.io quickstart)
        # the following would be done to include a format_id and a compression_id
        # moreover with MQTT v5 these would become custom headers on the MQTT message
        #        payload = bytes.fromhex(format_id) + bytes.fromhex(compression_id) + bytearray(payload_json, "utf8")
        payload = bytearray(payload_json, "utf8")
    except:
        print("Exception creating JSON payload dict.")
        raise
    return payload
