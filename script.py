import json
import time
from scholarly import scholarly

from fp.fp import FreeProxy
from multiprocessing import Pool

proxies = {'http' : 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}

proxy = FreeProxy(rand=True, timeout=1, country_id=['US', 'CA']).get()


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

def save_result(pi, result):
    try:
        result.fill()
        pi['scholarly'] = result.__dict__
        if 'nav' in pi['scholarly']:
            del pi['scholarly']['nav']
        if '_sections' in pi['scholarly']:
            del pi['scholarly']['_sections']
        if '_filled' in pi['scholarly']:
            del pi['scholarly']['_filled']
        email_host = get_email_host(pi)
        print("%s == %s" % (
            pi['name'],
            result.name,
        ))
        save_file(pi, 'results/results.json')
    except Exception as e:
        print("Error: " + str)

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


def scholarly_search(pi):
    if 'email' in pi and pi['email'] != None:
        names = pi['name'].split()
        if '.' in names[0]:
            firstname = names[1]
        else:
            firstname = names[0]
        lastname = get_lastname(pi)
        scholarly.nav.use_proxy(**proxies)
        results = scholarly.search_author(pi['name'])
        new_pi = set_scholarly(pi, results, lastname)
        if not 'scholarly' in new_pi:
            results = scholarly.search_author("%s %s" % (firstname, lastname))
            new_pi = set_scholarly(pi, results, lastname)
        if not 'scholarly' in new_pi:
            results = scholarly.search_author("%s %s" % (firstname[0], lastname))
            new_pi = set_scholarly(pi, results, lastname)
        if not 'scholarly' in pi and names[0][0] != firstname[0]:
            results = scholarly.search_author("%s %s" % (names[0][0], lastname))
            new_pi = set_scholarly(pi, results, lastname)
    if not 'scholarly' in pi:
        save_file(pi, 'results/nomatch.json')
        print("-----------------Not Found----------------------------")


if __name__ == "__main__":
    with open('all.json', 'r+') as file:
        new_data = {'data':[{}]}
        data = json.load(file)
        print("Start " + str(time.time()))
        for pi in data['data']:
            scholarly_search(pi)
            time.sleep(2)
        # with Pool(5) as p:
        #     p.map(scholarly_search, data['data'])
        print("End " + str(time.time()))
