import requests
import os
import re
import time
from curses import wrapper

def get_token():
    return os.environ.get('FINDWORK_TOKEN')

def prepare_request(token, search, location):
    url = 'https://findwork.dev/api/jobs/'
    headers = {'Authorization': 'Token ' + token}
    params = {}
    params['search'] = search
    params['location'] = location
    return url, headers, params

def get_results(url, headers, params):
    data = requests.get(url,
                        headers = headers,
                        params = params).json()
    return data.get('results'), data.get('next')

def is_internship(role):
    match = re.compile('intern(.*)', re.IGNORECASE)
    exclude = re.compile('^(ation)?al')
    search = match.search(role)
    if not search:
        return False
    if exclude.search(search.group(1)):
        return False
    return True



if __name__ == '__main__':
    TOKEN = get_token()
    search = input('Enter search term [Leave blank if none]: ')
    location = input('Enter location [Leave blank if none]: ')
    url, headers, params = prepare_request(TOKEN, search, location)
    while url is not None:
        results, next = get_results(url, headers, params)
        for result in results:
            role = result.get('role')
            if is_internship(role):
                print(role)
        url = next
        time.sleep(1) # to avoid going over request limit