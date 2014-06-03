from models import Alcohol, Mixer, Drink, DrinkRegistry, Slot
from menu   import MenuItem, Menu
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
            for i in drink.ingredients:
               print "   ", i[0], random.choice(list(i[0].slots))
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
