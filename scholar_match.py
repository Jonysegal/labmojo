import json
import validators
from libs.scholarly import scholarly  # Emile made edits to Scholarly so including in the repo
from urllib.parse import urlparse

from utils import clean_result_before_save

"""

Search Scholar for the Researchers

* data/leads :: is the raw data from universities that we are querying
* data/noresults :: is for the people that we could not find in Scholar
* data/results :: is for the people we could match to an ID in Scholar

"""


name = 'test'
LEADS = 'data/leads/%s.json' % name
RESULTS = 'data/scholar/gs_profile/%s-results.json' % name
NO_RESULTS = 'data/scholar/no_gs_profile/%s-noresults.json' % name

################################################################################
# Master File Writing function
################################################################################


def save_file(pi, file_name):
    m = open(file_name,'a')  # Amend mode
    json.dump(pi, m)  # Write JSON
    m.write(',')  # Add comma
    m.write('\n')
    m.close()  # Close the file
    return


################################################################################
# Saving Result
################################################################################


def save_result(pi, result):
    try:
        # result.fill()
        pi['scholarly'] = result.__dict__
        print("*** Success: %s == %s // %s - %s" % (
            pi['name'],
            result.name,
            pi['email_host'],
            result.email
        ))
        print('****************************************')
        pi = clean_result_before_save(pi)
        save_file(pi, RESULTS)
    except Exception as e:
        print("Error: " + str(e))
        import pdb; pdb.set_trace()


################################################################################
# Finding the best results
################################################################################


def find_best_result(pi, results):

    for r in results:
        # Need to also make sure the name is a match
        cleaned_name = orient_name(r.name)
        r_firstname = cleaned_name.split()[0]
        r_lastname = cleaned_name.split()[-1]
        cleaned_email = get_clean_email(r.email)

        # Exact match
        if r.name == pi['name'] and cleaned_email in pi['email_host']:
            return r

        # matching name
        if r_lastname in pi['name'] and r_firstname in pi['name']:
            return r

        # Try matching partial name and email
        cleaned_email = r.email.replace('@', '')
        if r_lastname in pi['name'] and cleaned_email in pi['email_host']:
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

def orient_name(name):
    # Some sort of title
    cleaned_name = remove_crud_at_start(name)
    # Is the comman with first word or at end ?
    if ',' in cleaned_name and ',' not in cleaned_name.split()[0]:
        # Some sort of title because comma at end
        cleaned_name = remove_crud_at_end(cleaned_name)
    elif ',' in name and name.count(',') == 1:
        # last name, first name
        split_name = name.split(',')
        cleaned_name = "%s %s" % (split_name[-1], split_name[0])
    return cleaned_name.strip()

def remove_crud_at_start(name):
    # Remove a first initial
    first_word = name.split()[0]
    if len(first_word) == 2 and '.' in first_word:
        name.replace(first_word, '').strip()

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
        'Jr.',
    ]
    for x in remove_list:
        name = name.replace(x, '')
    return name

def get_lastname(pi):
    return pi['cleaned_name'].strip().split()[-1]


################################################################################
# Search Scholarly
################################################################################

def get_queries(pi):
    queries = [
         "%s %s" % (pi['name'], pi['email_host']),  # Search what came from website
         "%s %s %s" % (pi['firstname'], pi['lastname'], pi['email_host']),  # By scrubbed name
         "%s %s %s" % (pi['firstname'][0], pi['lastname'], pi['email_host']),  # search by First Initial
         "%s %s %s" % (pi['lastname'], pi['firstname'], pi['email_host']),  # search by Lastname, First Name
         "%s, %s %s" % (pi['lastname'], pi['firstname'][0], pi['email_host']),  # search by Lastname, First Initial
    ]
    # See if the same and then remove
    query_set = set()
    for q in queries:
        query_set.add(q)
    return list(query_set)

def scholarly_search(pi):
    for x in get_queries(pi):
        if not 'scholarly' in pi:
            pi = query_scholarly(pi, x)

    if not 'scholarly' in pi:
        save_file(pi, NO_RESULTS)
        print("-----------------Not Found----------------------------")


################################################################################
# Clean Name
################################################################################

def get_cleaned_name(name):
    cleaned_name = orient_name(name)
    cleaned_name = remove_crud_at_start(cleaned_name)
    cleaned_name = remove_crud_at_end(cleaned_name)
    return cleaned_name

def set_cleaned_name(pi):
    pi['cleaned_name'] = get_cleaned_name(pi['name'])
    return pi

def has_two_names(pi):
    if len(pi['cleaned_name'].split()) > 1:
        return True
    return False

def set_first_name(pi):
    names = pi['cleaned_name'].split()

    # Middle Initial
    if '.' in names[-1]:
        names.remove(names[-1])

    if ',' in names[0]:
        firstname = names[1]
    else:
        firstname = names[0]
    pi['firstname'] = firstname
    return pi

def set_last_name(pi):
    pi['lastname'] = get_lastname(pi)
    return pi


################################################################################
# Clean Email
################################################################################


def get_clean_email(email):
    email = email.replace('mailto:', '')
    host_name = email.split('@')[-1]
    if host_name.count('.') > 1:
        subs = host_name.split('.')
        return "%s.%s" % (subs[-2], subs[-1])
    return host_name

def set_email_host(pi):
    pi['email_host'] = get_clean_email(pi['email'])
    return pi


def create_email_from_website(pi):
    sites = ['website', 'lab_website', 'personal_website']
    while not pi.get('website') and len(sites):
        for site in sites:
            if pi.get(site) and validators.url(pi.get(site)):
                pi['email'] = "@" + urlparse(pi[site]).hostname
            sites.remove(site)
    return

################################################################################
# Set Data
################################################################################


def set_initial_data(pi):
    pi = set_email_host(pi)
    pi = set_cleaned_name(pi)
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
        # Need to add something to replace any null fields with "", currently doing this manually
        for pi in data['data']:

            # Filter out the ones without a name and not Lectureres/ Emeritus
            if pi.get('name') and not 'Lecturer' in pi.get('title') and not 'Emeritus' in pi.get('title'):

                # If missing, give a url for the email
                if not 'email' in pi:
                    create_email_from_website(pi)
                elif pi['email'] == "":
                    create_email_from_website(pi)
                else:
                    pass

                # If do not have some sort of email, then adios
                if pi.get('email'):
                    # Set some initial data before search
                    pi = set_initial_data(pi)
                    # Check before searching
                    if has_two_names(pi):
                        # Search Google Scholar
                        scholarly_search(pi)

                        # Then search Scopus

        print("End")
