from scholarly import scholarly
# default values are shown below
proxies = {'http' : 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
scholarly.nav.use_proxy(**proxies)
# If proxy is correctly set up, the following runs through it
author = next(scholarly.search_author('Steven A Cholewiak'))
print(author)
