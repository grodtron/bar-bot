# TODO UNCOMMENT TESTING import smbus

from models    import Slot
from scheduler import get_movement_schedule
from math      import ceil

from operator  import xor
from time import time, sleep

DISPENSE_SHOT      = 0
DISPENSE_FREE_POUR = 1
DISPENSE_NO_POUR   = 2

ROTATION_CW        = 0
ROTATION_CCW       = 1
ROTATION_NONE      = 2

LED_MODE_RAMP      = 0
LED_MODE_SOLID     = 1
LED_MODE_BLINK     = 2

LED_COLOR_OFF      = 0
LED_COLOR_BOTTLE_1 = 1
LED_COLOR_BOTTLE_2 = 2
LED_COLOR_BOTTLE_3 = 3
LED_COLOR_BOTTLE_4 = 4
LED_COLOR_BOTTLE_5 = 5
LED_COLOR_BOTTLE_6 = 6
LED_COLOR_RAINBOW  = 7
LED_COLOR_WHITE    = 8

class CommandFailedException(Exception):
   pass

# Base class for I2C Commands, takes care of sending them and checking for the
# good response.
#
# subclasses must provide ._get_buffer() returning the list of bytes to send
class I2CCommand(object):
   def __init__(self, bus):
      self.bus = bus

   def execute(self):
      buff = self._get_buffer()

      response = 0
      attempts  = 0
      while response == 0 and attempts < 5:
         try:
            self.bus.write_i2c_block_data(self.addrs[n], buff[0], buff[1:])
            response = self.bus.read_byte_data(self.addrs[n], 2)
         except Exception as e:
            raise CommandFailedException("Could not communicate with Arduino (%s)", str(e))

         attempts += 5

      if response == 0:
         raise CommandFailedException("Could not communicate with Arduino after %d tries (bad csum)" % attempts)
      else:
         self._estimated_time_left = response

   def remaining_time(self):
      # TODO - poll on i2c each time for this
      return self._estimated_time_left
      
# Substitute base class for I2CCommand for non-rpi testing
# just prints out instead of attempting any i2c stuff
class TestCommand(object):
   def __init__(self, bus):
      self.bus = bus
      self.duration   = 1

   def execute(self):
      buff = self._get_buffer()

      print "Exectuing i2c command!!: %s" % str(buff)

      # update duration
      self.duration = buff[3] # pour amount

      self.start = time()

   def executing(self):
      try:
         time_rem = int(ceil( max(0, self.duration - (time() - self.start)) ))
         print "Time remaining =",time_rem
         return time_rem > 0
      except AttributeError:
         return False

   def remaining_time(self):
      try:
         return int(ceil( max(0, self.duration - (time() - self.start)) ))
      except AttributeError:
         return int(self.duration)

# TODO change back to I2CCommand for non-testing purposes
class PouringCommand(TestCommand):

   def __init__(self, bus, **kwargs):
      super(PouringCommand, self).__init__(bus)
      self.bus = bus
      self.bottle_delta  = kwargs["bottle_delta"]
      self.dispense_type = kwargs["dispense_type"]
      self.pour_amount   = kwargs["pour_amount"]
      self.rotation      = kwargs["rotation"]
      self.led_mode      = kwargs["led_mode"]
      self.led_color     = kwargs["led_color"]
   
   def _get_buffer(self):
      try:
         return self._buff
      except AttributeError:
         self._make_buffer()
         return self._buff

   def _make_buffer(self):
      buff = [ 0,
               self.bottle_delta  % 256,
               self.dispense_type % 256,
               self.pour_amount   % 256,
               self.rotation      % 256,
               self.led_mode      % 256,
               self.led_color     % 256]

      buff.append(reduce(xor, buff))

      self._buff = buff
      

# Command to be used to delay the pouring of a drink. Just keeps track of the time and
# sits there waiting
class DelayCommand(object):
   
   def __init__(self, duration):
      self.duration = duration

   def execute(self):
      print "Starting delay command with duration:", self.duration
      self.start = time()


   # throws an AttributError if we haven't started yet
   def _raw_get_time_remaining(self):
         return int(ceil( max(0, self.duration - (time() - self.start)) ))

   def executing(self):
      try:
         return self._raw_get_time_remaining()
      except AttributeError:
         return False

   def remaining_time(self):
      try:
         return self._raw_get_time_remaining()
      except AttributeError:
         return int(self.duration)



class PourManager(object):

   def __init__(self):
      self.pouring          = False
      self.current_position = {1:Slot(1,1), 2:Slot(2,1)}
      self.current_schedule = None
      self.current_commands = {1:None, 2:None}
      self.current_executing_command = {1:None, 2:None}
      self.commands         = None
      self.addrs            = {1:4, 2:6}

      self.bus = smbus.SMBus(1)

   def pour_drink(self, Drink):
      self.pouring = True

      self.current_schedule = get_movement_schedule(Drink, self.current_position)

      self._process_spire(1)
      self._process_spire(2)
   
      self._do_next_command(1)
      if len(self.current_commands[1]):
         self.current_commands[2].append(DelayCommand( 
            self.current_commands[1][-1].remaining_time()
            ))
      self._do_next_command(2)


   def update(self):
      self._do_next_command(1)
      self._do_next_command(2)

   def _do_next_command(self, n):
      if (len(self.current_commands[n])
            and (
                  (not self.current_executing_command[n])
                  or
                  (not self.current_executing_command[n].executing())
                 )
      ):
         print time(),"Do next command %d" % n
         self.current_executing_command[n] = self.current_commands[n].pop()
         self.current_executing_command[n].execute()

   def _process_spire(self, n):
      curr_slot = self.current_position[n].position

      commands = []
      for slot_amt in self.current_schedule[n]:
         slot      = slot_amt.slot.position

         # Get the shortest distance from where we currently
         # are, as well as the direction of the rotation
         d = slot - curr_slot
         dir = d < 0
         if abs(d) > 3:
            dir = not dir
            d = 6 - abs(d)
         else:
            d = abs(d)

         rotation_delta = d
         rotation_dir   = (ROTATION_CCW if dir else ROTATION_CW)

         command = PouringCommand(
            self.bus,
            bottle_delta  = rotation_delta,
            dispense_type = DISPENSE_SHOT,
            pour_amount   = slot_amt.amount,
            rotation      = rotation_dir,
            led_mode      = LED_MODE_SOLID,
            led_color     = LED_COLOR_RAINBOW
         )

         commands.append(command)

         curr_slot = slot
      
      # Reverse the list we just built because in the end these commands
      # Will be popped off one by one, but the list that we just built has the
      # first command at position 0
      #print "setting current commands [%d] to :%s" % (n, str(commands.reverse()))
      commands.reverse()
      self.current_commands[n] = commands


def main():
   """
   cmd = PouringCommand(
            bottle_delta  = 3,
            dispense_type = DISPENSE_SHOT,
            pour_amount   = 2,
            rotation      = ROTATION_CW,
            led_mode      = LED_MODE_RAMP,
            led_color     = LED_COLOR_OFF)

   bus = smbus.SMBus(1)

   buff = cmd.get_buffer()

   print "Trying:"
   bus.write_i2c_block_data(6, buff[0], buff[1:])
   print "Done sending command"

   sleep(1)
   
   print "Getting reply"
   result = bus.read_byte_data(6, 2)
   print "got reply, which was:", result
   """

   from scheduler import SlotAmount

   sched = {1:[
         SlotAmount(Slot(1, 2), 2),
         SlotAmount(Slot(1, 5), 1)
      ],
      2:[
         SlotAmount(Slot(2, 1), 3),
         SlotAmount(Slot(2, 6), 1)
         ]}
   
   pm = PourManager()
   pm.current_schedule = sched

   pm.pour_drink(None)

   while True:
      pm.update()
      sleep(0.5)


if __name__ == '__main__':
   main()
