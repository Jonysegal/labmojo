import json
from libs.scholarly import scholarly

from utils import clean_result_before_save

name = 'all-results'
LEADS = 'data/scholar/gs_profile/%s.json' % name

"""
Loop over every single results
- create a file for each person

people_details/id.json

"""

def get_author_id(row):
    return row['scholarly']['id']

def save_author(author):
    file_name = "data/scholar/gs_profile/profiles/%s.json" % author.id
    m = open(file_name,'w')  # Amend mode
    cleaned_author = clean_result_before_save(author.__dict__)
    try:
        json.dump(cleaned_author, m)  # Write JSON
    except Exception as e:
        print(e)
        import pdb; pdb.set_trace()
    m.close()  # Close the file
    return

with open(LEADS) as file:
    data = json.load(file)
    for row in data['data']:
        id = row['scholarly']['id']
        author = scholarly.search_author_custom_id(id)
        author.fill()
        save_author(author)
