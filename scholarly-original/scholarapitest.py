import scholarly

search_query = scholarly.search_author('Steven A. Cholewiak')
print(type(search_query))
print(len(list(search_query)))

author = next(search_query).fill()
print("aca");
#print(author)

print(author.hindex)
for key, val in author.publications[0].bib.items():
   if key == "year":
       print("awef")
##
##print(author.publications[0].bib["year"])
##
## as first run throug, take list of names. search and produce CSV with columns
## NAME | Hindex | Pubs 2020 | 2019 ... | 2015| av pubs per year
## methodology: foraech name in name {
              ## dictionary year to numpapers
              ## print string evaluating
              ##wow, actually seems easy
              ## if len(list(search_query)) is 0, still print the csv just make it 0's across board to indicate need other search

names = ["Len Seymour"
"Frank Leibfarth",
"Marcey Waters",
"Shawn Hingtgen",
"Leaf Huang",
"Jeff Aube",
"Max Berkowitz",
"Joseph DeSimone",
"Dorothy Erie",
"Gary Glish",
"Leslie Hicks",
"Abigail Knight",
"David Lawrence",
"Bo Li",
"Matthew Lockett",
"Andrew Moran"]
for name in names:
    print(name)


def get_pubs_by_year(author):
    for key, val in author.publications[0].bib.items():
       if key == "year":
           print("awef")
