#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import time

from configurator import Configurator
from buttons import NONE, LEFT, RIGHT, UP, DOWN, PRESSED, UNPRESSED, read_button, read_joystick


WAITING = 1
SLIDING = 2


class HelloWorld:

   def __init__(self):
      self.init_menu()
      self.init_gui()
      self.state = WAITING

   def init_menu(self):
      self.conf = Configurator()
      self.menu = self.conf.build_main_menu()
      self.curr_choice = 1

   def init_gui(self):
      # create a new window
      self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

      screen = self.window.get_screen()
      self.width = 512 #screen.get_width()
      self.height= 256 #screen.get_height()
      self.window.resize(self.width, self.height)
    
      # This packs the button into the window (a GTK container).
      self.lay = gtk.Layout()
      self.lay.set_size(self.width*2, self.height)
      self.window.add(self.lay)

      self.vbox = gtk.VBox()

      self.vbox.set_size_request(self.width, self.height)

      for choice in self.menu.choices:
         self.b = b = gtk.Button("<span size='44000'>%s</span>" % choice)
         b.child.set_use_markup(True)
         self.vbox.add(b)
         b.show()

      self.lay.put(self.vbox, 0, 0)

      self.vbox.show()
      self.lay.show()
    
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
         button_state   = read_button()
         joystick_state = read_joystick()
         self.handle_input(button_state, joystick_state)
      if self.state == SLIDING:
         # TODO - slide tick in direction
         pass
      return True
   
   def handle_input(self, button, joystick):
      if   joystick == UP:
         self.curr_choice = max(0, self.curr_choice - 1)
         self.update_choice()
      elif joystick == DOWN:
         self.curr_choice = min(len(self.menu.choices) - 1, self.curr_choice + 1)
         self.update_choice()
      elif joystick == RIGHT:
         pass
      elif joystick == LEFT:
         pass
   
   def update_choice(self):
      print "self.curr_choice is now", self.curr_choice
      for i, child in enumerate(self.vbox.get_children()):
         # TODO - there must be a better way of setting this no?
         if i == self.curr_choice:
            child.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
         else:
            child.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("grey"))
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
