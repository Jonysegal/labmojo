import scholarly
import csv





names = [
"David Aylor",
"Gavin Conant",
"Michael Cowley",
"Jim Mahaffey",
"John Godwin",
"David Reif",
"Rob Smart",
"Yihui Zhou",
"David Buchwalter",
"Adam Hartstone-Rose",
"Caiti Heil",
"Brian Langerhans",
"Jennifer Landin",
"Ann Ross",
"Mary Schweitzer",
"Adrian Smith",
"Lindsay Zanno",
"Patricia Estes",
"Randy Jirtle",
"Brian Langerhans",
"Kurt Marsden",
"Heather Patisaul",
"Russell Borski",
"Jane Lubischer",
"John Meitzen",
"Russell Borski",
"Jim Brown",
"Jun Ninomiya-Tsuji",
"Frank Scholle",
"Mary Schweitzer",
"Adam Hartstone-Rose",
"Ann Ross",
"Jamie Bonner",
"Seth Kullman",
"Carolyn Mattingly",
"Yoshi Tsuji"
]

with open('researchers.csv', 'w', newline = '') as csvfile :
	reseracherWriter = csv.writer(csvfile, delimiter=' ',
                            quotechar=',', quoting=csv.QUOTE_MINIMAL)
	for name in names:
		

		search_query = scholarly.search_author(name)
		
		found = 0;
		for author in search_query:
			if("NC State" in author.affiliation or "North Carolina State" in author.affiliation or "NCSU" in author.affiliation or "ncsu" in author.affiliation):
				author.fill()
				
				found = 1;
				count20 = count19 = count18 = count17 =count16 = count15 = 0
				
				hindex = author.hindex
				fiveyearhindex = author.hindex5y;
				interests = author.interests
				university = author.affiliation;
				for pub in author.publications:
					if "year" in pub.bib:

						x = pub.bib["year"]
						if(x==2020):
							count20+=1
						if(x==2019):
							count19+=1
							
						if(x==2018):
							count18+=1
						if(x==2017):
							count17+=1
						if(x==2016):
							count16+=1
						if(x==2015):
							count15+=1
				avPubs = count20 + count19 + count18 + count17 + count16 + count15
				avPubs /= 5;
				toPrint = ""
				toPrint += name + ", " + str(hindex) + ", " + str(count20) + ", "  + str(count19) + ", " + str(count18) + ", " + str(count17) + ", " + str(count16) + ", " + str(count15) + ", " + str(avPubs) + ", " + str(fiveyearhindex)
			
				for i in range(len(interests)):
					if(i == 0): #if it's the first one, print a string for the backf of whatever
						toPrint += ", "
					if(i == len(interests)-1): #ie is last entry
						toPrint += interests[i]
					else:
						toPrint += interests[i] + " | " # using this so it doesn't seperate w/ csv file type
				toPrint += ", " + university
				print(toPrint)
		if found == 0:
			print(name + ", 0")
		
		#reseracherWriter.writerow([name, hindex, count20, count19, count18, count17, count16, count15, avPubs, '', '', '', interests])	

