import phonenumbers
import opencage
import os 
from dotenv import load_dotenv
load_dotenv()

phno = os.getenv("phno")


from phonenumbers import geocoder

pep_number = phonenumbers.parse(phno)

from phonenumbers import geocoder
location = geocoder.description_for_number(pep_number, "en")
print(location)
 
from phonenumbers import carrier

service_provider = phonenumbers.parse(phno)
service_provider_name=carrier.name_for_number(service_provider, "en")
print(service_provider_name)



from opencage.geocoder import OpenCageGeocode
geo_key=os.getenv("geo_key")

geocoder = OpenCageGeocode(key)
query = str(location)
result = geocoder.geocode(query)

lat = result[0]['geometry']['lat']
lng = result[0]['geometry']['lng']
import folium

mymap = folium.Map(location=[lat, lng], zoom_start=9)

folium.Marker([lat, lng], popup=location).add_to(mymap)

mymap.save("School_Bus_Safety_System/templates/mylocation.html")




# import requests

# API_KEY = "YOUR_GOOGLE_API_KEY"  # Replace with your Google API key

# url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + API_KEY

# # Example payload (you can customize this with real Wi-Fi or cell tower data)
# payload = {
#     "considerIp": True,  # Use the device's IP address for location
# }

# response = requests.post(url, json=payload)
# location_data = response.json()

# if "location" in location_data:
#     lat = location_data["location"]["lat"]
#     lng = location_data["location"]["lng"]
#     accuracy = location_data["accuracy"]
#     print(f"Latitude: {lat}, Longitude: {lng}, Accuracy: {accuracy} meters")
# else:
#     print("Error:", location_data)