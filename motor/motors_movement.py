import RPi.GPIO as GPIO
from RpiMotorLib.rpi_dc_lib import TB6612FNGDc
from time import sleep

#------------------------------------#
# nazwy i numery pinow jak w mostku
#------------------------------------#
def AIN1(): return 13
def AIN2(): return 19
def PWMA(): return 26
def BIN1(): return 21
def BIN2(): return 20
def PWMB(): return 16
def FREQ(): return 50

class motors_movement():
    left_motor = TB6612FNGDc(AIN1(),AIN2(),PWMA(),FREQ())
    right_motor = TB6612FNGDc(BIN1(),BIN2(),PWMB(),FREQ())
    
    def move_forth(self,pwm1=30, pwm2=30):
        self.left_motor.forward(pwm1)
        self.right_motor.forward(pwm1)

    def move_back(self,pwm1=30, pwm2=30):
        self.left_motor.backward(pwm1)
        self.right_motor.backward(pwm1)

    def turn_left(self,pwm1=30, pwm2=30):
        self.left_motor.backward(pwm1)
        self.right_motor.forward(pwm1)

    def turn_right(self,pwm1=30, pwm2=30):
        self.left_motor.forward(pwm1)
        self.right_motor.backward(pwm1)

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
#test()
