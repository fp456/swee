import requests
import os
import re
import time
from bs4 import BeautifulSoup

def get_token():
    return os.environ.get('FINDWORK_TOKEN')

def prepare_request(token):
    url = 'https://findwork.dev/api/jobs/'
    headers = {'Authorization': 'Token ' + token}
    params = {}
    params['search'] = input('Enter search term [Leave blank if none]: ')
    params['location'] = input('Enter location [Leave blank if none]: ')
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
    match = re.compile('^.*(software|developer|programmer|designer).*$', re.IGNORECASE)
    search = match.search(role)
    if not search:
        return False
    return True

if __name__ == '__main__':
    TOKEN = get_token()
    url, headers, params = prepare_request(TOKEN)
    count = 0
    while url is not None:

        results, next = get_results(url, headers, params)
        for result in results:
            role = result.get('role')
            if role_is_intern(role) and is_tech_role(role):
                print(role)
                count += 1
                soup = BeautifulSoup(result.get('text'), features="html.parser")
                print(soup.get_text()[:260], "...")


                ##Ask yes, next etc and add to database

        url = next
        time.sleep(1) # to avoid going over request limit
    print(count)