# -*- coding: utf-8 -*-
import random


# ----- Function to generate random values for the example time series to publish -----

temperature_mean = 20.0
temperature_sigma = 2.0
temperature_random_state = random.getstate()

relative_humidity_mean = 30.0
relative_humidity_sigma = 5.0
relative_humidity_random_state = random.getstate()

barometric_pressure_in_millibars_mean = 1000.0
barometric_pressure_in_millibars_sigma = 10.0
barometric_pressure_in_millibars_state = random.getstate()


def generate_ts_values():
    global temperature_random_state
    random.setstate(temperature_random_state)
    temperature = random.normalvariate(temperature_mean, temperature_sigma)
    temperature_random_state = random.getstate()

    global relative_humidity_random_state
    random.setstate(relative_humidity_random_state)
    relative_humidity = random.normalvariate(relative_humidity_mean, relative_humidity_sigma)
    relative_humidity_random_state = random.getstate()

    global barometric_pressure_in_millibars_state
    random.setstate(barometric_pressure_in_millibars_state)
    barometric_pressure_in_millibars = random.normalvariate(barometric_pressure_in_millibars_mean,
                                                            barometric_pressure_in_millibars_sigma)
    barometric_pressure_in_millibars_state = random.getstate()

    ts_values = [temperature, relative_humidity, barometric_pressure_in_millibars]

    print("Generated time series values: " + str(ts_values))

    return ts_values
