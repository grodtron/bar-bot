#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import time

class HelloWorld:

    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def hello(self, widget, data=None):
        print "Hello World"

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    
        # When the window is given the "delete_event" signal (this is given
        # by the window manager, usually by the "close" option, or on the
        # titlebar), we ask it to call the delete_event () function
        # as defined above. The data passed to the callback
        # function is NULL and is ignored in the callback function.
        self.window.connect("delete_event", self.delete_event)
    
        # Here we connect the "destroy" event to a signal handler.  
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        self.window.connect("destroy", self.destroy)
    
        # Sets the border width of the window.
        #self.window.set_border_width(10)
    
        # Creates a new button with the label "Hello World".
        self.button = gtk.Button("Hello World")
    
        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        self.button.connect("clicked", self.hello, None)

	screen = self.window.get_screen()
	self.width = screen.get_width()
	self.height= screen.get_height()
        self.window.resize(self.width, self.height)
    
        # This will cause the window to be destroyed by calling
        # gtk_widget_destroy(window) when "clicked".  Again, the destroy
        # signal could come from here, or the window manager.
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
    
        # This packs the button into the window (a GTK container).

	self.lay = gtk.Layout()
	self.lay.set_size(self.width*2, self.height)
        self.window.add(self.lay)

	self.vbox = gtk.VBox()

	self.vbox.set_size_request(self.width, self.height)
	

	for i in range(4):
		self.b = b = gtk.Button("<span size='48000'>This is a test</span>" + str(i))
		b.child.set_use_markup(True)
		##self.lay.add(b)
		self.vbox.add(b)
		b.show()
    

	self.lay.put(self.vbox, -10, 0)

	self.vbox.show()
	self.lay.show()

        # The final step is to display this newly created widget.
        #self.button.show()
    
        # and the window
        self.window.show()

	self.pos = 0
	gobject.timeout_add(30, self.animate_callback)

    def animate_callback(self):
	self.pos = (self.pos + 4)
	self.lay.move(self.vbox, self.pos, 0)
	self.window.queue_draw()
	print "test"
	return self.pos < (self.width/2)

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
