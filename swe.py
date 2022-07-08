import countries_codes
import requests
import pprint
import urllib
import os

class Backend:
    def __init__(self, country_num, location):
        self.current_job = 0
        self.results = []
        ADZUNA_ID, ADZUNA_KEY = self.get_token()
        self.executer(country_num, location, ADZUNA_ID, ADZUNA_KEY)

    def executer(self, country_num, location, id, key):
        url, params = self.prepare_request(id, key, country_num, location)
        self.results = self.get_results(url, params)

    # Returns next job from the returned array
    def next_job(self):
        self.current_job += 1
        if self.current_job >= len(self.results):
            return None
        return self.results[self.current_job - 1]

    # Getting the Adzuna id, key
    def get_token(self):
        return os.environ.get('ADZUNA_ID'), os.environ.get('ADZUNA_KEY')

    # Returning the ISO3 code of a given country
    def get_country_key(self, country_num):
        return countries_codes.countries_dict[country_num]

    # Prepering the url and parameters
    def prepare_request(self, id, key, country_num, location):
        params = {}
        country_code = self.get_country_key(country_num)
        page_num = 1
        params['app_id'] = id
        params['app_key'] = key
        params['results_per_page'] = 300
        params['what_or'] = "software developer programmer" \
                            "designer ML security data product"
        params['title_only'] = "intern"
        params['where'] = location
        params['sort_by'] = "relevance"

        url = f'https://api.adzuna.com/v1/api/jobs/{country_code}' \
              f'/search/{page_num}?'
        params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return url, params

    # Get a request
    def get_results(self, url, params):
        data = requests.get(url, params=params).json()
        return data['results']


if __name__ == '__main__':

    # warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

    swe = Backend("15", "san francisco")
    print(swe.results)
