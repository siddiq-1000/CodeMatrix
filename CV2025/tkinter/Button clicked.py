# Import the library tkinter
from tkinter import *

# Create a GUI app
app = Tk()

# Create a function with one parameter to indicate which button was clicked
def which_button(button_text):
    # Printing the text when a button is clicked
    print(f"Button clicked: {button_text}")

# Creating and displaying of button b1
b1 = Button(app, text="Apple", command=lambda: which_button("Apple"))
b1.grid(padx=10, pady=10)

# Creating and displaying of button b2
b2 = Button(app, text="Banana", command=lambda: which_button("Banana"))
b2.grid(padx=10, pady=10)

# Make the infinite loop for displaying the app
app.mainloop()