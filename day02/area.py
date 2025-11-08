# Import math module for pi
import math
from tkinter import *

# Create the root window
root = Tk()
root.title("Circle Area Calculator")

# Create a function to calculate the area
def calculate_area():
    try:
        radius = float(radius_entry.get())
    except ValueError:
        msg = "not valid number for radius. please enter a valid number and try again"
        print(msg)
        result_label.config(text=msg)
        return
    # Calculate the area
    area = math.pi * radius ** 2
    # Update the result label with the area, rounded to 2 decimal places
    result_label.config(text=f"Area: {area:.2f}")

# Create a label and entry for the radius
radius_label = Label(root, text="Enter the radius of the circle:")
radius_label.pack()
radius_entry = Entry(root)
radius_entry.pack()

# Create a button to calculate the area
calculate_button = Button(root, text="Calculate Area", command=calculate_area)
calculate_button.pack()

# Create a label to display the result
result_label = Label(root, text="Area:")
result_label.pack()

if __name__ == "__main__":
    root.mainloop()