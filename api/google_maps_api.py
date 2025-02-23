import os
import requests
from dotenv import load_dotenv
from .exceptions import GoogleMapsAPIError, ValidationError

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_places_for_department(department):
    """獲取特定科別的醫療機構位置"""
    if not GOOGLE_MAPS_API_KEY:
        raise GoogleMapsAPIError("Missing Google Maps API configuration", 500)
        
    if not department or not isinstance(department, str):
        raise ValidationError("Department must be a non-empty string")

    try:
        search_query = f"{department} 診所 醫院"
        places_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        
        response = requests.get(
            places_url,
            params={
                'query': search_query,
                'key': GOOGLE_MAPS_API_KEY,
                'language': 'zh-TW',
                'region': 'tw'
            }
        )
        
        if response.status_code != 200:
            error_message = response.json().get('error_message', 'Unknown error')
            raise GoogleMapsAPIError(f"Google Maps API request failed: {error_message}", response.status_code)
            
        try:
            places = response.json().get('results', [])
            
            filtered_places = [
                place for place in places
                if place.get('rating', 0) >= 4.0 and
                place.get('user_ratings_total', 0) >= 50
            ]
            
            top_places = filtered_places[:5]
            
            return [
                {
                    "name": place['name'],
                    "place_id": place['place_id'],
                    "x": place['geometry']['location']['lng'],
                    "y": place['geometry']['location']['lat']
                }
                for place in top_places
            ]
            
        except KeyError as e:
            raise GoogleMapsAPIError(f"Invalid response format from Google Maps API: {str(e)}, response: {places}")
            
    except requests.RequestException as e:
        raise GoogleMapsAPIError(f"Network error while calling Google Maps API: {str(e)}") 