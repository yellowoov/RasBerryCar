# -*- coding: utf-8 -*-

from ForWardModule import *
from TurnModule import rightPointTurn, leftPointTurn
from ultraModule import getDistance
from Tracking import track
import RPi.GPIO as GPIO
from time import sleep

speed = 20


def avoid():
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
