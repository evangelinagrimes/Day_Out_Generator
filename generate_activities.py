from google_api import create_service
from geopy.geocoders import Nominatim
import math
import json

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


def call_places_api(zipcode):
    global curr_zipcode
    global curr_city
    global region_code
    requests_dict = {}

    # Validate zipcode (proper number of integers)
    # Check if zipcode changed

    # If a new zipcode is put in, make a new call
    if curr_zipcode != zipcode and zipcode not in past_zipcodes: 
        past_zipcodes.append(curr_zipcode)
        curr_zipcode = zipcode
        client_secret_file = 'client_secret.json'
        API_NAME = 'places'
        API_VERSION = 'v1'
        SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

        service = create_service(client_secret_file, API_NAME, API_VERSION, SCOPES)
        
        # Find Longitude and Latitude values
        curr_latitude, curr_longitude, curr_city = zipcode_to_coords(zipcode)
        # Find Long/Lat high and low
        location_restriction_rect = create_location_restriction(curr_latitude, curr_longitude)
        # Create text queries
        place_queries = [f"Best restaurants for dinner in {curr_city}", f"Fun activities to do in {curr_city}", f"Best dessert in {curr_city}"]
        
        field_mask= 'places.displayName,places.location,places.businessStatus,places.formattedAddress,places.priceRange,places.websiteUri,places.reviewSummary,places.currentOpeningHours'

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

            write_to_json_file(response, place, zipcode)
            convert_data_to_events(response, place)

    else:
        print(f"{zipcode} has already been called")
        pass


# HELPER FUNCTIONS 
def write_to_json_file(file_data, file_name, zip):
    try: 
        with open(f"json_files/{file_name}{str(zip)}.json", 'w') as json_file:
            json.dump(file_data, json_file, indent=4)
    except Exception as e: 
        print(f"ERROR: {e}")

def convert_data_to_events(response, place):
    return None

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

if __name__ == "__main__":
    call_places_api(23456)
