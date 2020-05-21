import json
import time
from scholarly import scholarly


LEADS = 'nomatch-2.json'
RESULTS = 'results/nomatch-3.json'


################################################################################
# Master File Writing function
################################################################################


def save_file(pi, file_name):
    m = open(file_name,'a')  # Amend mode
    json.dump(pi, m)  # Write JSON
    m.write(',')  # Add comma
    m.close()  # Close the file
    return


################################################################################
# Pre Save Clean
################################################################################

def remove_scholarly_objects(pi, remove_list, key_name):
    num_to_remove = len(pi['scholarly'][key_name])
    if num_to_remove:
        x = 0
        while x < num_to_remove:
            pi['scholarly'][key_name][x] = pi['scholarly'][key_name][x].__dict__
            for item in remove_list:
                try:
                    del pi['scholarly'][key_name][x][item]
                except:
                    pass
            x += 1
    return pi

def clean_result_before_save(pi):
    # Master List to remove from everywhere
    remove_list = ['nav' , '_sections', '_filled']
    for x in remove_list:
        if x in pi['scholarly']:
            del pi['scholarly'][x]

    # Sections that contain Scholarly Objects
    fields = ['coauthors', 'publications']
    for field in fields:
        pi = remove_scholarly_objects(pi, remove_list, field)
    return pi


################################################################################
# Saving Result
################################################################################


def save_result(pi, result):
    try:
        result.fill()
        pi['scholarly'] = result.__dict__
        print("*** Success: %s == %s" % (
            pi['name'],
            result.name,
        ))
        pi = clean_result_before_save(pi)
        save_file(pi, 'results/results.json')
    except Exception as e:
        print("Error: " + str(e))
        import pdb; pdb.set_trace()


################################################################################
# Finding the best results
################################################################################


def find_best_result(pi, results):
    maybe = []
    for r in results:
        if type(r).__name__ == 'Author':
            if pi['email_host'] == r.email:
                maybe.append(r)
    for r in maybe:
        # Need to also make sure the name is a match
        r_firstname = r.name.split()[0]
        if pi['lastname'] in r.name and r_firstname in pi['name']:
            return r
    return None


################################################################################
# Search Scholarly
################################################################################


def query_scholarly(pi, query):
    print('Searching: %s' % query)
    results = scholarly.search_author(query)
    result = find_best_result(pi, results)
    if result:
        save_result(pi, result)
    return pi


################################################################################
# Clean The Name
################################################################################


def remove_curd_at_start(name):
    remove_list = [
        'Dr.',
    ]
    for x in remove_list:
        name = name.replace(x, '')
    return name

def remove_crud_at_end(name):
    remove_list = [
        'Ph.D.',
        'B.S.',
        'M.D.',
        'M.S.',
        ' MB',
        'BChir',
        'BSc.',
        'PhD',
        'FRCP',
        'D.V.M.',
        'Dr.',
        ', '
    ]
    for x in remove_list:
        name = name.replace(x, '')
    return name

def get_lastname(pi):

    # Test For Last Name First
    if ',' in pi['name'].split()[0]:
        return remove_crud_at_end(pi['name'].split()[0])

    # Else Last name is at the end
    cleaned_name = scrub_name(pi['name'])
    return cleaned_name.strip().split()[-1]


################################################################################
# Search Scholarly
################################################################################


def scholarly_search(pi):

    queries = [
        pi['name'],  # Search what came from website
         "%s %s" % (pi['firstname'], pi['lastname']),  # By scrubbed name
         "%s %s" % (pi['firstname'][0], pi['lastname']),  # search by First Initial
    ]
    for x in queries:
        print('Searching: %s' % x)
        if not 'scholarly' in pi:
            pi = query_scholarly(pi, x)

    if not 'scholarly' in pi:
        save_file(pi, RESULTS)
        print("-----------------Not Found----------------------------")


################################################################################
# Setup the Data to go through search
################################################################################


def has_two_names(pi):
    try:
        # Catch weird name stuff
        name = remove_curd_at_start(pi['name'])
        pi['cleaned_name'] = name
        names = name.split()
    except:
        names = 0

    if len(names) > 1:
        return True
    return False

def set_first_name(pi):
    if '.' in names[0]:
        firstname = names[1]
    else:
        firstname = names[0]
    pi['firstname'] = firstname
    return pi

def set_last_name(pi):
    pi['lastname'] = get_lastname(pi)
    return pi

def set_email_host(pi):
    at_pos = pi['email'].find('@')
    pi['email_host'] = pi['email'][at_pos:]
    return pi

def set_initial_data(pi):
    pi = set_email_host(pi)
    pi = set_first_name(pi)
    pi = set_last_name(pi)
    return pi


################################################################################
# Main
################################################################################


if __name__ == "__main__":
    with open(LEADS, 'r+') as file:
        new_data = {'data':[{}]}
        data = json.load(file)
        print("Start " + str(time.time()))
        for pi in data['data']:
            # Make sure there is an Email
            if 'email' in pi and pi['email'] != None:
                # Set some initial data before search
                pi = set_initial_data(pi)
                # Check before searching
                if has_two_names(pi):
                    # Search Scholarly
                    scholarly_search(pi)

        print("End " + str(time.time()))
