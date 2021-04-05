import os
import json
import requests
from region.setting import API_BASE_URL, API_HEADER, REGION_JSON, CheckRequirements
from region.countries import allContries

def allStatesByCountry(check = False):
    requirements = CheckRequirements()
    if requirements['status']:
        while True:
            country_name = input("Enter country name: ").lower().strip()
            if country_name != '' and country_name in allContries(True):
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
                            if check:
                                return {'country_name': country_name , 'states_list' : [state['state_name'].lower() for state in country['states']]}
                            else:
                                return [state['state_name']for state in country['states']]
                            break
                break
            else:
                print("Country name is invalid")
                confirm = input("Are you sure again enter country name [y/n]: ")
                if confirm == 'y':
                    continue 
                else:
                    break
    else:
        return requirements