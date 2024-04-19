import requests
from datetime import datetime
from models import TZDB_TIMEZONES,TZDB_ZONE_DETAILS,TZDB_ERROR_LOG

def fetch_time_zones(url):
    try:
        print("Starting...")
        # Send GET request to the specified URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Fetched response from list timezone API")
            # Parse JSON response
            data = response.json()
            TZDB_TIMEZONES.delete().execute()
            for zone in data['zones']:
                print("Fetching data for timezone:", zone.get('zoneName', ''))
                fetch_time_zone_details('http://api.timezonedb.com/v2.1/get-time-zone?key=9HA6YHYMXGNM&format=json&by=zone&zone='+zone.get('zoneName', ''))
                TZDB_TIMEZONES.create(
                    COUNTRY_CODE=zone.get('countryCode', ''),
                    COUNTRY_NAME=zone.get('countryName', ''),
                    ZONENAME=zone.get('zoneName', ''),
                    GMTOFFSET=zone.get('gmtOffset', None),
                    IMPORT_DATE=datetime.now()  # Assuming import date is None for now
                )
            print("Data inserted successfully.")
        else:
            print("Failed to fetch data. Status code:", response.status_code)
    except Exception as e:
        print("Error fetching data:", e)

def fetch_time_zone_details(url):
    try:
        # Send GET request to the specified URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            # print(data.get('zoneEnd', ''),data.get('zoneStart', ''))
            if TZDB_ZONE_DETAILS.get_or_none(
                ZONE_NAME=data.get('zoneName', ''),
                ZONESTART=data.get('zoneStart', ''),
                ZONEEND=data.get('zoneEnd', '')
            ) is None:
                TZDB_ZONE_DETAILS.create(
                    COUNTRY_CODE=data.get('countryCode', ''),
                    COUNTRY_NAME=data.get('countryName', ''),
                    ZONE_NAME=data.get('zoneName', ''),
                    GMTOFFSET=data.get('gmtOffset', None),
                    DST=data.get('dst', None),
                    ZONESTART=data.get('zoneStart', None),
                    ZONEEND=data.get('zoneEnd', None),
                    IMPORT_DATE=datetime.now()  # Store current date and time
                )
        elif response.status_code==429:
            TZDB_ERROR_LOG.create(
                ERROR_DATE=datetime.now(),
                ERROR_MESSAGE = "too many requests"
            )
    except Exception as e:
         TZDB_ERROR_LOG.create(
                ERROR_DATE=datetime.now(),
                ERROR_MESSAGE = e
            )
def main():
    # Example API endpoint URL
    url = 'http://api.timezonedb.com/v2.1/list-time-zone?key=9HA6YHYMXGNM&format=json'
    
    # Fetch and print data from the API endpoint
    fetch_time_zones(url)

if __name__ == "__main__":
    main()
