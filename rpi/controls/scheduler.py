from models import Drink, Slot
from operator import attrgetter

# Return usable slots for a given ingredient. This method simply
# filters out any slots that have been overused, forcing the usage
# to be spread roughly equally across duplicate bottles.
def get_usable_slot(ingredient):
   max_delta = 3

   slots = ingredient.slots

   if len(slots) == 1:
      # If there's only one slot, just return it
      return slots.keys()[0]
   else:
      # Otherwise find the least and most used slots.
      min_used = max_used = slots.keys()[0]
      for key in slots.keys():
         if slots[key] < slots[min_used]:
            min_used = key
         if slots[key] > slots[max_used]:
            max_used = key

      #if slots[min_used] + max_delta < slots[max_used]:
      #   return min_used
      # TODO - for now we will just always use whatever is the
      # least used one. We can potentially make this more sophisticated in
      # the future, but for now, it's good enough.
      #
      # Also, in this current algorithm, it's useless to calculate max_used,
      # but who cares.
      return min_used

# TODO - this is currently unused, but could be used later
# Choose which slot to pour from based on a list of potential slots and the
# current slots.
##BLOCK_COMMENTdef choose_slot(potential_slots, curr_slots):
##BLOCK_COMMENT   def dist(x, y):
##BLOCK_COMMENT      # circular distance between two indexes in a circle.
##BLOCK_COMMENT      # That doesn't make sense, but you know what I'm talking about.
##BLOCK_COMMENT      return min(abs(x - y), abs(x - (y+6)), abs(x-(y-6)))
##BLOCK_COMMENT
##BLOCK_COMMENT   # Simply take the closest one. This won't work well if everything's all
##BLOCK_COMMENT   # mixed up between spires, but it shouldn't be so whatever...
##BLOCK_COMMENT   closest = potential_slots[0]
##BLOCK_COMMENT   min_dist = 1000
##BLOCK_COMMENT   for slot in potential_slots:
##BLOCK_COMMENT      this_dist = dist(closest.slot, curr_slots[closest.spire].slot)
##BLOCK_COMMENT      if this_dist < min_dist:
##BLOCK_COMMENT         min_dist = this_dist
##BLOCK_COMMENT         closest = slot
##BLOCK_COMMENT
##BLOCK_COMMENT   return closest



# Get a sequence of movements as two queues, one for each spire. They will be sorted
# so that longer drinks pour first. They will be queued so that the distance moved
# between each is minimized
def get_movement_schedule(drink, current_position): # current_pos is unused, but may as well keep it
   class SlotAmount(object):
      def __init__(self, slot, amount):
         self.slot   = slot
         self.amount = amount
      def __str__(self):
         return str(self.slot) + "x" + str(self.amount)

   # For each ingredient in the drink, get the available slots we could pour
   # from. Available slots are those containing the drink which are not overused.
   # If any drink has more than X less in it than another, it is excluded, to avoid
   # overusing any particular drink.
   
   spire = {1:[], 2:[]}

   print "drink:",drink
   print "drink.ingredients:",drink.ingredients
   for entry in drink.ingredients:
      print "   entry:", entry
      slot = get_usable_slot(entry.ingredient)
      spire[slot.spire].append(SlotAmount(slot, entry.amount))

   spire[1] = sorted(spire[1], key=attrgetter("amount"))
   spire[2] = sorted(spire[2], key=attrgetter("amount"))

   return spire

   
