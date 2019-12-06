import RPi.GPIO as GPIO
import time


MAX_PWM = 9 
MIN_PWM = 3
FREQ = 50
SINGLE_POS_CHANGE = 10
SERVO_PIN = 4

class servo:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self.pin = GPIO.PWM(SERVO_PIN, FREQ)
        self.pin.start((MAX_PWM-MIN_PWM)/2+MIN_PWM) # servo starts by positioning to center
        self.current_position = 90

    def pos_to_pwm(self, servo_pos):
        my_pwm = servo_pos*(MAX_PWM-MIN_PWM)/180+MIN_PWM 
        return my_pwm

    def servo_position(self, servo_pos=90):
        servo_pwm = self.pos_to_pwm(servo_pos)
        self.pin.ChangeDutyCycle(servo_pwm)
        self.current_position = servo_pos
        #time.sleep(1)   # those 2 lines are in case of servo vibrations
        #p.ChangeDutyCycle(0)

    def move_up(self):
        self.current_position += 10
        self.servo_position(self.current_position)

    def move_down(self):
        self.current_position -= 10
        self.servo_position(self.current_position)


def test():
    my_servo = servo()
    time.sleep(2)
    for i in range(5):
        my_servo.move_up()
        time.sleep(0.5)
    for i in range(10):
        my_servo.move_down()
    time.sleep(2)
    GPIO.cleanup()

#test()
