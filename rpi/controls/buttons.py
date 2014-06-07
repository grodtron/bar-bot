NONE  = 0
UP    = 1
DOWN  = 2
LEFT  = 3
RIGHT = 4

PRESSED   = 1
UNPRESSED = 0

def read_joystick():
   s = raw_input("input joystick as w-a-s-d: ")
   print "got >>>>%s<<<<" % s
   if   s == "w":
      print "returning UP"
      return UP
   elif s == "a":
      print "returning LEFT"
      return LEFT
   elif s == "s":
      print "returning DOWN"
      return DOWN
   elif s == "d":
      print "returning RIGHT"
      return RIGHT
   else:
      print "returning NONE"
      return NONE

def read_button():
   s = raw_input("Enter button, empty string is unpressed")
   if len(s):
      return PRESSED
   else:
      return UNPRESSED
