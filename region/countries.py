import json
from region.setting import REGION_JSON, CheckRequirements

def allContries(check = False):
    requirements = CheckRequirements()
    if requirements['status']:
        with open(REGION_JSON, 'r') as region_file:
            return [countries['country_name'] if check == False else countries['country_name'].lower() for countries in json.load(region_file)]
    else:
        return requirements