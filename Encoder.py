import RPi.GPIO as GPIO
from time import time, sleep
import threading
from constant_values import *

class Encoder: 
    def __init__(self,pin_a):
        self.window=[]
        self.sum = 0
        self.speed = 0.0

        self.thread = threading.Thread(target=self.time_thread)
        self.thread.start()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_a, GPIO.IN,pull_up_down=GPIO.PUD_UP)
       
 
        GPIO.add_event_detect(pin_a, GPIO.BOTH, callback=self.peak_event)

    def add_sample(self,sample):
        if len(self.window) == NUM_OF_SAMPLES :
            self.window.pop(0)
            self.window.append(sample)
        else:
            self.window.append(sample)

    def time_thread(self):
        while True:
            sleep(WINDOW_LENGTH)
            self.process_window()

    def process_window(self):
       self.add_sample(self.sum * TRANSMISSION_FACTOR)
       self.speed = self.sum/TRANSMISSION_FACTOR/WINDOW_LENGTH
       # print(speed)
       self.sum = 0.0
       
    def peak_event(self,channel):
        self.sum += 1

    def clear(self):
        self.sum = 0
        self.speed = 0.0

if __name__ == "__main__": 
    e = Encoder()
    e._init(37)
    try:
        sleep(60)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("im over")



# import RPi.GPIO as GPIO
# from time import time, sleep
# from constant_values import *




# class Encoder:

#     def __init__(self, pin_a, pin_b):
#         self.clk = pin_a
#         self.dt = pin_b
#         self.clear()
        
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#         GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#         GPIO.add_event_detect(self.clk, GPIO.RISING, callback=self.pulse_no_direction)
#         GPIO.add_event_detect(self.dt, GPIO.RISING, callback=self.pulse_no_direction)

#     def clear(self):
#         self.rotaryLastState = None
#         self.clkLevel = 0
#         self.dtLevel = 0
#         self.counter = 0
#         # self.prev_time = None
#         self.prev_time = time()
#         self.speed = None

#     def pulse(self, channel):
#         clk_state = GPIO.input(self.clk)
#         dt_state = GPIO.input(self.dt)
#         if clk_state != self.rotaryLastState:
#             self.rotaryLastState = clk_state
#             if dt_state != clk_state:
#                 current_time = time()
#                 if self.prev_time is not None:
#                     # revolutions per minute assuming 1 tick per revolution
#                     self.speed = 60/(current_time-self.prev_time)
#                     # print('{:3f}'.format(current_time-self.prev_time), end='\t')
#                     print('{:3f}' .format(self.speed))
#                 self.prev_time = current_time
#                 # self.counter += 1
#                 # print (self.counter)
#             else:
#                 current_time = time()
#                 if self.prev_time is not None:
#                     # revolutions per minute assuming 1 tick per revolution
#                     # minus because moving backward
#                     self.speed = -60/(current_time-self.prev_time)
#                     # print('{:3f}'.format(current_time-self.prev_time), end='\t')
#                     print('{:3f}'.format(self.speed))
#                 self.prev_time = current_time
#                 # self.counter -= 1
#                 # print(self.counter)


#     def pulse_no_direction(self,channel):
#         # for event detect do only RISING/FALLING never both
#         current_time = time()
#         self.counter+=self.counter
#         if current_time-self.prev_time>ENC_MEASUR_TIME:
#             self.prev_time = current_time
#             self.speed = counter/ENC_MEASUR_TIME # revolutions/sec
#             counter = 0
#             print('{:3f}' .format(self.speed))
#         self.prev_time = current_time



# if __name__ == "__main__":
#     encoder1 = Encoder(23, 24)
#     try:
#         sleep(1000)
#     except KeyboardInterrupt:
#         GPIO.cleanup()
#         print("im over")
