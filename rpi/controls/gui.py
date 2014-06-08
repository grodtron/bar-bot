#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import time

from configurator import Configurator
from buttons import NONE, LEFT, RIGHT, UP, DOWN, PRESSED, UNPRESSED, Joystick, Button


WAITING = 1
SLIDING = 2


class HelloWorld:

   def __init__(self):
      print "init'ing menu"
      self.init_menu()
      print "init'ing inputs"
      self.init_inputs()
      print "init'ing gui"
      self.init_gui()
      self.state = WAITING

   def init_inputs(self):
      self.prev_joystick_state = NONE
      self.prev_button_state = UNPRESSED
      self.joystick = Joystick()
      self.button   = Button()

   def init_menu(self):
      self.conf = Configurator()
      self.menu = self.conf.build_main_menu()
      self.curr_choice = 0

   def init_gui(self):
      # create a new window
      self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

      screen = self.window.get_screen()
      self.width = screen.get_width()
      self.height= screen.get_height()
      self.window.resize(self.width, self.height)
    
      # This packs the button into the window (a GTK container).
      self.lay = gtk.Layout()
      self.lay.set_size(self.width*2, self.height)
      self.window.add(self.lay)

      self.vbox = gtk.VBox()
      self.vbox.set_size_request(self.width, self.height)

      self.lay.put(self.vbox, 0, 0)

      self.update_menu()
      self.update_choice()

      self.lay.show()

      self.update_choice()
    
      self.window.show()

      self.pos = 0
      gobject.timeout_add(30, self.state_machine_tick)

   ##def animate_callback(self):
      ##self.pos = (self.pos + 4)
      ##self.lay.move(self.vbox, self.pos, 0)
      ##self.window.queue_draw()
      ##return self.pos < (self.width/2)

   def state_machine_tick(self):
      if self.state == WAITING:
         button_state   = self.button.read()
         joystick_state = self.joystick.read()
         self.handle_input(button_state, joystick_state)
      if self.state == SLIDING:
         # TODO - slide tick in direction
         pass
      return True
   
   def handle_input(self, button, joystick):
      if button == PRESSED:
         if self.prev_button_state == UNPRESSED:

            # TODO - do we pour directly from the menu or have some
            # kind of details page?

            if self.menu.is_leaf():
               print "POURING DRINK!!! %s" % self.menu.key
            else:
               # Same as right joystick
               self.menu = self.menu.choice(self.curr_choice)
               self.curr_choice = 0
               self.update_menu()

      # ignore joystick if button pressed
      elif self.prev_joystick_state == NONE:
         if   joystick == UP   and not self.menu.is_leaf():
            self.curr_choice = max(0, self.curr_choice - 1)
         elif joystick == DOWN and not self.menu.is_leaf():
            self.curr_choice = min(len(self.menu.choices) - 1, self.curr_choice + 1)
         elif joystick == RIGHT:
            if not self.menu.is_leaf():
               self.menu = self.menu.choice(self.curr_choice)
               self.curr_choice = 0
               self.update_menu()
         elif joystick == LEFT:
            self.menu = self.menu.back()
            self.curr_choice = 0
            self.update_menu()

         if joystick != NONE:
            self.update_choice()

      self.prev_joystick_state = joystick
      self.prev_button_state   = button

   
   def update_menu(self):
      self.vbox.hide()

      for child in self.vbox.get_children():
         self.vbox.remove(child)

      try:
         choices = self.menu.choices
      except AttributeError:
         choices = (self.menu.key,)

      for choice in choices:
         b = gtk.Button("<span size='44000'>%s</span>"
            % gobject.markup_escape_text(str(choice)))
         b.child.set_use_markup(True)
         self.vbox.add(b)
         b.show()

   
      self.vbox.show()


   def update_choice(self):
      print "self.curr_choice is now", self.curr_choice
      for i, child in enumerate(self.vbox.get_children()):
         # TODO - there must be a better way of setting this no?
         for state in (gtk.STATE_NORMAL, gtk.STATE_PRELIGHT):
            if i == self.curr_choice:
               child.modify_fg(state, gtk.gdk.color_parse("#000000"))
               child.modify_bg(state, gtk.gdk.color_parse("#FCFF3D"))
            else:
               child.modify_fg(state, gtk.gdk.color_parse("#555555"))
               child.modify_bg(state, gtk.gdk.color_parse("#CCCCCC"))
      self.vbox.queue_draw()



   def main(self):
      # All PyGTK applications must have a gtk.main(). Control ends here
      # and waits for an event to occur (like a key press or mouse event).
      gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
   hello = HelloWorld()
   hello.main()
