import os
import json
import requests
from region.setting import API_BASE_URL, API_HEADER, REGION_JSON, CheckRequirements
from region.states import allStatesByCountry

def allCitiesByState():
    requirements = CheckRequirements()
    if requirements['status']:
        country_states_list = allStatesByCountry(True)
        if country_states_list != None:
            while True:
                state_name = input("Enter state name: ").lower().strip()
                country_requirements = CheckRequirements(country_states_list['country_name'])
                if country_requirements['status']:
                    if state_name != '' and state_name in country_states_list['states_list']:
                        response = requests.get(API_BASE_URL+'/api/cities/'+state_name, headers=API_HEADER)
                        with open(REGION_JSON, "r+") as region:
                            data = json.load(region)
                            for country in data:
                                if country['country_name'].lower() == country_states_list['country_name']:
                                    for state in country['states']:
                                        if state['state_name'].lower() == state_name: 
                                            if 'cities' not in state.keys():
                                                response = requests.get(API_BASE_URL+'/api/cities/'+state_name, headers=API_HEADER)
                                                if response.ok:
                                                    state['cities'] = response.json()
                                                else:
                                                    return (response, response.json())
                                            
                                            region.seek(0)
                                            json.dump(data, region, indent=4)
                                            region.truncate()
                                            return [city['city_name'] for city in state['cities']]
                                            break
                                    break
                        break
                    else:
                        print("State name is invalid")
                        confirm = input("Are you sure again enter state name [y/n]: ")
                        if confirm == 'y':
                            continue 
                        else:
                            break
                    break
                else:
                    return country_requirements
    else:
        return requirements