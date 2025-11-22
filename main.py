import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from generate_activities import generate_activities

# ==================| MAIN WINDOW |==================
window = tk.Tk()
s = ttk.Style()
window.title("Day Out Generator")
window.geometry('1200x700')

# INPUT FIELDS / VARIABLES
HEADER_FONT = 'Calibri 15'
SUBHEADING_FONT = 'Calibri 13'
OUTPUT_FONT = 'Calibri 12'
STOP_Y_POS = 10
INFO_SUB_LABEL_POS = (5, 0)

selectedStop_str = tk.StringVar(value="")
selectedType_str = tk.StringVar()
selectedBusiness_str = tk.StringVar()
selectedAddress_str = tk.StringVar()
selectedWebsite_str = tk.StringVar()
selectedPrice_str = tk.StringVar()
selectedTopReview_str = tk.StringVar()
zipcode_int = tk.IntVar()

selectedFirstStop_list = []
activity_toggle_states = {}
dayOfWeek_toggle_states = {}
isSetToDay = True
isThemeActive = True
generateButtonPressed = False
traceID = ""

# HELPER FUNCTIONS
def generate_helper():
    print("Calling Google API...")
    
    # Update the output frame to display activities
    updateOutputFrame()

def on_radio_select_stop():
    '''
    Updates the currently selected stop to the current state of the radio button
    '''
    global selectedStop_str
    selected = selectedStop_str.get()
    print(f"Selected: {selected}")

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
            # print(f"{str(key)} state toggled ON" )
        else:
            btn.config(relief=tk.RAISED, bg="SystemButtonFace")
            # print(f"{str(key)} state toggled OFF" )
    
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
        # print("Switched to NIGHT OUT")
    else:
        day_button.config(image=day)
        # print("Switched to DAY OUT")
        
    isSetToDay = not isSetToDay

def switchThemeButton():
    global isThemeActive
    if isThemeActive: 
        theme_button.config(image=theme)
        # print("Switch to RANDOM THEME")
    else:
        theme_button.config(image=noTheme)
        # print("Switched to NO THEME")
        
    isThemeActive = not isThemeActive

def updateOutputFrame(): 
    '''
    Updates the output content frame to display the activities pulled from the 
    data collected with the Google Places API call
    '''
    global isSetToDay
    global traceID
    global activities

    # Clear existing content_FRAME widgets
    for widget in content_FRAME.winfo_children():
        widget.destroy()

    try:
        selectedStop_str.trace_remove('write', traceID)
    except:
        print("             Could not remove existing Trace ID")

    # - - - - - - - -  | SELECTION FRAME | - - - - - - - -
    selection_FRAME = ttk.Frame(master= content_FRAME, width=300, height=550, relief="groove")
    selection_FRAME.pack_propagate(False)

    # > ------ first stop ------
    firstStop_FRAME = ttk.Frame(master= selection_FRAME)
    firstStop_label = ttk.Label(firstStop_FRAME, text= "FIRST STOP ", font = HEADER_FONT)
    subFirstStop_label = ttk.Label(firstStop_FRAME, text="", font = SUBHEADING_FONT)

    firstStopRadioSelection_FRAME = ttk.Frame(master= firstStop_FRAME)
    
    if isSetToDay and activity_toggle_states["Activity"]: 
        # >> - - - dynamic button selection RESTAURANT- - -
        subFirstStop_label.config(text="Activity")

        # @TODO:                vvv   REPLACE WITH GENERATED VALUES    vvv
        selectedFirstStop_list = ["Activity 1", "Activity 2", "Activity 3"]
        #                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        for i, option_text in enumerate(selectedFirstStop_list):
            radButt = tk.Radiobutton(firstStopRadioSelection_FRAME, 
                        text=option_text, 
                        variable=selectedStop_str, 
                        value=option_text, 
                        command=on_radio_select_stop,
                        )
            radButt.pack()
            print(f"First Stop: Generating selection ACTIVITY... {str(selectedStop_str)}")

    elif not isSetToDay and activity_toggle_states["Restaurant"]: 
        # >> - - - dynamic button selection ACTIVITY - - -
        subFirstStop_label.config(text="Restaurant")

        # @TODO:                vvv       REPLACE WITH GENERATED VALUES       vvv
        selectedFirstStop_list = ["Restaurant 1", "Restaurant 2", "Restaurant 3"]
        #                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        for i, option_text in enumerate(selectedFirstStop_list):
            radButt = tk.Radiobutton(firstStopRadioSelection_FRAME, 
                        text=option_text, 
                        variable=selectedStop_str, 
                        value=option_text, 
                        command=on_radio_select_stop,
                        )
            radButt.pack()
            print(f"First Stop: Generating selection RESTAURANT ... {str(selectedStop_str)}")
    else:
        print(f"                SKIPPED because {activities[0]} or {activities[1]} was false")
        firstStop_label.config(text= "")

    firstStop_label.pack(anchor='w')
    subFirstStop_label.pack()
    firstStopRadioSelection_FRAME.pack()

    firstStop_FRAME.pack(side= 'top', pady= STOP_Y_POS)

    # > ------ second stop ------
    secondStop_FRAME = ttk.Frame(master= selection_FRAME)
    secondStop_label = ttk.Label(secondStop_FRAME, text= "SECOND STOP ", font = HEADER_FONT)
    subSecondStop_label = ttk.Label(secondStop_FRAME, text="", font = SUBHEADING_FONT)

    secondStopRadioSelection_FRAME = ttk.Frame(master= secondStop_FRAME)

    if isSetToDay and activity_toggle_states["Restaurant"]: 
        subSecondStop_label.config(text="Restaurant")

        # @TODO:                vvv       REPLACE WITH GENERATED VALUES       vvv
        selectedSecondStop_list = ["Restaurant 1", "Restaurant 2", "Restaurant 3"]
        #                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        for i, option_text in enumerate(selectedSecondStop_list):
            radButt = tk.Radiobutton(secondStopRadioSelection_FRAME, 
                        text=option_text, 
                        variable=selectedStop_str, 
                        value=option_text, 
                        command=on_radio_select_stop,
                        )
            radButt.pack()
            print(f"Second Stop: Generating selection RESTAURANT ... {str(selectedStop_str)}")
    elif not isSetToDay and activity_toggle_states["Activity"]: 
        subSecondStop_label.config(text="Activity")

        # @TODO:                vvv    REPLACE WITH GENERATED VALUES     vvv
        selectedSecondStop_list = ["Activity 1", "Activity 2", "Activity 3"]
        #                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        for i, option_text in enumerate(selectedSecondStop_list):
            radButt = tk.Radiobutton(secondStopRadioSelection_FRAME, 
                        text=option_text, 
                        variable=selectedStop_str, 
                        value=option_text, 
                        command=on_radio_select_stop,
                        )
            radButt.pack()
            print(f"Second Stop: Generating selection ACTIVITY ... {str(selectedStop_str)}")

    else: 
        print(f"                SKIPPED because {activities[0]} or {activities[1]} was false")
        secondStop_label.config(text= "")

    secondStop_label.pack(anchor='w')
    subSecondStop_label.pack()
    secondStopRadioSelection_FRAME.pack()
    
    secondStop_FRAME.pack(side= 'top', pady= STOP_Y_POS)

    # > ------ final stop ------
    finalStop_FRAME = ttk.Frame(master= selection_FRAME)
    finalStop_label = ttk.Label(finalStop_FRAME, text= "FINAL STOP ", font = HEADER_FONT)
    subFinalStop_label = ttk.Label(finalStop_FRAME, text="Dessert", font = SUBHEADING_FONT)

    finalStopRadioSelection_FRAME = ttk.Frame(master= finalStop_FRAME)

    if activity_toggle_states["Dessert"]: 
        # @TODO:                vvv       REPLACE WITH GENERATED VALUES       vvv
        selectedFinalStop_list = ["Dessert 1", "Dessert 2", "Dessert 3"]
        #                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        for i, option_text in enumerate(selectedFinalStop_list):
            radButt = tk.Radiobutton(finalStopRadioSelection_FRAME, 
                        text=option_text, 
                        variable=selectedStop_str, 
                        value=option_text, 
                        command=on_radio_select_stop,
                        )
            radButt.pack()
            print(f"Final Stop: Generating selection DESSERT ... {str(selectedStop_str)}")
    else:
        print(f"                SKIPPED because {activities[2]} was false")
        finalStop_label.config(text= "")
        subFinalStop_label.config(text="")

    finalStop_label.pack(anchor='w')
    subFinalStop_label.pack()
    finalStopRadioSelection_FRAME.pack()

    finalStop_FRAME.pack(side= 'top', pady= STOP_Y_POS)

    selection_FRAME.pack(side= 'left')

    # - - - - - - - - - - | INFO FRAME | - - - - - - - - - 

    INFO_ROW_Y_SPACING = 5
    INFO_ROW_X_SPACING = 25

    info_FRAME = ttk.Frame(master= content_FRAME, width=500, height=550, relief="groove")
    info_FRAME.pack_propagate(False)

    infoTitle_label = ttk.Label(master= info_FRAME, 
                                text= "Select to see more information", 
                                font= HEADER_FONT)
    
    infoTitle_label.pack(pady=25)

    # > ------ activity type display ------
    activityType_ROW = ttk.Frame(master= info_FRAME)

    activityType_label = ttk.Label(master= activityType_ROW, 
                                text= "Test Default", 
                                font= SUBHEADING_FONT)
    
    activityType_label.pack()

    activityType_ROW.pack(anchor='w', padx= INFO_ROW_X_SPACING, pady= INFO_ROW_Y_SPACING)
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

    def update_info_label(*args):
        '''
        Updates the info labels to match the selected
        radio button

        Needs to be beneath the labels to update
        '''
        selection = selectedStop_str.get()
        if selection: 
            infoTitle_label.config(text=selection)
            
            
        else:
            # Reset values
            infoTitle_label.config(text="Select to see more information")
            activityType_label.config(text="")

        
    traceID = selectedStop_str.trace('w', update_info_label)
    info_FRAME.pack(side= 'right')
# - - - - - - - - - - - - - - - - - - - -

# ==================| INPUT FRAME |==================
input_FRAME = ttk.Frame(master= window, width=400, height=700)
input_FRAME.pack_propagate(False)
# s.configure('TFrame', background='red')

# > ------ zipcode frame ------
zipcode_ROW = ttk.Frame(master= input_FRAME)
zipcode_label = ttk.Label(master= zipcode_ROW,
                            text= "ZIPCODE: ", 
                            font= HEADER_FONT)
zipcode_field = ttk.Entry(master= zipcode_ROW, textvariable= zipcode_int)
# zipcode_field.insert(0, "Enter text here")  # Set default text

zipcode_label.pack(side= 'left')
zipcode_field.pack(side= 'left')
zipcode_ROW.pack(pady=(20,0))

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
theme_button = tk.Button(dayNight_ROW, image=noTheme, bd=0, command=switchThemeButton)

day_button.pack(side='left')
theme_button.pack(side='left')
dayNight_ROW.pack()

# > ------ generate button ------
generate = PhotoImage(file="assets/GENERATE.png")
generate_button = tk.Button(master= input_FRAME,  image=generate, bd=0, command=generate_helper)

generate_button.pack(side='bottom')
input_FRAME.pack(side='left', pady=50)

# !#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#
#        DISPLAYS CONTENT BEFORE API IS CALLED
# !#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#

# ==================| OUTPUT FRAME |==================
output_FRAME = ttk.Frame(master= window, width=800, height=700)
output_FRAME.pack_propagate(False)

# ------------------| CONTENT FRAME |-----------------
content_FRAME = ttk.Frame(master= output_FRAME)

# Default OUTPUT frame contents
outputCover_label = ttk.Label(master= content_FRAME, text= "Generate your day out!", font= "Calibri 25")
outputCover_label.pack(padx=100, pady= 100)

# @TODO: Add "Make my selection" Button HERE (Content_FRAME)
content_FRAME.pack(side='top', pady=(50, 0))
# ---------------------------------------
output_FRAME.pack(side='right')
# =======================================

# === RUN ===
window.mainloop()