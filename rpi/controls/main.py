from models import Alcohol, Mixer, Drink, DrinkRegistry
from menu   import MenuItem, Menu
import config

def initialize():
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

def main():
   dr = initialize()

   menu = Menu(None, [
      MenuItem(Alcohol, dr.get_all, name="By Alcohol"),
      MenuItem(Mixer  , dr.get_all, name="By Mixer")
   ])
   
   while True:

      if menu.is_leaf():
         print menu.key.description

         choice = raw_input("[s]elect or [b]ack? :")

         if choice == "b":
            menu = menu.back()
         if choice == "s":
            menu.select()
            menu = menu.back()
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
