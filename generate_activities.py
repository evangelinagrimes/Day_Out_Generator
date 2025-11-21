from google_api import create_service
import datetime


def generate_activities(time, day, zip, mile_limit, region, activityList):
    timeOfDay = time
    dayOfWeek = day
    zipcode = zip #Convert to long/lat values
    mileLimit = mile_limit
    region = region
    restaurantBool = True
    activityBool = True
    desertBool = True 
    return None

    client_secret_file = 'client_secret.json'
    API_NAME = 'places'
    API_VERSION = 'v1'
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

    service = create_service(client_secret_file, API_NAME, API_VERSION, SCOPES)


    query = 'ramen'
    request_body = {
        'textQuery': query,
        'regionCode': 'US', 
        'locationRestriction': {
            'rectangle': {
                'low': {
                    'latitude': 40.477398, 
                    'longitude': -74.259087
                },
                'high': {
                    'latitude': 40.91618, 
                    'longitude': -73.70018
                }
            }
        },
        'priceLevels': ['PRICE_LEVEL_INEXPENSIVE', 'PRICE_LEVEL_VERY_EXPENSIVE'] 
    }

    response = service.places().searchText(
        body=request_body,
        fields='*'
    ).execute()

    print(response)