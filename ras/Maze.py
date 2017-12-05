# -*- coding: utf-8 -*-

from ForWardModule import *
from TurnModule import rightPointTurn, leftPointTurn
from Tracking import track
import RPi.GPIO as GPIO
from time import sleep

speed = 15


def lineTrace():
    go_forward_nosleep(speed)
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
    try:
        if led_list[0] and led_list[1] and led_list[2] and led_list[3] and led_list[4]:
            stop()
            go_forward(30, 0.4)
            doing_U_turn()
            return

        if (led_list[0] and led_list[1]) and not (led_list[2] and led_list[3] and led_list[4]):
            stop()
            go_forward(30, 0.4)
            while True:
                led_list = track()
                if led_list[3]:
                    rightPointTurn(30, 0.5)
                else:
                    return
            return  # 오른쪽만 있는 교차로
        elif (led_list[3] and led_list[4]) and not (led_list[0] and led_list[1] and led_list[2]):
            stop()
            go_forward(30, 0.4)
            while True:
                led_list = track()
                if led_list[1]:
                    leftPointTurn(30, 0.5)
                else:
                    return
            return  # 왼쪽만 있는 교차로
        elif not (led_list[0] and led_list[1] and led_list[2] and led_list[3] and led_list[4]):
            stop()
            go_forward(30, 0.4)
            while True:
                led_list = track()
                if led_list[3]:
                    rightPointTurn(30, 0.5)
                else:
                    return
            return  # 양갈래길 교차로

    except KeyboardInterrupt:
        stopCar()
    GPIO.cleanup()


def doing_U_turn():
    try:
        while True:
            led_list = track()

            if led_list[2]:
                rightPointTurn(30, 0.05)
            else:
                return

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
