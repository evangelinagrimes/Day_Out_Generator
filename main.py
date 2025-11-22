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
activity_toggle_states = {}

# HELPER FUNCTIONS
def create_toggle_button(parent, text, key):
    '''
    Creates a toggle button and implements the toggle feature
    
    :param parent: The parent frame the button should be attached to (tk.Frame)
    :param text: The text that appears on the button (string)
    :param key: The button identifier (string)

    :return: A button object
    '''
    activity_toggle_states[key] = True
    
    def toggle():
        activity_toggle_states[key] = not activity_toggle_states[key]
        if activity_toggle_states[key]:
            btn.config(relief=tk.SUNKEN, bg="darkgrey")
        else:
            btn.config(relief=tk.RAISED, bg="SystemButtonFace")
    
    btn = tk.Button(parent, text=text, command=toggle, 
                    width=10, height=1, relief=tk.SUNKEN, bg="darkgrey")
    return btn

# ==================| INPUT FRAME |==================
input_FRAME = ttk.Frame(master= window, width=400, height=700, relief="ridge")

# > ------ zipcode frame ------
zipcode_ROW = ttk.Frame(master= input_FRAME)
zipcode_label = ttk.Label(master= zipcode_ROW,
                            text= "ZIPCODE: ", 
                            font= HEADER_FONT)
zipcode_field = ttk.Entry(master= zipcode_ROW, textvariable= zipcode_int)
zipcode_label.pack(side= 'left')
zipcode_field.pack(side= 'left')
zipcode_ROW.pack()

# > ------ activity preference frame ------
# NOTE: 
activityPref_ROW = ttk.Frame(master= input_FRAME)
activities = ["Restaurant", "Activity", "Dessert"]

for i, activity in enumerate(activities):
    btn = create_toggle_button(activityPref_ROW, activity, activity)
    btn.grid(row=0, column=i, padx=5, pady=5)

activityPref_ROW.pack()

# > ------ day of week ------
dayOfWeek_ROW = ttk.Frame(master= input_FRAME)

dayOfWeek_ROW.pack()

# > ------ theme ------
theme_ROW = ttk.Frame(master= input_FRAME)

theme_ROW.pack()

# > ------ generate button ------
#@TODO: Button can just be linked to input_FRAME

input_FRAME.pack(side='left')

# ==================| OUTPUT FRAME |==================
output_FRAME = ttk.Frame(master= window, width=800, height=700, relief="ridge")

# ------------------| CONTENT FRAME |-----------------
content_FRAME = ttk.Frame(master= output_FRAME)

# - - - - - - - -  | SELECTION FRAME | - - - - - - - -
selection_FRAME = ttk.Frame(master= content_FRAME, width=300, height=500)

# > ------ first stop ------
firstStop_FRAME = ttk.Frame(master= selection_FRAME)

firstStop_FRAME.pack(side= 'left')
# > ------ second stop ------
secondStop_FRAME = ttk.Frame(master= selection_FRAME)

secondStop_FRAME.pack(side= 'left')
# > ------ final stop ------
finalStop_FRAME = ttk.Frame(master= selection_FRAME)

finalStop_FRAME.pack(side= 'left')
selection_FRAME.pack(side= 'left')

# - - - - - - - - - - | INFO FRAME | - - - - - - - - - 
info_FRAME = ttk.Frame(master= content_FRAME, width=500, height=500 )
#@TODO: Create a title label for this frame, doesn't need to be its own frame

# > ------ activity type display ------
activityType_ROW = ttk.Frame(master= info_FRAME)

activityType_ROW.pack()
# > ------ company name display ------
companyName_ROW = ttk.Frame(master= info_FRAME)

companyName_ROW.pack()
# > ------ website link display ------
websiteLink_ROW = ttk.Frame(master= info_FRAME)

websiteLink_ROW.pack()
# > ------ price level display ------
priceLevel_ROW = ttk.Frame(master= info_FRAME)

priceLevel_ROW.pack()
# > ------ top review display ------
topReview_ROW = ttk.Frame(master= info_FRAME)

topReview_ROW.pack()


info_FRAME.pack(side= 'right')
# - - - - - - - - - - - - - - - - - - - -

# @TODO: Add "Make my selection" Button HERE (Content_FRAME)
content_FRAME.pack(side='top')
# ---------------------------------------
output_FRAME.pack(side='right')
# =======================================

# === RUN ===
window.mainloop()