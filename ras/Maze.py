# -*- coding: utf-8 -*-

from ForWardModule import *
from TurnModule import rightPointTurn, leftPointTurn
from Tracking import track
import RPi.GPIO as GPIO
from time import sleep

speed = 15


def lineTrace():
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
