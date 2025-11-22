import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
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
dayOfWeek_toggle_states = {}
isSetToDay = True
isThemeActive = True

# HELPER FUNCTIONS
def create_toggle_button(parent, text, width, height, key, start_state, state_dictionary, ):
    '''
    Creates a toggle button and implements the toggle feature
    
    :param parent: The parent frame the button should be attached to (tk.Frame)
    :param text: The text that appears on the button (string)
    :param width: The desired width of the button (int)
    :param height: The desired height of the button (int)
    :param key: The button identifier (string)
    :param start_state: The state of the button upon create (On/Off) (Boolean)
    :param state_dictionary: A dictionary that stores the state of each button in the frame (dict)

    :return: A button object
    '''
    state_dictionary[key] = start_state
    
    def toggle():
        state_dictionary[key] = not state_dictionary[key]
        if state_dictionary[key]:
            btn.config(relief=tk.SUNKEN, bg="darkgrey")
            print(f"{str(key)} state toggled ON" )
        else:
            btn.config(relief=tk.RAISED, bg="SystemButtonFace")
            print(f"{str(key)} state toggled OFF" )
    
    if start_state: 
        btn = tk.Button(parent, text=text, command=toggle, 
                    width=width, height=height, relief=tk.SUNKEN, bg="darkgrey")
    else: 
        btn = tk.Button(parent, text=text, command=toggle, 
                    width=width, height=height, relief=tk.RAISED, bg="SystemButtonFace")
    
    return btn

def switchDayButton(): 
    global isSetToDay
    if isSetToDay: 
        day_button.config(image=night)
        print("Switched to NIGHT")
    else:
        day_button.config(image=day)
        print("Switched to DAY")
        
    isSetToDay = not isSetToDay

def switchThemeButton():
    global isThemeActive
    if isThemeActive: 
        theme_button.config(image=theme)
        print("Switch to RANDOM THEME")
    else:
        theme_button.config(image=noTheme)
        print("Switched to NO THEME")
        
    isThemeActive = not isThemeActive


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
# NOTE: button values are stored in activity_toggle_states

activityPref_ROW = ttk.Frame(master= input_FRAME)
activities = ["Restaurant", "Activity", "Dessert"]

for i, activity in enumerate(activities):
    btn = create_toggle_button(activityPref_ROW, activity, 10, 1, activity, True, activity_toggle_states)
    btn.grid(row=0, column=i, padx=5, pady=5)

activityPref_ROW.pack()

# > ------ day of week ------
# NOTE: button values are stored in dayOfWeek_toggle_states
dayOfWeek_ROW = ttk.Frame(master= input_FRAME)
dayOfWeek = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

for i, day in enumerate(dayOfWeek):
    btn = create_toggle_button(dayOfWeek_ROW, day, 5, 1, day, False, dayOfWeek_toggle_states)
    btn.grid(row=0, column=i, padx=5, pady=5)

dayOfWeek_ROW.pack()

# > ------ day/night AND theme  ------
dayNight_ROW = ttk.Frame(master= input_FRAME)   

day = PhotoImage(file="assets/switchDAY.png")
night = PhotoImage(file="assets/switchNIGHT.png")
day_button = tk.Button(dayNight_ROW, image=day, bd=0, command=switchDayButton)

theme = PhotoImage(file="assets/THEME.png")
noTheme = PhotoImage(file="assets/NO_THEME.png")
theme_button = tk.Button(dayNight_ROW, image=theme, bd=0, command=switchThemeButton)

day_button.pack(side='left')
theme_button.pack(side='left')
dayNight_ROW.pack()

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