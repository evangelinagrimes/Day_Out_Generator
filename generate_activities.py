from google_api import create_service
from geopy.geocoders import Nominatim
import math, json, csv, re, Event

# @TODO: 
#   - Go through the curr_city setting method and figure out why it's returning None

event_dict= {}
past_zipcodes = []
curr_city= ""
region_code= 'US'
curr_zipcode = 0
entertainment_type= ["adventure_sports_center", "coffee_shop", "amphitheatre", "amusement_center", "amusement_park",
                      "aquarium", "banquet_hall", "barbecue_area", "botanical_garden", "bowling_alley",
                      "casino", "comedy_club", "community_center", "concert_hall", "cultural_center",
                      "cycling_park", "dance_hall", "dog_park", "hiking_area", "historical_landmark",
                      "internet_cafe", "karaoke", "movie_rental", "movie_theater", "national_park", 
                      "night_club", "park", "roller_coaster", "planetarium", "picnic_ground", 
                      "skateboard_park", "video_arcade", "water_park", "zoo", "pub", "cat_cafe", "chocolate_factory"
]
restauraunt_type=   ["acai_shop", "afghani_restaurant", "african_restaurant", "american_restaurant", "asian_restaurant",
                    "barbecue_restaurant", "brazilian_restaurant", "buffet_restaurant", "chinese_restaurant", "fast_food_restaurant",
                    "fine_dining_restaurant", "food_court", "french_restaurant", "greek_restaurant", "hamburger_restaurant", 
                    "indian_restaurant", "indonesian_restaurant", "italian_restaurant", "japanese_restaurant", "korean_restaurant",
                    "lebanese_restaurant", "mediterranean_restaurant", "mexican_restaurant", "middle_eastern_restaurant", "pizza_restaurant",
                    "ramen_restaurant", "seafood_restaurant", "spanish_restaurant", "sushi_restaurant", "thai_restaurant", "turkish_restaurant",
                    "vegan_restaurant", "vegetarian_restaurant", "vietnamese_restaurant"
]
dessert_type=       ["acai_shop", "bakery", "candy_store", "chocolate_shop", "confectionery", "dessert_restaurant", "dessert_shop", "donut_shop",
                    "ice_cream_shop"
]
place_types=        ["Restaurant", "Activity", "Dessert"]

def generate_activities(zipcode, dayPref, isTimeSetToDay):
    global event_dict
    firstStop_list = []
    secondStop_list = []
    finalStop_list = []

    call_places_api(zipcode)

    if isTimeSetToDay: 
        # Activity > Dinner > Dessert
        create_stop_list(isTimeSetToDay, "Activity", dayPref, firstStop_list)
        create_stop_list(isTimeSetToDay, "Restaurant", dayPref, secondStop_list)
        create_stop_list(isTimeSetToDay, "Dessert", dayPref, finalStop_list)
    else:
        # Dinner > Activity > Dessert
        create_stop_list(isTimeSetToDay, "Restaurant", dayPref, secondStop_list)
        create_stop_list(isTimeSetToDay, "Activity", dayPref, firstStop_list)
        create_stop_list(isTimeSetToDay, "Dessert", dayPref, finalStop_list)

    # Sort through the input
    # This method should return three lists (first stop, second stop, final stop) 
    #   FIRST STOP: 
    #       - If DayOut: Start with activity (Open before 5PM)
    #       - If NighOut: Start with dinner (Open past 5PM)
    #   SECOND STOP:
    #       - If DayOut: Search for restaurant (Open past 5PM)
    #       - If NighOut: Search for activity (Open past 5PM)
    #   FINAL STOP:
    #       If DayOut: Will always be dessert (Open past 5PM)
    #       If NighOut: Will always be dessert (Open past 8PM)
    #
    #   Other Conditions: 
    #       - If business must be in operation
    #       - Business hours must correspond with given times
    #       - 
    return firstStop_list, secondStop_list, finalStop_list

def create_stop_list(isTimeSetToDay, place_type, dayPref, stop_list):
    checkIfOpen = 5  # 5 AM for day check
    checkIfOpenNight = 17  # 5 PM for night check
    
    # If day out, check when business opens
    # If night out, check when business closes

    for event in event_dict[place_type]:
        print(f"Filtering {event.getBusiness()}...")
        status = event.getStatus()
        businessHours = event.getBusinessHours()
        
        if status != "OPERATIONAL":
            continue
            
        print(f"Business Hours: {', '.join(f'{key}: {value}' for key, value in businessHours.items())}")
        
        time_string = businessHours.get(dayPref, "Closed")
        
        if time_string == "Closed":
            print(f"  {dayPref}: Closed, skipping...")
            continue
            
        # Split on dash to get opening and closing times
        if '-' not in time_string:
            print(f"  Unexpected format for {dayPref}: {time_string}")
            continue
        
        opening_time, closing_time = [t.strip() for t in time_string.split('-')]
        
        try:
            # Parse opening hour
            opening_hour = int(opening_time.split(':')[0])
            if 'PM' in opening_time and opening_hour != 12:
                opening_hour += 12
            elif 'AM' in opening_time and opening_hour == 12:
                opening_hour = 0
            
            # Parse closing hour
            closing_hour = int(closing_time.split(':')[0])
            if 'PM' in closing_time and closing_hour != 12:
                closing_hour += 12
            elif 'AM' in closing_time and closing_hour == 12:
                closing_hour = 0
            
            # Check if business meets time criteria
            if isTimeSetToDay:
                # Day out: check if opens early enough (before 5 PM)
                if opening_hour < checkIfOpenNight:
                    print(f"  {dayPref}: Opens at {opening_time} - Adding to list!")
                    stop_list.append(event)
                else:
                    print(f"  {dayPref}: Opens at {opening_time} - Too late")
            else:
                # Night out: check if closes late enough (after 5 PM)
                if closing_hour >= checkIfOpenNight:
                    print(f"  {dayPref}: Closes at {closing_time} - Adding to list!")
                    stop_list.append(event)
                else:
                    print(f"  {dayPref}: Closes at {closing_time} - Too early")
                    
        except (ValueError, IndexError) as e:
            print(f"  Could not parse time from: {opening_time} - {closing_time}")
    
    return stop_list


def call_places_api(new_zipcode):
    global curr_zipcode
    global curr_city
    global region_code
    global past_zipcodes
    requests_dict = {}

    # If a new zipcode is put in, make a new call
    if new_zipcode not in past_zipcodes: 
        past_zipcodes.append(new_zipcode)
        curr_zipcode = new_zipcode
        client_secret_file = 'client_secret.json'
        API_NAME = 'places'
        API_VERSION = 'v1'
        SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

        service = create_service(client_secret_file, API_NAME, API_VERSION, SCOPES)
        
        # Find Longitude and Latitude values
        curr_latitude, curr_longitude, curr_city = zipcode_to_coords(curr_zipcode)
        # Find Long/Lat high and low
        location_restriction_rect = create_location_restriction(curr_latitude, curr_longitude)
        # Create text queries
        place_queries = [f"Best restaurants for dinner in {curr_city}", f"Fun activities to do in {curr_city}", f"Best dessert in {curr_city}"]
        # Create field mask i.e. the values you want returned
        field_mask= 'places.displayName,places.location,places.businessStatus,places.formattedAddress,places.priceLevel,places.websiteUri,places.reviewSummary,places.currentOpeningHours'

        # Request Body Generator
        for i, place in enumerate(place_types):
            requests_dict[place] = {
                'textQuery': place_queries[i], 
                'includePureServiceAreaBusinesses': False,
                'locationRestriction': location_restriction_rect,
                'minRating': 3.0,
                'regionCode': region_code
        }
            
        print(f"         COMPLETED request body generation: \n{str(requests_dict)}")
        print("STARTING API call...")

        for place in place_types:
            response = service.places().searchText(
                body= requests_dict[place],
                fields= field_mask
            ).execute()

            # write_to_json_file(response, place, curr_zipcode)
            event_dict[place] = read_json_data(response, place)
            
        for key, value in event_dict.items():
            for val in value:
                print(val)

    else:
        print(f"{curr_zipcode} has already been called")

# HELPER FUNCTIONS 
# ==========================================
#       MANIPULATING FILES |Deprecated|
# ==========================================
def append_zip_to_csv(zipcode):
    """Append a ZIP code to the used_zips.csv file.
    
    Adds the ZIP code as a new row in assets/used_zips.csv to track
    which ZIP codes have been queried.
    
    :param zipcode: ZIP code to append (int or string)
    :return: None
    :raises: Prints error message if file write fails
    """
    try:
        with open("assets/used_zips.csv", 'a', newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([zipcode])
    except Exception as e:
        print(f"ERROR write_zip_to_csv: {e}")

def read_and_store_csv(file_name):
    """Read all data from a CSV file and return as a flat list.
    
    Reads all rows and columns from the CSV file and flattens them
    into a single list of values.
    
    :param file_name: Path to the CSV file to read
    :return: List containing all values from the CSV file (flattened). Returns empty list if file read fails
    :raises: Prints error message if file read fails
    """
    csv_list= []
    try:
        with open(file_name, 'r') as csv_file: 
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                for data in row:
                    csv_list.append(data)
    except Exception as e:
        print(f"ERROR read_csv: {e}")

    return csv_list

def write_to_json_file(file_data, file_name, zipcode):
    """
    Write data to a JSON file in the json_files directory.
    
    Creates a JSON file with the format: json_files/{file_name}{zipcode}.json
    
    :param file_data: Dictionary or data structure to write to JSON file
    :param file_name: Base name for the file (without extension)
    :param zipcode: ZIP code to append to filename (int or string)
    :return: None
    :raises: Prints error message if file write fails
    """
    try: 
        with open(f"json_files/{file_name}{str(zipcode)}.json", 'w') as json_file:
            json.dump(file_data, json_file, indent=4)
    except Exception as e: 
        print(f"ERROR write_to_json_file: {e}")

def read_json_data(response, place_type):
    """
    Fresh data read
    """
    event_list = []
    try: 
        print("                                             Began read_json_data...")
        for place in response['places']:
            openHours   = {}
            name        = place.get('displayName', {}).get('text', 'Unknown')
            daysOpen    = place['currentOpeningHours']['weekdayDescriptions']
            for elem in daysOpen: 
                day, time = elem.split(": ")
                if time == "Closed":
                    openHours[day] = time
                else:
                    clean_time  = re.sub(r'\s+', ' ', time).replace('–', '-')
                    openHours[day] = clean_time
            address     = place.get('formattedAddress', 'Unknown')
            website     = place.get('websiteUri', 'Unknown')
            status      = place.get('businessStatus', 'Unknown')
            review      = place.get('reviewSummary', {}).get('text', {}).get('text', 'N/A')
            priceLevel  = place.get('priceLevel', 'N/A')

            event_list.append(Event.Event(type=place_type,
                                    status=status,
                                    business=name,
                                    businessHours=openHours,
                                    address=address,
                                    website=website,
                                    priceLevel=priceLevel,
                                    reviewSummary=review))
        print("                                             Leaving read_json_file...")
    except Exception as e:
        print(f"ERROR read_json_data: {e}")
        print(place)
        return event_list 
    
    return event_list 

# ================================
#     QUERY HELPER FUNCTIONS
# ================================

def zipcode_to_coords(zipcode):
    """Convert ZIP code to latitude/longitude and get city
    
    :param zipcode: The zip code that will be converted
    :return: Tuple of (latitude, longitude, city) or (None, None, None)
    """
    try:
        geolocator = Nominatim(user_agent="day_out_generator")
        location = geolocator.geocode(str(zipcode))
        
        if location:
            # Parse the address to get the city
            address = location.raw.get('address', {})
            
            # Try different possible city fields
            city = (address.get('city') or 
                   address.get('town') or 
                   address.get('village') or 
                   address.get('municipality') or
                   'Unknown')
            
            return location.latitude, location.longitude, city
        else:
            print(f"ZIP code {zipcode} not found")
            return None, None, None
            
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None
    
def create_location_restriction(latitude, longitude, radius_km=10):
    """
    Create locationRestriction rectangle for Google Places API
    
    :param latitude: Center latitude
    :param longitude: Center longitude
    :param radius_km: Search radius in kilometers
    :return: Dictionary formatted for Google Places API locationRestriction
    """
    # Calculate offsets
    # 1 degree latitude ≈ 111 km
    lat_offset = radius_km / 111.0
    
    # 1 degree longitude varies by latitude
    lon_offset = radius_km / (111.0 * math.cos(math.radians(latitude)))
    
    return {
        'rectangle': {
            'low': {
                'latitude': latitude - lat_offset,
                'longitude': longitude - lon_offset
            },
            'high': {
                'latitude': latitude + lat_offset,
                'longitude': longitude + lon_offset
            }
        }
    }

# ================================
#     DATA CLEANING FUNCTIONS
# ================================

def convert_data_to_events(response, place):
    global event_dict


    # @TODO: implement to create event objects
    return None

if __name__ == "__main__":
    generate_activities(23456, True, {"Monday": False, "Tuesday": True, "Wednesday": True, "Thursday": False, "Friday": True, "Saturday": False, "Sunday": False})
    # read_json_file('json_files/Dessert23456.json', 'Restaurant')
    
