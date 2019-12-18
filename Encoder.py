import RPi.GPIO as GPIO
from time import time, sleep
from constant_values import *


# pin numbers
ENCODER1_A_PIN = 23
ENCODER1_B_PIN = 24
ENCODER2_A_PIN = 27
ENCODER2_B_PIN = 17


class Encoder:

    def __init__(self, pin_a, pin_b):
        self.clk = pin_a
        self.dt = pin_b
        self.clear()
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.clk, GPIO.BOTH, callback=self.pulse)
        GPIO.add_event_detect(self.dt, GPIO.BOTH, callback=self.pulse)

    def clear(self):
        self.rotaryLastState = None
        self.clkLevel = 0
        self.dtLevel = 0
        self.counter = 0
        self.prev_time = None
        self.speed = None

    def pulse(self, channel):
        clk_state = GPIO.input(self.clk)
        dt_state = GPIO.input(self.dt)
        if clk_state != self.rotaryLastState:
            self.rotaryLastState = clk_state
            if dt_state != clk_state:
                current_time = time()
                if self.prev_time is not None:
                    self.speed = 60/(current_time-self.prev_time)
                    # revolutions per minute assuming 1 tick per revolution
                    print(self.speed)
                self.prev_time = current_time
                # self.counter += 1
                # print (self.counter)
            else:
                current_time = time()
                if self.prev_time is not None:
                    self.speed = -60/(current_time-self.prev_time)
                    # revolutions per minute assuming 1 tick per revolution
                    # minus because moving backward
                    print(self.speed)
                self.prev_time = current_time
                # self.counter -= 1
                # print(self.counter)



if __name__ == "__main__":
    encoder1 = Encoder(23, 24)
    try:
        sleep(1000)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("im over")