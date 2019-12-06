import RPi.GPIO as GPIO
from RpiMotorLib.rpi_dc_lib import TB6612FNGDc
from time import sleep
from PID import *

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
def MAX_SPEED(): return 300 #max predkosc silnika w obrotach na minute nie wiem jaka bedzie wiec narazie 300
def MAX_PWM(): return 100 #w razie gdybysmy nie mogli wykorzystywac maksymalnego bo costam

class motors_movement():
    left_motor = TB6612FNGDc(AIN1(),AIN2(),PWMA(),FREQ())
    right_motor = TB6612FNGDc(BIN1(),BIN2(),PWMB(),FREQ())
    pid = PID()
    
    def move_forth(self,speed): #speed to zadana wartosc predkosci
        feedback1 = encoder(1) #to jak dostane funkcje ktora zwraca predkosc silnika1 sczytana z enkodera
        feedback2 = encoder(2) #to jak dostane funkcje ktora zwraca predkosc silnika1 sczytana z enkodera
        self.pid.SetPoint=feedback1
        self.pid.update(feedback2) #zakladamy ze dosterowujemy silnik2 tak zeby dzialal jak silnik1
        second_motor_speed=(feedback2+self.pid.output)*MAX_PWM()/MAX_SPEED()
        if second_motor_speed>100: #wiecej niz 100% nie da rady
            second_motor_speed=100
        self.left_motor.forward(speed)
        self.right_motor.forward(second_motor_speed) #yyy??? do sprawdzenia
        #zamysl jest taki zeby bralo predkosc dodawalo wyliczone wyjscie pidu mnozylo razy MAX_PWM czyli 100 i dzielilo na max predkosc
        #tylko czy tak powinien dzialac pid? pogubilem sie chyba

    def move_back(self,speed): #speed to zadana wartosc predkosci
        feedback1 = encoder(1) #to jak dostane funkcje ktora zwraca predkosc silnika1 sczytana z enkodera
        feedback2 = encoder(2) #to jak dostane funkcje ktora zwraca predkosc silnika1 sczytana z enkodera
        self.pid.SetPoint=feedback1
        self.pid.update(feedback2) #zakladamy ze dosterowujemy silnik2 tak zeby dzialal jak silnik1
        second_motor_speed=(feedback2+self.pid.output)*MAX_PWM()/MAX_SPEED()
        if second_motor_speed>100: #wiecej niz 100% nie da rady
            second_motor_speed=100
        self.left_motor.backward(speed)
        self.right_motor.backward(second_motor_speed) #yyy??? do sprawdzenia
        #zamysl jest taki zeby bralo predkosc dodawalo wyliczone wyjscie pidu mnozylo razy MAX_PWM czyli 100 i dzielilo na max predkosc
        #tylko czy tak powinien dzialac pid? pogubilem sie chyba
