import requests
import os
import json
API_BASE_URL = 'https://www.universal-tutorial.com'
API_HEADER = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJfZW1haWwiOiJrb3RoaXlha2F1c2hpazI1QGdtYWlsLmNvbSIsImFwaV90b2tlbiI6IlNfb0dYSzEtczdRdEdTc3FuU0wyQjAzb3l2Mmc0QnlzT0NWQ2kzOXlSYjJwckdiVGEwRWJRSFYyNHhJSXpyNlhqbEUifSwiZXhwIjoxNjE3Njg4ODk3fQ.JqLkiRz3zEYRzaeG0lMmnEiEomVBpPRtOjtU2JCJ1yI",
    "Accept": "application/json",
}
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(ROOT_DIR, 'cache')
REGION_JSON = os.path.join(CACHE_DIR, 'region.json')

def validateRegionJson(jsonData):
    try:
        region = json.load(jsonData)
        if len(region) != 245:
            raise ValueError('All countries name not available')
    except ValueError as err:
        return False
    return True

def checkCountriesFile(country_name):
    with open(REGION_JSON,'r+') as region_file:
        if not validateRegionJson(region_file):
            response = requests.get(API_BASE_URL+'/api/countries/', headers=API_HEADER)
            if response.ok:
                with open(REGION_JSON, 'w') as region_file:
                    json.dump(response.json(), region_file, indent=4)
                    
                if country_name != None:
                    with open(REGION_JSON, "r+") as region:
                        data = json.load(region)
                        for country in data:
                            if country['country_name'].lower() == country_name: 
                                if 'states' not in country.keys():
                                    response = requests.get(API_BASE_URL+'/api/states/'+country_name, headers=API_HEADER)
                                    if response.ok:
                                        country['states'] = response.json()
                                    else:
                                        return {"status" : False, "message" : response}
                                region.seek(0)
                                json.dump(data, region, indent=4)
                                region.truncate()
                                break
            else:
                return {"status" : False, "message" : response}
    return {"status": True, "message" : "All setup complet"}
                    
def CheckRequirements(country_name = None):
    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)
    if not os.path.exists(REGION_JSON):
        open(REGION_JSON, 'a').close()
    
    return checkCountriesFile(country_name)
    
    