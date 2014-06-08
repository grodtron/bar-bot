
class MenuLeaf(object):
   def __init__(self, parent, key):
      self.key    = key
      self.parent = parent

   def back(self):
      return self.parent

   def select(self):
      print "You have selected %s" % str(self.key)

   def is_leaf(self):
      return True

class MenuItem(object):
   def __init__(self, key, children_func, **kwargs):
      self.parent = None
      self.key = key
      self.name = kwargs["name"] if "name" in kwargs else str(key)
      self.children_func = children_func

   def __str__(self):
      return self.name
   
   def menu(self):
      try:
         return Menu(self.parent,
               map(
                  lambda x: MenuItem(x, self.children_func),
                  self.children_func(self.key)))
      except Exception as e:
         return MenuLeaf(self.parent, self.key)


class Menu(object):
   def __init__(self, parent, choices):
      self.parent  = self if parent is None else parent
      self.choices = choices
      for choice in choices:
         choice.parent = self

   def back(self):
      return self.parent

   def choice(self, n):
      try:
         return self.choices[n].menu()
      except IndexError:
         print "WARNING: returning self for a childless Menu"
         return self

   def is_leaf(self):
      return False
