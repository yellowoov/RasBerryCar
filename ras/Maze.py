# -*- coding: utf-8 -*-

from ForWardModule import *
from TurnModule import rightPointTurn, leftPointTurn
from Tracking import track
import RPi.GPIO as GPIO
from time import sleep

speed = 15


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
    go_forward_nosleep(40)
    while True:
        try:
            led_list = track()  # Black = 0, White = 1

            if led_list[0] and not (led_list[4]):
                LeftPwm.ChangeDutyCycle(speed + 75)
                RightPwm.ChangeDutyCycle(speed)
            if led_list[1] and not (led_list[3]):
                LeftPwm.ChangeDutyCycle(speed + 65)
                RightPwm.ChangeDutyCycle(speed)
            if led_list[3] and not (led_list[1]):
                LeftPwm.ChangeDutyCycle(speed)
                RightPwm.ChangeDutyCycle(speed + 40)
            if led_list[4] and not (led_list[0]):
                LeftPwm.ChangeDutyCycle(speed)
                RightPwm.ChangeDutyCycle(speed + 60)

            mazeSearch(led_list)

        except KeyboardInterrupt:
            stop()
            GPIO.cleanup()


def mazeSearch(led_list):
    '''
    미로 찾기를 하기 위한 mazeSearch 함수입니다.
    
    5방향 센서의 5개 센서를 왼쪽부터 0,1,2,3,4번이라고 했을 때,
    모두 True일 때, 유턴을 합니다.
    
    0번과 1번이 True, 3번과 4번이 False일 때,
    오른쪽으로 턴합니다.
    
    0번과 1번이 False, 3번과 4번이 True일 때,
    왼쪽으로 턴합니다.
    
    모두 False일 때, 우수법 때문에
    오른쪽으로 턴합니다.
    
    모든 턴은 진행하기 전에 조금 앞으로 전진했다가 턴합니다.
    '''
    try:
        if led_list[0] and led_list[1] and led_list[2] and led_list[3] and led_list[4]:
            print("u")
            print(led_list)
            stop()
            sleep(1)
            go_forward(37, 0.5)
            rightPointTurn(28, 0.5)
            while True:
                inner_led_list = track()
                print(inner_led_list)
                if not inner_led_list[2]:
                    go_forward_nosleep(40)
                    return 0
                else:
                    leftPointTurn(40, 0.25)

        elif led_list[0] and led_list[1] and not led_list[3] and not led_list[4]:
            print("right")
            print(led_list)
            stop()
            sleep(1)
            go_forward(37, 0.5)
            rightPointTurn(28, 0.5)
            while True:
                inner_led_list = track()
                print(inner_led_list)
                if not inner_led_list[2]:
                    go_forward_nosleep(40)
                    return 1
                else:
                    rightPointTurn(40, 0.25)

        elif not led_list[0] and not led_list[1] and led_list[3] and led_list[4]:
            print("left")
            print(led_list)
            stop()
            sleep(1)
            go_forward(37, 0.5)
            leftPointTurn(28, 0.5)
            while True:
                inner_led_list = track()
                print(inner_led_list)
                if not inner_led_list[2]:
                    go_forward_nosleep(40)
                    return 2
                else:
                    leftPointTurn(40, 0.25)

        elif not led_list[0] and not led_list[1] and not led_list[2] and not led_list[3] and not led_list[4]:
            print("all")
            print(led_list)
            stop()
            sleep(1)
            go_forward(37, 0.5)
            rightPointTurn(28, 0.5)
            while True:
                inner_led_list = track()
                print(inner_led_list)
                if not inner_led_list[2]:
                    go_forward_nosleep(40)
                    return 3
                else:
                    rightPointTurn(40, 0.25)

    except KeyboardInterrupt:
        stop()
        GPIO.cleanup()


if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    try:
        LeftPwm.start(0)
        RightPwm.start(0)
        go_forward(speed, 0.3)
        lineTrace()

    except KeyboardInterrupt:
        stop()
        GPIO.cleanup()
