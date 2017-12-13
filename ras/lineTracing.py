# -*- coding: utf-8 -*-

from ForWardModule import *
from TurnModule import rightPointTurn, leftPointTurn
from ultraModule import getDistance
from Tracking import track
import RPi.GPIO as GPIO
from time import sleep

speed = 20


def avoid():
    '''
    장애물을 회피하기 위한 avoid 함수입니다.
    장애물을 만나면 모터 속도를 0으로 만들고 1초 동안 멈춘 뒤,
    오른쪽으로 포인트턴, 1초 쉬고 조금 앞으로 전진했다가
    왼쪽으로 포인트턴을 진행하여 장애물을 회피합니다.
    그리고 다시 라인을 따라 라인트레이싱을 진행합니다.
    '''


        try:
            LeftPwm.ChangeDutyCycle(0)
            RightPwm.ChangeDutyCycle(0)
            sleep(1)
            rightPointTurn(30, 1)
            sleep(1)
            go_forward(30, 1.5)
            leftPointTurn(30, 2)
            sleep(1)
            go_forward_nosleep(speed)

        except KeyboardInterrupt:
            stop()
            GPIO.cleanup()


    def lineTrace():
        '''
        라인 트레이싱을 하기 위한 lineTrace함수입니다.
        led_list라는 변수에 Tracking모듈에서 리턴받은 튜플 값을 받아옵니다.

        5방향 센서의 5개 센서를 왼쪽부터 0,1,2,3,4번이라고 했을 때,
        0번이 True이고 4번이 False이면 왼쪽 바퀴의 속도를 올려 오른쪽으로 턴하고
        1번이 True이고 3번이 False이면 왼쪽 바퀴의 속도를 올려 오른쪽으로 턴합니다.

        3번이 True이고 1번이 False이면 오른쪽 바퀴의 속도를 올려 왼쪽으로 턴하고
        4번이 True이고 0번이 False이면 오른쪽 바퀴의 속도를 올려 왼쪽으로 턴합니다.
        '''
        GPIO.output(MotorLeft_A, GPIO.HIGH)
        GPIO.output(MotorLeft_B, GPIO.LOW)
        GPIO.output(MotorRight_A, GPIO.LOW)
        GPIO.output(MotorRight_B, GPIO.HIGH)
        # while True:
        try:
            led_list = track()

            if led_list[0] and not (led_list[4]):
                # print 'a'
                LeftPwm.ChangeDutyCycle(speed + 75)
                RightPwm.ChangeDutyCycle(speed)
            if led_list[1] and not (led_list[3]):
                # print 'b'
                LeftPwm.ChangeDutyCycle(speed + 65)
                RightPwm.ChangeDutyCycle(speed)
            if led_list[3] and not (led_list[1]):
                # print 'c'
                LeftPwm.ChangeDutyCycle(speed)
                RightPwm.ChangeDutyCycle(speed + 40)
            if led_list[4] and not (led_list[0]):
                # print 'd'
                LeftPwm.ChangeDutyCycle(speed)
                RightPwm.ChangeDutyCycle(speed + 60)

        except KeyboardInterrupt:
            stop()
            GPIO.cleanup()


    def start():
        '''
        직선 주행할 때는 계속 앞으로 직선 주행하다가
        초음파 센서를 통해 거리를 계속 재면서 장애물과의 거리가 22보다 크면 라인 트레이싱을 진행하고
        22보다 작으면 장애물 회피를 진행합니다.
        '''
        go_forward_nosleep(speed)
        while True:
            a = getDistance()
            if a > 22:
                lineTrace()
            else:
                avoid()

    if __name__ == "__main__":

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(MotorLeft_A, GPIO.OUT)
        GPIO.setup(MotorLeft_B, GPIO.OUT)
        GPIO.setup(MotorLeft_PWM, GPIO.OUT)

        GPIO.setup(MotorRight_A, GPIO.OUT)
        GPIO.setup(MotorRight_B, GPIO.OUT)
        GPIO.setup(MotorRight_PWM, GPIO.OUT)
        # 과제 진행
        try:
            LeftPwm.start(0)
            RightPwm.start(0)
            go_forward(speed, 0.3)
            start()
            # start2()

        except KeyboardInterrupt:
            stop()
            GPIO.cleanup()
