import RPi.GPIO as GPIO
from RpiMotorLib.rpi_dc_lib import TB6612FNGDc
from time import sleep
from constant_values import *

#------------------------------------#
# nazwy i numery pinow jak w mostku
#------------------------------------#


class motors_movement():
    left_motor = TB6612FNGDc(AIN1, AIN2, PWMA, FREQUENCY)
    right_motor = TB6612FNGDc(BIN1, BIN2, PWMB, FREQUENCY)
    
    def move_forth(self,pwm1=STANDARD_PWM1, pwm2=STANDARD_PWM2):
        self.left_motor.forward(pwm1)
        self.right_motor.backward(pwm2)

    def move_back(self,pwm1=STANDARD_PWM1, pwm2=STANDARD_PWM2):
        self.left_motor.backward(pwm1)
        self.right_motor.forward(pwm2)

    def turn_left(self,pwm1=STANDARD_PWM1, pwm2=STANDARD_PWM2):
        self.left_motor.backward(pwm1)
        self.right_motor.backward(pwm2)

    def turn_right(self,pwm1=STANDARD_PWM1, pwm2=STANDARD_PWM2):
        self.left_motor.forward(pwm1)
        self.right_motor.forward(pwm2)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
        
    def pin_cleanup(self):
        self.left_motor.cleanup(True)
        

def test():
    motors=motors_movement()
    sleep(2)
    motors.move_forth(20)
    sleep(2)
    motors.move_back(20)
    sleep(2)
    motors.turn_left(20)
    sleep(2)
    motors.turn_right(20)
    sleep(2)
    motors.stop()
    motors.pin_cleanup()

if __name__ == "__main__":
    test()
