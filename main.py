import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from generate_activities import generate_activities
from Event import *

# ==================| MAIN WINDOW |==================
window = tk.Tk()
s = ttk.Style()
window.title("Day Out Generator")
window.geometry('1300x700')

# INPUT FIELDS / VARIABLES
HEADER_FONT = 'Calibri 15'
SUBHEADER_FONT = 'Calibri 13'
PARAGRAPH_FONT = 'Calibri 12'
STOP_Y_POS = 10
INFO_SUB_LABEL_POS = (5, 0)

selectedStop_str = tk.StringVar(value="")

event_list = []

selectedType_str = tk.StringVar(value="Default value")
selectedBusiness_str = tk.StringVar(value="Default value")
selectedAddress_str = tk.StringVar(value="Default value")
selectedWebsite_str = tk.StringVar(value="Default value")
selectedPrice_str = tk.StringVar(value="Default value")
selectedTopReview_str = tk.StringVar(value="Default value")
zipcode_int = tk.IntVar()

selectedFirstStop_list = []
selectedSecondStop_list = []
selectedFinalStop_list = []

activity_toggle_states = {}
dayOfWeek_toggle_states = {}
isSetToDay = True
isThemeActive = True
generateButtonPressed = False
traceID = ""

# HELPER FUNCTIONS
def generate_helper():
    global selectedFirstStop_list
    global selectedSecondStop_list
    global selectedFinalStop_list
    print("Calling Google API...")

    # TEST INPUT DATA
    event_list.append( 
        {Event("Restaurant", "RockLovers", "223 Forthcoming St", "https://RockLover.com", "Expensive", "Love this place!"), 
         Event("Activity", "PartyLovers", "124 AppleBlossom St", "https://PartyLovers.com", "Cheap", "Yeah.. it was ok"),
         Event("Dessert", "BerriesAndCream", "444 Dairy Way", "https://BerriesAndCream.com", "Medium", "WOOO WOULD TOTALLY GO BACK")
         })
    
    # @TODO: Update with event objects
    selectedFirstStop_list = ["Activity 1", "Activity 2", "Activity 3"]
    selectedSecondStop_list = ["Restaurant 1", "Restaurant 2", "Restaurant 3"]
    selectedFinalStop_list = ["Dessert 1", "Dessert 2", "Dessert 3"]
    print(f'Updated selected Lists... \nFirst: {str(selectedFirstStop_list)}\nSecond: {str(selectedSecondStop_list)}\nFinal: {str(selectedFinalStop_list)}')
    
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
    global selectedFirstStop_list   
    global selectedSecondStop_list  
    global selectedFinalStop_list  

    global HEADER_FONT
    global SUBHEADER_FONT
    global PARAGRAPH_FONT

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
    subFirstStop_label = ttk.Label(firstStop_FRAME, text="", font = SUBHEADER_FONT)

    firstStopRadioSelection_FRAME = ttk.Frame(master= firstStop_FRAME)
    
    if isSetToDay and activity_toggle_states["Activity"]: 
        # >> - - - dynamic button selection RESTAURANT- - -
        subFirstStop_label.config(text="Activity")

        # @TODO:                vvv   REPLACE WITH GENERATED VALUES    vvv
        # selectedFirstStop_list = ["Activity 1", "Activity 2", "Activity 3"]
        #                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        print(f"First at Enumeration: {str(selectedFirstStop_list)}")
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
    subSecondStop_label = ttk.Label(secondStop_FRAME, text="", font = SUBHEADER_FONT)

    secondStopRadioSelection_FRAME = ttk.Frame(master= secondStop_FRAME)

    if isSetToDay and activity_toggle_states["Restaurant"]: 
        subSecondStop_label.config(text="Restaurant")

        # @TODO:                vvv       REPLACE WITH GENERATED VALUES       vvv
        # selectedSecondStop_list = ["Restaurant 1", "Restaurant 2", "Restaurant 3"]
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
    subFinalStop_label = ttk.Label(finalStop_FRAME, text="Dessert", font = SUBHEADER_FONT)

    finalStopRadioSelection_FRAME = ttk.Frame(master= finalStop_FRAME)

    if activity_toggle_states["Dessert"]: 
        # @TODO:                vvv       REPLACE WITH GENERATED VALUES       vvv
        # selectedFinalStop_list = ["Dessert 1", "Dessert 2", "Dessert 3"]
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
                                text= "Select a stop to see more information", 
                                font= HEADER_FONT)
    
    infoTitle_label.pack(pady=25)

    # > ------ activity type display ------
    activityType_ROW = ttk.Frame(master= info_FRAME)

    activityType_label = ttk.Label(master= activityType_ROW, 
                                text= "", 
                                font= SUBHEADER_FONT)
    activityType_output_label = ttk.Label(master= activityType_ROW,
                                          text="",
                                          font= PARAGRAPH_FONT)
    
    activityType_label.pack(side='left')
    activityType_output_label.pack(side='left')
    activityType_ROW.pack(anchor='w', padx= INFO_ROW_X_SPACING, pady= INFO_ROW_Y_SPACING)
    
    # > ------ business name display ------
    business_ROW = ttk.Frame(master= info_FRAME)
    
    business_label = ttk.Label(master= business_ROW, 
                                text= "", 
                                font= SUBHEADER_FONT)
    business_output_label = ttk.Label(master= business_ROW,
                                          text="",
                                          font= PARAGRAPH_FONT)
    business_label.pack(side='left')
    business_output_label.pack(side='left')
    business_ROW.pack(anchor='w', padx= INFO_ROW_X_SPACING, pady= INFO_ROW_Y_SPACING)

    # > ------ address name display ------
    address_ROW = ttk.Frame(master= info_FRAME)
    address_label = ttk.Label(master= address_ROW, 
                                text= "", 
                                font= SUBHEADER_FONT)
    address_output_label = ttk.Label(master= address_ROW,
                                          text="",
                                          font= PARAGRAPH_FONT)
    address_label.pack(side='left')
    address_output_label.pack(side='left')
    address_ROW.pack(anchor='w', padx= INFO_ROW_X_SPACING, pady= INFO_ROW_Y_SPACING)
    
    # > ------ website link display ------
    website_ROW = ttk.Frame(master= info_FRAME)
    website_label = ttk.Label(master= website_ROW, 
                                text= "", 
                                font= SUBHEADER_FONT)
    website_output_label = ttk.Label(master= website_ROW,
                                        text="",
                                        font= PARAGRAPH_FONT)
    website_label.pack(side='left')
    website_output_label.pack(side='left')
    website_ROW.pack(anchor='w', padx= INFO_ROW_X_SPACING, pady= INFO_ROW_Y_SPACING)
    
    # > ------ price level display ------
    price_ROW = ttk.Frame(master= info_FRAME)
    price_label = ttk.Label(master= price_ROW, 
                                text= "", 
                                font= SUBHEADER_FONT)
    price_output_label = ttk.Label(master= price_ROW,
                                        text="",
                                        font= PARAGRAPH_FONT)
    price_label.pack(side='left')
    price_output_label.pack(side='left')
    price_ROW.pack(anchor='w', padx= INFO_ROW_X_SPACING, pady= INFO_ROW_Y_SPACING)
    
    # > ------ top review display ------
    topReview_ROW = ttk.Frame(master= info_FRAME)
    topReview_label = ttk.Label(master= topReview_ROW, 
                                text= "", 
                                font= SUBHEADER_FONT)
    topReview_output_label = ttk.Label(master= topReview_ROW,
                                        text="",
                                        font= PARAGRAPH_FONT)
    topReview_label.pack(side='left')
    topReview_output_label.pack(side='left')
    topReview_ROW.pack(anchor='w', padx= INFO_ROW_X_SPACING, pady= INFO_ROW_Y_SPACING)

    def update_info_label(*args):
        '''
        Updates the info labels to match the selected
        radio button

        Needs to be beneath the labels to update

        selectedStop_str = tk.StringVar(value="")
        selectedType_str = tk.StringVar()
        selectedBusiness_str = tk.StringVar()
        selectedAddress_str = tk.StringVar()
        selectedWebsite_str = tk.StringVar()
        selectedPrice_str = tk.StringVar()
        selectedTopReview_str = tk.StringVar()

        '''
        # OUTPUT data
        selection = selectedStop_str.get()
        type = selectedType_str.get()
        business = selectedBusiness_str.get()
        address = selectedAddress_str.get() 
        website = selectedWebsite_str.get()
        price = selectedPrice_str.get()
        review = selectedTopReview_str.get()

        if selection: 
            # Show title
            infoTitle_label.config(text=selection)

            #Show labels
            activityType_label.config(text= "Type: ")
            business_label.config(text= "Business: ")
            address_label.config(text= "Address: ")
            website_label.config(text= "Website: ")
            price_label.config(text= "Price: ")
            topReview_label.config(text= "Top Review: ")

            #Show output
            activityType_output_label.config(text=type)
            business_output_label.config(text=business)
            address_output_label.config(text=address)
            website_output_label.config(text=website)
            price_output_label.config(text=price)
            topReview_output_label.config(text=review)
            
        else:
            # Reset label values
            infoTitle_label.config(text= "Select a stop to see more information")
            activityType_label.config(text= "")
            business_label.config(text= "")
            address_label.config(text= "")
            website_label.config(text= "")
            price_label.config(text= "")
            topReview_label.config(text= "")
              
    traceID = selectedStop_str.trace('w', update_info_label)
    info_FRAME.pack(side= 'right')
# - - - - - - - - - - - - - - - - - - - -

# ==================| INPUT FRAME |==================
input_FRAME = ttk.Frame(master= window, width=500, height=700)
input_FRAME.pack_propagate(False)
# s.configure('TFrame', background='red')

# > ------ field frame ------
field_FRAME = ttk.Frame(master= input_FRAME, width= 500, height=225, relief="raised")
field_FRAME.pack_propagate(False)

# >> ------ zipcode frame ------
zipcode_ROW = ttk.Frame(master= field_FRAME)
zipcode_label = ttk.Label(master= zipcode_ROW,
                            text= "ZIPCODE: ", 
                            font= SUBHEADER_FONT)
zipcode_field = ttk.Entry(master= zipcode_ROW, textvariable= zipcode_int)
# zipcode_field.insert(0, "Enter text here")  # Set default text

zipcode_label.pack(side= 'left')
zipcode_field.pack(side= 'left')
zipcode_ROW.pack(pady=(20,0))

# >> ------ activity preference frame ------
# NOTE: button values are stored in activity_toggle_states

activityPref_ROW = ttk.Frame(master= field_FRAME)
activities = ["Restaurant", "Activity", "Dessert"]

for i, activity in enumerate(activities):
    btn = create_toggle_button(activityPref_ROW, activity, 10, 1, activity, True, activity_toggle_states)
    btn.grid(row=0, column=i, padx=5, pady=5)

activityPref_ROW.pack()

# >> ------ day of week ------
# NOTE: button values are stored in dayOfWeek_toggle_states
dayOfWeek_ROW = ttk.Frame(master= field_FRAME)
dayOfWeek = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

for i, day in enumerate(dayOfWeek):
    btn = create_toggle_button(dayOfWeek_ROW, day, 5, 1, day, False, dayOfWeek_toggle_states)
    btn.grid(row=0, column=i, padx=5, pady=5)

dayOfWeek_ROW.pack()

# >> ------ day/night AND theme  ------
dayNight_ROW = ttk.Frame(master= field_FRAME)   

day = PhotoImage(file="assets/switchDAY.png")
night = PhotoImage(file="assets/switchNIGHT.png")
day_button = tk.Button(dayNight_ROW, image=day, bd=0, command=switchDayButton)

theme = PhotoImage(file="assets/THEME.png")
noTheme = PhotoImage(file="assets/NO_THEME.png")
theme_button = tk.Button(dayNight_ROW, image=noTheme, bd=0, command=switchThemeButton)

day_button.pack(side='left')
theme_button.pack(side='left')
dayNight_ROW.pack()

# >> ------ generate button ------
generate = PhotoImage(file="assets/GENERATE.png")
generate_button = tk.Button(master= field_FRAME,  image=generate, bd=0, command=generate_helper)

generate_button.pack(pady=15)

# >> -----------------------------
field_FRAME.pack(padx=25)

# > ------ final selection frame ------
finalSelection_FRAME = ttk.Frame(master= input_FRAME)
# @TODO: Have the final selection display here

finalSelection_FRAME.pack()
# > -----------------------------
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
content_FRAME.pack(side='top', pady=(50, 0), padx=50)
# ---------------------------------------
output_FRAME.pack(side='right')
# =======================================

# === RUN ===
window.mainloop()