import RPi.GPIO as gpio

NONE  = 0
UP    = 1
DOWN  = 2
LEFT  = 3
RIGHT = 4
MANY  = 5

PRESSED   = 1
UNPRESSED = 0

"""
Connections are:

Joystick:

   The corner that the wires come out of is the top left

   black   - gnd
   green   - GPIO 25
   yellow  - GPIO CE0
   orange  - GPIO CE1
   red     - GPIO CLK

Button:
   comm          - gnd
   normally open - GPIO 24

"""

class Joystick(object):
   def __init__(self):
      self.UP_PIN    = 26
      self.DOWN_PIN  = 23
      self.LEFT_PIN  = 24
      self.RIGHT_PIN = 22
      gpio.setmode(gpio.BOARD)
      gpio.setup(self.UP_PIN,    gpio.IN, pull_up_down=gpio.PUD_UP)
      gpio.setup(self.DOWN_PIN,  gpio.IN, pull_up_down=gpio.PUD_UP)
      gpio.setup(self.LEFT_PIN,  gpio.IN, pull_up_down=gpio.PUD_UP)
      gpio.setup(self.RIGHT_PIN, gpio.IN, pull_up_down=gpio.PUD_UP)

   def read(self):
      up    = (gpio.input(self.UP_PIN)    == 0)
      down  = (gpio.input(self.DOWN_PIN)  == 0)
      left  = (gpio.input(self.LEFT_PIN)  == 0)
      right = (gpio.input(self.RIGHT_PIN) == 0)

      if   up    and not (left or right):
         return UP
      elif down  and not (left or right):
         return DOWN
      elif left  and not (up or down):
         return LEFT
      elif right and not (up or down):
         return RIGHT
      elif (left or right) and (up or down):
         return MANY
      else:
         return NONE

class Button(object):
   def __init__(self):
      self.PIN = 18
      gpio.setmode(gpio.BOARD)
      gpio.setup(self.PIN, gpio.IN, pull_up_down=gpio.PUD_UP)

   def read(self):
      return PRESSED if gpio.input(self.PIN) == 0 else UNPRESSED


from time import sleep
def main():
   dir_names = {UP:"up", LEFT:"left", RIGHT:"right", DOWN:"down", NONE:"none"}

   j = Joystick()

   while True:
      x = j.read()
      print x
      sleep(0.1)
      
if __name__ == '__main__':
   try:
      main()
   except KeyboardInterrupt:
      gpio.cleanup()
