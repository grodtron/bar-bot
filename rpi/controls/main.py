from models    import Alcohol, Mixer, Drink, DrinkRegistry, Slot
from menu      import MenuItem, Menu
from scheduler import get_movement_schedule
import config
import random
import cPickle as pickle
import os

def init():
   # Create Registry
   reg = DrinkRegistry()

   for a in config.alcohols:
      reg.add(Alcohol(a))

   for m in config.mixers:
      reg.add(Mixer(m))

   for d in config.drinks:
      drink = Drink(d["name"], d["description"])
      for i in d["ingredients"]:
         ingredient = reg.get_ingredient(i["name"])
         drink.add(ingredient, i["amount"])

      reg.add(drink)

   return reg

   # Map ingredients to spire positions

def build_main_menu(reg):
   # Build menu
   return Menu(None, [
      MenuItem(Alcohol, reg.get_all, name="By Alcohol"),
      MenuItem(Mixer  , reg.get_all, name="By Mixer")
   ])

def build_slot_mapping_menu(reg):
   return Menu(None,
         map(lambda i: MenuItem(i, None), reg.get_all_ingredients()))

def main():

   pickled_reg_fname = "drink-registry.p"

   if not os.path.isfile(pickled_reg_fname):
      reg = init()

      menu = build_slot_mapping_menu(reg)

      # Map the Drinks to their positions in the spires!
      # TODO - use pickling to save and restore configs!!
      #        (but still show menu to optionally correct)
      for spire in (1,2):
         for slot in range(1,6 + 1):
            for i, name in enumerate(menu.choices):
               print i, name

            choice = raw_input("What ingredient is in spire %d slot %d?: " % (spire, slot))

            menu.choice(int(choice)).key.add_slot(Slot(spire, slot))

      with open(pickled_reg_fname, "w") as pickle_file:
         pickle.dump(reg, pickle_file, pickle.HIGHEST_PROTOCOL)
   else:
      with open(pickled_reg_fname, "r") as pickle_file:
         reg = pickle.load(pickle_file)

   for i in reg.get_all_ingredients():
      print "Ingredient %s is in slots: (%s)" % (str(i), ", ".join(map(str, i.slots)))

   menu = build_main_menu(reg)

   current = {1:Slot(1,1), 2:Slot(2,1)}
   
   while True:
      if menu.is_leaf():
         print menu.key.description

         choice = raw_input("[s]elect or [b]ack? :")

         if choice == "b":
            menu = menu.back()
         if choice == "s":
            drink = menu.key
            print "Selected Drink:", drink
            print "               ", drink.description
            print "Pouring ingredients from:"

            seq = get_movement_schedule(drink, current)

            while len(seq[1]) and len(seq[2]):
               new1 = seq[1].pop()
               new2 = seq[2].pop()
               print "Moving from", str(current[1])+"-"+str(current[2]), "to", str(new1)+"-"+str(new2)
               current[1] = new1
               current[2] = new2

            while len(seq[1]):
               new = seq[1].pop()
               print "Moving from", str(current[1])+"-"+str(current[2]), "to", new
               current[1] = new

            while len(seq[2]):
               new = seq[2].pop()
               print "Moving from", str(current[1])+"-"+str(current[2]), "to", new
               current[2] = new

            menu = menu.back().back().back()
         else:
            print "invalid choice %s" % choice
      else:
         for i, name in enumerate(menu.choices):
            print "   %d.  %s" % (i, name)

         choice = raw_input("What do you want? [b]ack, <int choice>: ")

         if choice == "b" or choice == "back":
            menu = menu.back()
         else:
            menu = menu.choice(int(choice))

if __name__ == '__main__':
   main()
