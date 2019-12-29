# Measure the distance or depth with an HCSR04 Ultrasonic sound 
# sensor and a Raspberry Pi.  Imperial and Metric measurements are available

# Al Audet
# MIT License
from __future__ import division

import time
import math
import warnings
import RPi.GPIO as GPIO

TRIG_PIN = 21
ECHO_PIN = 20


class Measurement(object):
    # Create a measurement using a HC-SR04 Ultrasonic Sensor connected to 
    # the GPIO pins of a Raspberry Pi.
    # Metric values are used by default. For imperial values use
    # unit='imperial'
    # temperature=<Desired temperature in Fahrenheit>


    def __init__(
        self, trig_pin, echo_pin, temperature=20, unit="metric", gpio_mode=GPIO.BCM
    ):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.temperature = temperature
        self.unit = unit
        self.gpio_mode = gpio_mode
        self.pi = math.pi
        self.median_reading = 0
        # setup input/output pins
        GPIO.setwarnings(False)
        GPIO.setmode(self.gpio_mode)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def raw_distance(self, sample_size=11, sample_wait=0.1):
        # Return an error corrected unrounded distance, in cm, of an object 
        # adjusted for temperature in Celcius.  The distance calculated
        # is the median value of a sample of `sample_size` readings.
        # Speed of readings is a result of two variables.  The sample_size
        # per reading and the sample_wait (interval between individual samples).
        # Example: To use a sample size of 5 instead of 11 will increase the 
        # speed of your reading but could increase variance in readings;
        # value = sensor.Measurement(trig_pin, echo_pin)
        # r = value.raw_distance(sample_size=5)
        # Adjusting the interval between individual samples can also
        # increase the speed of the reading.  Increasing the speed will also
        # increase CPU usage.  Setting it too low will cause errors.  A default
        # of sample_wait=0.1 is a good balance between speed and minimizing 
        # CPU usage.  It is also a safe setting that should not cause errors.
        # e.g.
        # r = value.raw_distance(sample_wait=0.03)

        if self.unit == "imperial":
            self.temperature = (self.temperature - 32) * 0.5556
        elif self.unit == "metric":
            pass
        else:
            raise ValueError("Wrong Unit Type. Unit Must be imperial or metric")

        speed_of_sound = 331.3 * math.sqrt(1 + (self.temperature / 273.15))
        sample = []
        sonar_signal_off = 0
        sonar_signal_on = 0
        missed_pulse = False

        for distance_reading in range(sample_size):
            GPIO.output(self.trig_pin, GPIO.LOW)
            time.sleep(sample_wait)
            GPIO.output(self.trig_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_pin, False)
            echo_status_counter = 1
            while GPIO.input(self.echo_pin) == 0 and echo_status_counter<1001:
                if echo_status_counter < 1000:
                    sonar_signal_off = time.time()
                    echo_status_counter += 1
                else:
                    print("Echo pulse was not received")
                    missed_pulse = True
                    break
            while GPIO.input(self.echo_pin) == 1:
                sonar_signal_on = time.time()
                if missed_pulse == True:
                    break
            if missed_pulse == False:
                time_passed = sonar_signal_on - sonar_signal_off
                distance_cm = time_passed * ((speed_of_sound * 100) / 2)
                sample.append(distance_cm)
            else:
                missed_pulse == False
                # out of range or other error
                sample.append(99999999)
        sorted_sample = sorted(sample)
        self.median_reading = sorted_sample[sample_size // 2]
        if self.median_reading > 100:
            for distance_reading in range(sample_size):
                print(sample[distance_reading])

    def distance(self):
        # Calculate the distance from the sensor to an object.
        self.raw_distance()
        if self.unit == "imperial":
            return self.median_reading * 0.394
        else:
            # don't need this method if using metric. Use raw_distance
            # instead.  But it will return median_reading anyway if used.
            return self.median_reading

    @staticmethod
    def basic_distance(trig_pin, echo_pin, celsius=20):
        # Return an unformatted distance in cm's as read directly from
        # RPi.GPIO.

        sonar_signal_off = 0
        sonar_signal_on = 0

        speed_of_sound = 331.3 * math.sqrt(1 + (celsius / 273.15))
        GPIO.setup(trig_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        GPIO.output(trig_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(trig_pin, False)
        echo_status_counter = 1
        while GPIO.input(echo_pin) == 0:
            if echo_status_counter < 1000:
                sonar_signal_off = time.time()
                echo_status_counter += 1
            else:
                raise SystemError("Echo pulse was not received")
        while GPIO.input(echo_pin) == 1:
            sonar_signal_on = time.time()

        time_passed = sonar_signal_on - sonar_signal_off
        return time_passed * ((speed_of_sound * 100) / 2)


if __name__ == "__main__":
    hcsr04 = Measurement(TRIG_PIN, ECHO_PIN)
    try:
        while(True):
            how_far = hcsr04.distance()
            print('Distance: {:.1f} cm' .format(how_far))
            time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()