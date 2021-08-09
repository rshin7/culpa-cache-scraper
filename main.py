# This script scrapes for reviews from CULPA either through the actual website (http://www.culpa.info)
# or the Wayback Machine archives. 

# Copyright (C) 2021 Richard Shin

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

fail_counter = 0
sleep_amount = 6

url = 'https://web.archive.org/web/20210719232152/http://www.culpa.info/professors/'
#url = 'http://www.culpa.info/professors/'

def scrape_reviews(id):
    html_text = requests.get(f'{url}/{id}').text
    soup = BeautifulSoup(html_text, 'lxml')
    prof_name = soup.find('h1').text.strip()

    reviews = soup.find_all('div', class_ = ['review box','review box old'])

    data = {}
    data['prof_info'] = []
    data['reviews'] = []

    review_course = None
    review_content = None
    review_date = None

    for review in reviews:
        try:
            review_course = review.find('span', class_ = 'course_name').text
            review_content = review.find('div', class_ = 'review_content').text
            review_date = review.find('p', class_ = 'date').text.strip()
        except(AttributeError) as e:
            pass

        data['reviews'].append({
            'course_name' : review_course,
            'review_date' : review_date,
            'review_content' : review_content
        })

    data['prof_info'].append({
        'prof_name' : prof_name,
        'prof_id' : id, 
        'total_reviews' : len(data['reviews'])
    })

    with open(f'data/prof-{id}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

for i in range(1, 14152): 
    dt_string = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    
    if fail_counter >= 100:
            print(f'Failed too many times consecutively, quitting now.')
            quit()
    
    try:
        scrape_reviews(i)
        fail_counter = 0
        print(f'[{dt_string}] Success: {i} exists, saved. Fail Count Reset: {fail_counter}')
        time.sleep(sleep_amount)
    except(AttributeError, requests.exceptions.ConnectionError) as e:
        fail_counter += 1
        print(f'[{dt_string}] Fail: {i} does not exist, skipping. Fail Count: {fail_counter}')
        time.sleep(sleep_amount)
        pass
    

