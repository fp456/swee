import requests
import os
import re
import time
from bs4 import BeautifulSoup
import warnings

def get_token():
    return os.environ.get('FINDWORK_TOKEN')

def prepare_request(token):
    url = 'https://findwork.dev/api/jobs/'
    headers = {'Authorization': 'Token ' + token}
    params = {}
    location =  input('Enter location ["Remote" for remote, or leave blank if none]: ')

    if "remote" in location.lower():
        params['remote'] = True
    else:
        params['location'] = location

    params['search'] = input('Enter search term [Leave blank if none]: ')
    return url, headers, params

def get_results(url, headers, params):
    data = requests.get(url,
                        headers = headers,
                        params = params).json()
    return data.get('results'), data.get('next')

def role_is_intern(role):
    match = re.compile('intern(.*)', re.IGNORECASE)
    exclude = re.compile('^(ation)?al')
    search = match.search(role)
    if not search:
        return False
    if exclude.search(search.group(1)):
        return False
    return True

def is_tech_role(role):
    match = re.compile('^.*(software|developer|programmer|designer|ML|security|data|product|engineer|engineering).*$', re.IGNORECASE)
    search = match.search(role)
    if not search:
        return False
    return True

if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
    TOKEN = get_token()
    url, headers, params = prepare_request(TOKEN)
    count = 0

    #MOVE TO FRONT

    while url is not None:

        results, next = get_results(url, headers, params)
        
        for result in results:
            role = result.get('role')
            if role_is_intern(role) and is_tech_role(role):
                print(role)
                count += 1
                soup = BeautifulSoup(result.get('text'), features="html.parser")
                
                if result.get('remote') is True:
                    print(result.get('company_name') +  " (Remote)")
                elif result.get('location') is not None:
                    if result.get('location')[-1] is " ":
                        result['location'] = result.get('location')[:-2]
                    print(result.get('company_name') + " (" + result.get('location') + ")")
                else:
                    print(result.get('company_name'))
                
                #Prints the description 
                print(soup.get_text()[:260] + "...")
                ##Ask "yes, next etc" and add to database

        url = next
        time.sleep(1) 

    print(count)







    countries_dict = {
    "1" : "Austria",
    "2" : "Brazil",
    "3":  "Canada",
    "4" : "France",
    "5" : "Germany",
    "6" : "India",
    "7" : "Italy",
    "8" : "Netherlands",
    "9" : "New Zealand",
    "10" : "Poland",
    "11" : "Russia",
    "12" : "Singapore",
    "13" : "South Africa",
    "14" : "United Kingdom",
    "15" : "us",
}