#!/usr/bin/env python
import os
import sys
import pygtk
pygtk.require('2.0')
import gtk

class SimpleAnnotator:
    # list of files in the given directory
    files = []
    
    # currently displayed image
    imageFile = None

    # when invoked (via signal delete_event), terminates the application.
    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False

    # is invoked when the button is clicked
    def button_clicked(self, widget, image, entry):
        # save ground truth to text file
        with open(os.path.splitext(self.imageFile)[0] + ".gt.txt", 'w') as f:
            f.write(entry.get_text())
        print self.imageFile + ": " + entry.get_text()
        
        # load the next image, if one without annotation exists
        entry.set_text("")
        entry.grab_focus()
        self.imageFile = self.get_next_file()        
        if self.imageFile == None:
            print "All images have been annotated."
            gtk.main_quit()
        image.set_from_file(self.imageFile)
    
    # get the next file that has no annotation yet
    def get_next_file(self):
        next_file = None
        while len(self.files) != 0:
            f = self.files.pop()
            if not os.path.isfile(os.path.splitext(f)[0] + ".gt.txt"):
                next_file = f
                break
        return next_file        
    
    def __init__(self):
        # read and sort list of files in given directory
        for f in os.listdir(sys.argv[1]):
            if f.endswith('.png'):
                self.files.append(os.path.join(sys.argv[1], f))
        self.files = sorted(self.files, reverse=True)
        
        # get first image file (or exit if no images found)
        self.imageFile = self.get_next_file()
        if self.imageFile == None:
            sys.exit("No png files without annotation found!")
        
        # create the main window, and attach delete_event signal for terminating
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("delete_event", self.close_application)
        window.set_border_width(10)
        window.show()

        # a vertical box to hold the stuff
        vbox = gtk.VBox()
        vbox.set_spacing(3)
        vbox.show()
        window.add(vbox)
        
        # image
        image = gtk.Image()
        image.set_from_file(self.imageFile)
        image.show()
        vbox.pack_start(image)
        
        # text field
        entry = gtk.Entry(max=0)
        entry.show()
        vbox.pack_start(entry,expand=False)
        entry.grab_focus()
        entry.set_activates_default(True)
        
        # button
        button = gtk.Button("Submit")
        button.show()
        vbox.pack_start(button, expand=False)
        button.set_can_default(True)
        button.grab_default()
        button.connect("clicked", self.button_clicked, image, entry)

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    SimpleAnnotator()
    main()
