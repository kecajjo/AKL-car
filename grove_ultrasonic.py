# Measure the distance or depth with an grove Ultrasonic sound
# sensor and a Raspberry Pi.  Imperial and Metric measurements are available

# Al Audet
# MIT License
from __future__ import division

import time
import math
import warnings
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

TRIG_PIN = 21



class Measurement(object):
    # Create a measurement using a HC-SR04 Ultrasonic Sensor connected to
    # the GPIO pins of a Raspberry Pi.
    # Metric values are used by default. For imperial values use
    # unit='imperial'
    # temperature=<Desired temperature in Fahrenheit>


    def __init__(
        self, trig_pin, temperature=20, unit="metric", gpio_mode=GPIO.BCM
    ):
        self.trig_pin = trig_pin
        self.temperature = temperature
        self.unit = unit
        self.gpio_mode = gpio_mode
        self.pi = math.pi
        self.median_reading = 0
        self.distance_cm = 0
        self.signal_off = 0
        self.signal_on = 0
        self.speed_of_sound = 331.3 * math.sqrt(1 + (self.temperature / 273.15))
        self.sample = []

        # setup input/output pins
        GPIO.setwarnings(False)
        GPIO.setmode(self.gpio_mode)
        # GPIO.setup(self.trig_pin, GPIO.IN)
        # GPIO.add_event_detect(self.trig_pin, GPIO.BOTH, callback = self.detect_edge)

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
        # sample = []
        # time.sleep(sample_wait)
        # GPIO.remove_event_detect(self.trig_pin)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.output(self.trig_pin, GPIO.LOW)
        time.sleep(sample_wait)
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)
        self.signal_on = time.time()
        GPIO.setup(self.trig_pin, GPIO.IN)
        # add event detect is too slow and misses the signal sent and returned
        # GPIO.add_event_detect(self.trig_pin, GPIO.BOTH, callback = self.detect_edge)
        while GPIO.input(self.trig_pin) == 0:
            self.signal_on = time.time()

        while GPIO.input(self.trig_pin) == 1:
            self.signal_off = time.time()
        signal_duration = self.signal_off - self.signal_on

        # lowpass filter version
        # if signal_duration < 0.04:
        #     self.distance_cm = signal_duration * ((self.speed_of_sound * 100) / 2)
        #     print('Distance: {:.1f}cm' .format(self.distance_cm))
        #     self.sample.append(self.distance_cm)

        # no lowpass filter version
        self.distance_cm = signal_duration * ((self.speed_of_sound * 100) / 2)
        print('Distance: {:.1f}cm' .format(self.distance_cm))
        self.sample.append(self.distance_cm)


    def distance(self):
        # Calculate the distance from the sensor to an object.
        self.raw_distance()
        if self.unit == "imperial":
            return self.median_reading * 0.394
        else:
            # don't need this method if using metric. Use raw_distance
            # instead.  But it will return median_reading anyway if used.
            self.median_reading = self.distance_cm
            return self.median_reading

    def detect_edge(self,channel):
        # print("detected edge")
        if GPIO.input(self.trig_pin) == 1:
            self.signal_on = time.time()
        else:
            self.signal_off = time.time()
            signal_duration = self.signal_off - self.signal_on
            if signal_duration < 0.04:
                self.distance_cm = signal_duration * ((self.speed_of_sound * 100) / 2)
                # print('Distance: {:.1f}cm' .format(self.distance_cm))
                self.sample.append(self.distance_cm)

    @staticmethod
    def basic_distance(trig_pin, echo_pin, celsius=20):
        # Return an unformatted distance in cm's as read directly from
        # RPi.GPIO.
        # currently not working

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
    grove = Measurement(TRIG_PIN)
    sample9 = []
    tmp9 = []
    sample7 = []
    tmp7 = []
    sample5 = []
    tmp5 = []
    sample3 = []
    tmp3 = []
    nine_samples = open("nine_samples4.txt", "a")
    seven_samples = open("seven_samples4.txt", "a")
    five_samples = open("five_samples4.txt", "a")
    three_samples = open("three_samples4.txt", "a")
    one_samples = open("one_samples4.txt", "a")

    # how_far = grove.distance()
    # time.sleep(120)
    # GPIO.cleanup()
    try:
        while(True):
            # for i in range(9):
            #     how_far = grove.distance()
            # grove.sample.sort()
            # size_grove_sample = len(grove.sample)
            # sample.append(grove.sample[size_grove_sample//2])
            # grove.sample.clear()
            ###############################
            how_far = grove.distance()


    except KeyboardInterrupt:
        GPIO.cleanup()
        size_all_samples = len(grove.sample)
        for i in range(size_all_samples):
            tmp3.append(grove.sample[i])
            if 2 == i%3:
                size3 = len(tmp3)
                tmp3.sort()
                sample3.append(tmp3[size3//2])
                tmp3.clear()
            tmp5.append(grove.sample[i])
            if 4 == i%5:
                size5 = len(tmp5)
                tmp5.sort()
                sample5.append(tmp5[size5//2])
                tmp5.clear()            
            tmp7.append(grove.sample[i])
            if 6 == i%7:
                size7 = len(tmp7)
                tmp7.sort()
                sample7.append(tmp7[size7//2])
                tmp7.clear()
            tmp9.append(grove.sample[i])
            if 8 == i%9:
                size9 = len(tmp9)
                tmp9.sort()
                sample9.append(tmp9[size9//2])
                tmp9.clear()
        sample3.sort()
        num_bins = 51
        n, bins, patches = plt.hist(sample3, num_bins, facecolor='blue', alpha=0.5)
        plt.savefig("sample3_4.png")
        plt.clf()
        size3 = len(sample3)
        for i in range(size3):
            three_samples.write('Distance: {:.1f}cm\n' .format(sample3[i]))
        three_samples.write('5%: {:.1f}cm\nQuartile: {:.1f}cm\nMedian: {:.1f}cm\nThird quartile: {:.1f}cm\n95%: {:.1f}cm' .format(sample3[size3//20], sample3[size3//4], sample3[size3//2], sample3[size3*3//4], sample3[size3*19//20]))
        three_samples.close()
        sample5.sort()
        num_bins = 51
        n, bins, patches = plt.hist(sample5, num_bins, facecolor='blue', alpha=0.5)
        plt.savefig("sample5_4.png")
        plt.clf()
        size5 = len(sample5)
        for i in range(size5):
            five_samples.write('Distance: {:.1f}cm\n' .format(sample5[i]))
        five_samples.write('5%: {:.1f}cm\nQuartile: {:.1f}cm\nMedian: {:.1f}cm\nThird quartile: {:.1f}cm\n95%: {:.1f}cm' .format(sample5[size5//20], sample5[size5//4], sample5[size5//2], sample5[size5*3//4], sample5[size5*19//20]))
        five_samples.close()
        sample7.sort()
        num_bins = 51
        n, bins, patches = plt.hist(sample7, num_bins, facecolor='blue', alpha=0.5)
        plt.savefig("sample7_4.png")
        plt.clf()
        size7 = len(sample7)
        for i in range(size7):
            seven_samples.write('Distance: {:.1f}cm\n' .format(sample7[i]))
        seven_samples.write('5%: {:.1f}cm\nQuartile: {:.1f}cm\nMedian: {:.1f}cm\nThird quartile: {:.1f}cm\n95%: {:.1f}cm' .format(sample7[size7//20], sample7[size7//4], sample7[size7//2], sample7[size7*3//4], sample7[size7*19//20]))
        seven_samples.close()
        sample9.sort()
        num_bins = 51
        n, bins, patches = plt.hist(sample9, num_bins, facecolor='blue', alpha=0.5)
        plt.savefig("sample9_4.png")
        plt.clf()
        size9 = len(sample9)
        for i in range(size9):
            nine_samples.write('Distance: {:.1f}cm\n' .format(sample9[i]))
        nine_samples.write('5%: {:.1f}cm\nQuartile: {:.1f}cm\nMedian: {:.1f}cm\nThird quartile: {:.1f}cm\n95%: {:.1f}cm' .format(sample9[size9//20], sample9[size9//4], sample9[size9//2], sample9[size9*3//4], sample9[size9*19//20]))
        nine_samples.close()
        # raw samples
        grove.sample.sort()
        num_bins = 51
        n, bins, patches = plt.hist(grove.sample, num_bins, facecolor='blue', alpha=0.5)
        plt.savefig("sample1_4.png")
        plt.clf()
        size = len(grove.sample)
        for i in range(size):
            one_samples.write('Distance: {:.1f}cm\n' .format(grove.sample[i]))
        one_samples.write('5%: {:.1f}cm\nQuartile: {:.1f}cm\nMedian: {:.1f}cm\nThird quartile: {:.1f}cm\n95%: {:.1f}cm' .format(grove.sample[size//20], grove.sample[size//4], grove.sample[size//2], grove.sample[size*3//4], grove.sample[size*19//20]))
        one_samples.close()
        #######################
        # sample.sort()
        # size = len(sample)
        # for i in range(size):
        #     print('Distance: {:.1f}cm' .format(sample[i]))
        # print('5%: {:.1f}cm\nQuartile: {:.1f}cm\nMedian: {:.1f}cm\nThird quartile: {:.1f}cm\n95%: {:.1f}cm' .format(sample[size//20], sample[size//4], sample[size//2], sample[size*3//4], sample[size*19//20]))