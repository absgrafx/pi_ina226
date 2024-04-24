#!/usr/bin/env python3
# Description: This script logs the bus voltage of the INA226 power monitor 
# to a CSV file only when the change in voltage is greater than a specified threshold.
# Modify the 
    # monitoring_interval, 
    # logging_duration, 
    # voltage_change_threshold, and 
    # output_file variables to suit your requirements.
# Usage: python3 efficientlogging.py
# Note: This script requires the ina226.py file to be present in the same directory.
# The INA226 power monitor must be connected to the I2C bus of the Raspberry Pi.
# The INA226 power monitor must be connected to a power source and a load to measure the bus voltage.
# The INA226 power monitor must be configured with the ina226.configure() method before logging data.
# The INA226 power monitor must be put to sleep with the ina226.sleep() method after logging data.
# The INA226 power monitor must be woken up with the ina226.wake() method before logging data.

import csv
import logging
from datetime import datetime
from ina226 import INA226
from time import sleep, time

def log_voltage_data(ina, interval, duration, filename, threshold):
    start_time = time()
    last_logged_voltage = None  # Variable to store the last logged voltage

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Bus Voltage (V)'])

        while time() - start_time < duration:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Including milliseconds
            bus_voltage = ina.voltage()

            # Display all readings on the console
            print(f"Current at {current_time}: Bus Voltage: {bus_voltage:.3f} V")

            # Write to CSV file only if the change in voltage is greater than the threshold
            if last_logged_voltage is None or abs(bus_voltage - last_logged_voltage) > threshold:
                writer.writerow([current_time, "%.3f" % bus_voltage])
                last_logged_voltage = bus_voltage
                print(f"Logged at {current_time}: Bus Voltage: {bus_voltage:.3f} V")  # Optionally log this to file as well

            sleep(interval)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ina = INA226(busnum=1, max_expected_amps=25, log_level=logging.INFO)
    ina.configure()
    ina.set_low_battery(5)
    ina.wake()
    
    try:
        # Configure monitoring interval, logging duration, and voltage change threshold
        monitoring_interval = 0.1  # seconds
        logging_duration = 1 * 60  # 5 minutes in seconds
        voltage_change_threshold = 0.01  # volts
        output_file = 'efficient_log.csv'
        
        log_voltage_data(ina, monitoring_interval, logging_duration, output_file, voltage_change_threshold)
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
    finally:
        ina.sleep()
        print("Device is now in sleep mode.")

