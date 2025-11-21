import tkinter as tk
from tkinter import ttk
from generate_activities import generate_activities

# Tutorial referenced https://www.youtube.com/watch?v=mop6g-c5HEY 
"""
Notes: 
# Keep in mind what widgets are dependent on what
# Use .pack() to officially add the widget to the base
"""

def trigger_generate_activities():
    zip = zipcode_int.get()

    # generate_activities()

    output_dinner_string.set('Restaurant')
    output_activity_string.set('Activity')
    output_desert_string.set('Desert')

# === WINDOW ===
window = tk.Tk()
window.title("Date Night Generator")
window.geometry('500x300')

# === TITLE ===
title_label = ttk.Label(master= window, text = "Date Night Generator", font = 'Calibri 24')
title_label.pack()

# === INPUT FIELDS ===
input_frame = ttk.Frame(master= window)
zipcode_int = tk.IntVar()
zipcode = ttk.Entry(master= input_frame, textvariable= zipcode_int)
button = ttk.Button(master= input_frame, text= 'Generate', command = trigger_generate_activities)
zipcode.pack(side= 'left', padx = 10)
button.pack(side= 'left')
input_frame.pack(pady = 10)

# === OUTPUT ===

# Header settings
HEADER_FONT = 'Calibri 15'
HEADER_SIDE = 'left'

# Output settings
OUTPUT_FONT = 'Calibri 12'

# Variables and Labels
output_frame= ttk.Frame(master= window)

# Dinner Column
dinner_column = ttk.Frame(master= output_frame)
header_dinner_label = ttk.Label(master= dinner_column,
                            text= "Activity 1", 
                            font= HEADER_FONT)
header_dinner_label.pack(pady=(5, 0))

output_dinner_string= tk.StringVar()
output_dinner_label= ttk.Label(master= dinner_column, 
                         text= 'Dinner', 
                         font= OUTPUT_FONT, 
                         textvariable= output_dinner_string)
output_dinner_label.pack(pady=(0, 15))
dinner_column.pack(side=tk.LEFT, padx=5)

# Activity Column
activity_column = ttk.Frame(master= output_frame)
header_activity_label = ttk.Label(master= activity_column,
                            text= "Activity 2", 
                            font= HEADER_FONT)
header_activity_label.pack(pady=(5, 0))

output_activity_string = tk.StringVar()
output_activity_label = ttk.Label(master= activity_column, 
                         text= 'Activity', 
                         font= OUTPUT_FONT, 
                         textvariable= output_activity_string)
output_activity_label.pack(pady=(0, 15))
activity_column.pack(side=tk.LEFT, padx=5)

# Desert Column
desert_column= ttk.Frame(master= output_frame)
header_desert_label= ttk.Label(master= activity_column,
                            text= "Activity 3", 
                            font= HEADER_FONT)
header_desert_label.pack(pady=(5, 0))

output_desert_string= tk.StringVar()
output_desert_label= ttk.Label(master= activity_column, 
                         text= 'output', 
                         font= OUTPUT_FONT, 
                         textvariable= output_desert_string)
output_desert_label.pack(pady=(0, 15))
desert_column.pack(side=tk.LEFT, padx=5)
output_frame.pack()

# === RUN ===
window.mainloop()

