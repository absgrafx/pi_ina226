voltagelog.py
#!/usr/bin/env python3
import csv
import logging
from datetime import datetime
from ina226 import INA226
from time import sleep, time

def log_voltage_data(ina, interval, duration, filename):
    start_time = time()
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Bus Voltage (V)'])

        while time() - start_time < duration:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Including milliseconds
            bus_voltage = ina.voltage()

            # Write to CSV file
            writer.writerow([current_time, "%.3f" % bus_voltage])

            print(f"Logged at {current_time}: Bus Voltage: {bus_voltage:.3f} V")
            sleep(interval)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ina = INA226(busnum=1, max_expected_amps=25, log_level=logging.INFO)
    ina.configure()
    ina.set_low_battery(5)
    ina.wake()
    
    try:
        # Configure monitoring interval and logging duration
        monitoring_interval = 0.1  # seconds
        logging_duration = 5 * 60  # 5 minutes in seconds
        output_file = 'voltage_log.csv'
        
        log_voltage_data(ina, monitoring_interval, logging_duration, output_file)
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
    finally:
        ina.sleep()
        print("Device is now in sleep mode.")
