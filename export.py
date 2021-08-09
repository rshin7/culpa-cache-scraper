# This script compiles all the .json files in 'scraper/data/' into
# one file: all_professors.json.

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

import os
import json

list_of_json = os.listdir("data") 

#new_data = {}
new_data = []


for i in range(0, len(list_of_json)):
    
    file_name = list_of_json[i]
    print(file_name)

    with open(f'data/{file_name}') as f:
        old_data = json.load(f)

        tmp_prof_name = old_data['prof_info'][0]['prof_name']
        tmp_prof_id = old_data['prof_info'][0]['prof_id']

        new_data.append({
            'prof_id' : tmp_prof_id,
            'prof_name' : tmp_prof_name
        })

with open('all_professors.json', 'w') as new_f:
    json.dump(new_data, new_f, indent = 4, sort_keys = True)