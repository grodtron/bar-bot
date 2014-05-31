#!/usr/bin/python2

import RPi.GPIO as gpio
from time import sleep

def main():
	gpio.setmode(gpio.BCM)
	gpio.setup(23, gpio.IN, pull_up_down=gpio.PUD_UP)

	print "Waiting for button press..."

	while gpio.input(23):
		sleep(0.1)

	print "Button Pressed!"


if __name__ == "__main__":
	main()
