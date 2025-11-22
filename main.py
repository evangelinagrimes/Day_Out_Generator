import tkinter as tk
from tkinter import ttk
from generate_activities import generate_activities

# ==================| MAIN WINDOW |==================
window = tk.Tk()
window.title("Day Out Generator")
window.geometry('1200x700')

# INPUT FIELDS / VARIABLES
HEADER_FONT = 'Calibri 15'
HEADER_SIDE = 'left'
OUTPUT_FONT = 'Calibri 12'
zipcode_int = tk.IntVar()

# ==================| INPUT FRAME |==================
input_frame = ttk.Frame(master= window)

# ------ zipcode frame ------
zipcode_ROW = ttk.Frame(master= input_frame)
zipcode_label = ttk.Label(master= zipcode_ROW,
                            text= "ZIPCODE: ", 
                            font= HEADER_FONT)
zipcode_field = ttk.Entry(master= zipcode_ROW, textvariable= zipcode_int)
zipcode_field.pack()
zipcode_ROW.pack(side= 'left', padx= 5)

# ------ activity preference frame ------
# ------ day of week ------
# ------ theme ------
# ------ generate button ------

input_frame.pack(side='left')
# ==================| OUTPUT FRAME |==================
# output_frame = ttk.Frame(master= window)

# ------------------| CONTENT FRAME |------------------


# === RUN ===
window.mainloop()