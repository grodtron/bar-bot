import smbus

from scheduler import get_movement_schedule
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

class PouringCommand(object):

   def __init__(self, **kwargs):
      self.bottle_delta  = kwargs["bottle_delta"]
      self.dispense_type = kwargs["dispense_type"]
      self.pour_amount   = kwargs["pour_amount"]
      self.rotation      = kwargs["rotation"]
      self.led_mode      = kwargs["led_mode"]
      self.led_color     = kwargs["led_color"]

   def get_buffer(self):
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
      #buff.append(0)

      self._buff = buff
      


class PourManager(object):

   def __init__(self):
      self.pouring          = False
      self.executing        = {1:False, 2:False}
      self.current_command  = {1:None, 2:None}
      self.current_position = {1:Slot(1,1), 2:Slot(2,1)}
      self.current_schedule = None
      self.addrs            = {1:4, 2:6}
      self.complete_at      = 0

      self.bus = smbus.SMBus(1)

   def pour_drink(self, Drink):
      self.pouring = True

      self.current_schedule = get_movement_schedule(Drink, self.current_position)

      self._process_spire(1)
      self._process_spire(2)

      self._do_command(1)
      self._do_command(2)
   

   def update(self):
      if time() > self.complete_at:
         self.pouring = False 

   def _do_command(self, n):
      if self.current_command[n] and not self.executing[n]:

         buff = self.current_command[n].get_buffer()

         self.bus.write_i2c_block_data(self.addrs[n], buff[0], buff[1:])
         response = self.bus.read_byte_data(self.addrs[n], 2)

         if response == 0:
            print "Bad Checksum!!!"
         else:
            self.executing[n] = True
            self.complete_at = max(time() + response, self.complete_at)
            print "Received response, command will take",response,"seconds"
         

   def _process_spire(self, n):
      if len(self.current_schedule[n]):
         slot_amt  = self.current_schedule[n].pop()

         slot      = slot_amt.slot.slot
         curr_slot = self.current_position[n].slot

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

         self.current_command[n] = PouringCommand(
            bottle_delta  = rotation_delta,
            dispense_type = DISPENSE_SHOT,
            pour_amount   = slot.amt.amount,
            rotation      = rotation_dir,
            led_mode      = LED_MODE_SOLID,
            led_color     = LED_COLOR_RAINBOW
         )
      else:
         self.current_command[n] = None
      




def main():
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


if __name__ == '__main__':
   main()
