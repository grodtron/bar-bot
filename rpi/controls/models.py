
class Ingredient(object):
   def __init__(self, name):
      self.name = name
      self.slots = set()

   def add_slot(self, slot):
      self.slots.add(slot)

   def __str__(self):
      return self.name
   
class Alcohol(Ingredient):
   def __str__(self):
      return self.name

class Mixer(Ingredient):
   def __str__(self):
      return self.name

class DuplicateIngredientError(Exception):
   pass

class UnknownIngredientError(Exception):
   pass

class DrinkRegistry(object):

   def __init__(self):
      self.registry = {
         Alcohol: dict(),
         Mixer  : dict()
      }

      self.ingredients_by_name = dict()

   def add(self, a):
      if type(a) is Drink:
         for i in a.ingredients:
            self.registry[type(i[0])][i[0]].add(a)
      else:

         if self.ingredients_by_name.has_key(str(a)):
            raise DuplicateIngredientError("Already have an entry for %s" % a.name)
         else:
            self.ingredients_by_name[str(a)] = a

         registry = self.registry[type(a)]

         registry[a] = set()

   def get_ingredient(self, name):
      return self.ingredients_by_name[name]

   def get_all(self, a):
      if self.registry.has_key(a):
         return self.registry[a].keys()
      else:
         return self.registry[type(a)][a]

class Drink(object):
   
   def __init__(self, name, desc):
      self.name        = name
      self.description = desc
      self.ingredients = set()

   def add(self, ingredient, amount):
      self.ingredients.add( (ingredient, amount) )

   def __str__(self):
      return self.name
