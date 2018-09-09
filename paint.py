# paint.py by Dom Reichl
# a simple drawing program that produces test images for neural_network.py

from tkinter import *
from tkinter import messagebox
from PIL import ImageGrab
import os

class Paint:
    def __init__(self):
        '''
        Initializes tkinter frame with variables for coordinates and image number,
        a canvas for drawing, a binding of mouse events, a label that displays the
        current image's number, and two buttons (save and reset).
        '''
        self.root = Tk()
        
        self.x = None # x axis
        self.y = None # y axis

        self.number = 0 # this variable is for both the image number and the digit to be drawn
        Label(self.root, text='Please draw "' + str(self.number) + '"', font="Verdana 15 bold").grid(row=0, columnspan=3)

        self.canvas = Canvas(self.root, bg='white', width=280, height=280) # 280x280 drawing area
        self.canvas.grid(row=1, columnspan=3)

        self.canvas.bind('<B1-Motion>', self.paint) # tracks mouse motion while mouse button 1 being held down
        self.canvas.bind('<ButtonRelease-1>', self.no_paint) # tracks mouse button 1 being released

        Label(self.root, text=" #" + str(self.number)).grid(row=2, column=0, sticky=W)
        Button(self.root, text="Save", command=(lambda: self.save(self.number))).grid(row=2, column=1)
        Button(self.root, text="Reset", command=self.reset).grid(row=2, column=2, sticky=E)
        
        self.root.mainloop()

    def paint(self, event):
        '''
        Called by mouse button 1 being held down on canvas.
        Draws black line according to mouse motion.
        '''
        
        if self.x and self.y:
            self.canvas.create_line(self.x, self.y, event.x, event.y, width=30, fill='black', capstyle=ROUND)
        self.x = event.x
        self.y = event.y

    def no_paint(self, event):
        '''
        Called by mouse button 1 being released.
        Resets coordinate variables; nothing is drawn.
        '''
        
        self.x, self.y = None, None

    def save(self, number):
        '''
        Called by click on button 'Save'.
        Creates image object from canvas, processes it, and saves it as PNG file.
        Resets canvas for drawing the next digit, unless the current digit was already 9 (i.e., the last one).
        '''
        
        # get image coordinates
        x1 = self.root.winfo_rootx() + self.canvas.winfo_x()
        y1 = self.root.winfo_rooty() + self.canvas.winfo_y()
        x2 = x1 + self.canvas.winfo_width()
        y2 = y1 + self.canvas.winfo_height()

        # convert to grayscale, resize, and save image in 'test' directory
        test_path = os.path.join(os.getcwd(), 'test') # path for dictionary 'test'
        if not os.path.isdir(test_path): os.makedirs(test_path) # create dictionary if it doesn't exist
        image_path = os.path.join(test_path, '{num}.png'.format(num=str(self.number))) # path for image file
        ImageGrab.grab().crop((x1, y1, x2-4, y2-4)).convert('L').resize((28, 28)).save(image_path) # process and save image

        # move on to next number or quit
        if self.number < 9:
            self.number += 1
            Label(self.root, text=" #" + str(self.number)).grid(row=2, column=0, sticky=W)
            Label(self.root, text='Please draw "' + str(self.number) + '"', font="Verdana 15 bold").grid(row=0, columnspan=3)
            self.reset()
        else:
            messagebox.showinfo("", "Done.")
            self.root.destroy()
            
    def reset(self):
        '''
        Called by function 'save' when an image has been saved and a new one needs to be drawn.
        Empties the canvas.
        '''
        
        self.canvas.delete('all')

Paint()
