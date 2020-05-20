import json
import time
from scholarly import scholarly
from multiprocessing import Pool



def save_file(pi, file_name):
    m = open(file_name,'a')
    json.dump(pi, m)
    m.write(',')
    m.close()
    return

def get_email_host(pi):
    at_pos = pi['email'].find('@')
    return pi['email'][at_pos:]

def get_lastname(pi):
    return pi['name'].split()[-1]

def clean_author(pi):
    remove_list = ['nav' , '_sections', '_filled']
    for x in remove_list:
        if x in pi['scholarly']:
            del pi['scholarly'][x]

    num_coauthors = len(pi['scholarly']['coauthors'])
    if num_coauthors:
        x = 0
        while x < num_coauthors:
            pi['scholarly']['coauthors'][x] = pi['scholarly']['coauthors'][x].__dict__
            for item in remove_list:
                try:
                    del pi['scholarly']['coauthors'][x][item]
                except:
                    pass
            x += 1

    num_pubs = len(pi['scholarly']['publications'])
    if num_pubs:
        x = 0
        while x < num_pubs:
            pi['scholarly']['publications'][x] = pi['scholarly']['publications'][x].__dict__
            for item in remove_list:
                try:
                    del pi['scholarly']['publications'][x][item]
                except:
                    pass
            x += 1
    return pi

def save_result(pi, result):
    try:
        result.fill()
        pi['scholarly'] = result.__dict__
        email_host = get_email_host(pi)
        print("*** Success: %s == %s" % (
            pi['name'],
            result.name,
        ))
        pi = clean_author(pi)
        save_file(pi, 'results/results.json')
    except Exception as e:
        print("Error: " + str(e))
        import pdb; pdb.set_trace()

def find_best_match(pi, results):
    email_host = get_email_host(pi)
    maybe = []
    for r in results:
        if type(r).__name__ == 'Author':
            if email_host == r.email:
                maybe.append(r)
    for r in maybe:
        lastname = get_lastname(pi)
        if lastname in r.name:
            return r
    return None


def set_scholarly(pi, results, lastname):
    email_host = get_email_host(pi)
    result = find_best_match(pi, results)
    if result:
        save_result(pi, result)
    return pi


def query_scholarly(pi, query):
    print('Searching: %s' % query)
    results = scholarly.search_author(query)
    lastname = get_lastname(pi)
    new_pi = set_scholarly(pi, results, lastname)


def scholarly_search(pi):
    names = pi['name'].split()
    if '.' in names[0]:
        firstname = names[1]
    else:
        firstname = names[0]
    lastname = get_lastname(pi)
    print('Searching: %s' % pi['name'])
    results = scholarly.search_author(pi['name'])
    new_pi = set_scholarly(pi, results, lastname)

    # queries = [
    #     "%s %s" % (firstname, lastname),
    #      "%s %s" % (firstname[0], lastname),
    #      "%s %s" % (names[0][0], lastname)
    # ]
    #
    # for x in queries:
    #     if not 'scholarly' in new_pi:
    #         new_pi = query_scholarly(pi, x)

    if not 'scholarly' in pi:
        save_file(pi, 'results/nomatch.json')
        print("-----------------Not Found----------------------------")


if __name__ == "__main__":
    with open('all.json', 'r+') as file:
        new_data = {'data':[{}]}
        data = json.load(file)
        print("Start " + str(time.time()))
        for pi in data['data']:
            if 'email' in pi and pi['email'] != None:
                scholarly_search(pi)
            # time.sleep(2)
        # with Pool(5) as p:
        #     p.map(scholarly_search, data['data'])
        print("End " + str(time.time()))
