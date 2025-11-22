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
input_FRAME = ttk.Frame(master= window, width=400, height=700, relief="solid")

# > ------ zipcode frame ------
zipcode_ROW = ttk.Frame(master= input_FRAME)
zipcode_label = ttk.Label(master= zipcode_ROW,
                            text= "ZIPCODE: ", 
                            font= HEADER_FONT)
zipcode_field = ttk.Entry(master= zipcode_ROW, textvariable= zipcode_int)
zipcode_label.pack(side= 'left')
zipcode_field.pack(side= 'left')
zipcode_ROW.pack(side= 'left', padx= 5)

# > ------ activity preference frame ------
activityPref_ROW = ttk.Frame(master= input_FRAME)

activityPref_ROW.pack(side= 'left')

# > ------ day of week ------
dayOfWeek_ROW = ttk.Frame(master= input_FRAME)

dayOfWeek_ROW.pack(side= 'left')

# > ------ theme ------
theme_ROW = ttk.Frame(master= input_FRAME)

theme_ROW.pack(side= 'left')

# > ------ generate button ------
#@TODO: Button can just be linked to input_FRAME

input_FRAME.pack(side='left')

# ==================| OUTPUT FRAME |==================
output_FRAME = ttk.Frame(master= window, width=800, height=700, relief="solid")

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

activityType_ROW.pack(side='left')
# > ------ company name display ------
companyName_ROW = ttk.Frame(master= info_FRAME)

companyName_ROW.pack(side='left')
# > ------ website link display ------
websiteLink_ROW = ttk.Frame(master= info_FRAME)

websiteLink_ROW.pack(side='left')
# > ------ price level display ------
priceLevel_ROW = ttk.Frame(master= info_FRAME)

priceLevel_ROW.pack(side='left')
# > ------ top review display ------
topReview_ROW = ttk.Frame(master= info_FRAME)

topReview_ROW.pack(side='left')


info_FRAME.pack(side= 'right')
# - - - - - - - - - - - - - - - - - - - -

# @TODO: Add "Make my selection" Button HERE (Content_FRAME)
content_FRAME.pack(side='top')
# ---------------------------------------
output_FRAME.pack(side='right')
# =======================================

# === RUN ===
window.mainloop()