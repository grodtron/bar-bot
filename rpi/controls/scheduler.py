from models import Drink, Slot
from operator import attrgetter

def get_usable_slots(ingredient):
   max_delta = 3

   slots = ingredient.slots

   if len(slots) == 1:
      return slots.keys()[0]
   else:
      min_used = max_used = slots.keys()[0]
      for key in slots.keys():
         if slots[key] < slots[min_used]:
            min_used = key
         if slots[key] > slots[max_used]
            max_used = key

      if slots[min_used] + 3 < slots[max_used]:
         ingredient.inc_use_count(min_used)
         return min_used

def choose_slot_and_inc_use_count(ingredient, curr_slot):
         ingredient.inc_use_count(min_used)
         return min_used

      def dist(x, y):
         # circular distance between two indexes in a circle.
         # That doesn't make sense, but you know what I'm talking about.
         return min(abs(x - y), abs(x - (y+6)), abs(x-(y-6)))



def get_movement_schedule(drink, current_position):
   class SlotAmount(object):
      def __init__(self, slot, amount):
         self.slot   = slot
         self.amount = amount


   # For each ingredient in the drink, get the available slots we could pour
   # from. Available slots are those containing the drink which are not overused.
   # If any drink has more than X less in it than another, it is excluded, to avoid
   # overusing any particular drink.
   
   spire = {1:[], 2:[]}

   for entry in drink.ingredients:
      for slot in get_usable_slots(entry.ingredient):
         spire[slot.spire].append(SlotAmount(slot, entry.amount))

   spire[1] = sorted(spire[1], key=attrgetter("amount"))
   spire[2] = sorted(spire[2], key=attrgetter("amount"))

   return spire

   
