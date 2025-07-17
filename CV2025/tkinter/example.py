from tkinter import *

# create root window
root = Tk()

# frame inside root window
frame = Frame(root,bg='red', bd=3, cursor='hand2', height=100, 
                      highlightcolor='red', highlightthickness=2, highlightbackground='black', width=200)

# geometry method
frame.pack()

# button inside frame which is
# inside root
button = Button(frame, text='NIDHI')
button.pack()

# Tkinter event loop
root.mainloop()