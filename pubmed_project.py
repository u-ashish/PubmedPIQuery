import sys
import numpy
import collections 
import matplotlib.pyplot as plt 
from collections import Counter
from Bio import Entrez
from Bio import Medline
Entrez.email = "ashish.uppala@nih.gov" #NCBI, Who am I?

class PI_stats(object):
	total_article_count = 0
	idlist = []
	list_of_journals = []
	years_published = []

	def __init__(self, name):
		self.name = name

	#Figure out how many articles this PI has in pubmed. 
	def total_num_articles(self):

		handle = Entrez.egquery(term=self.name)
		record = Entrez.read(handle)

		for row in record["eGQueryResult"]:
			if row["DbName"]=="pubmed":
				self.total_article_count = row["Count"]
				print(self.total_article_count)

	#Get a list of the PubMed IDs of each article (for fun...)
	def get_ID_list(self):
		handle = Entrez.esearch(db="pubmed", term=self.name, retmax=self.total_article_count)
		record = Entrez.read(handle)
		self.idlist = record["IdList"]
		return self.idlist

	#Go through pubmed and find all the publication dates as well as list of journals
	#this PI has published under.
	def get_pub_stats(self):
		handle = Entrez.efetch(db="pubmed", id=self.idlist, rettype="medline", retmode="text")
		records = Medline.parse(handle)
		records = list(records)


		for record in records:
			if not "AU" in record:
				continue
			self.list_of_journals.append(record["JT"])     #Unabbreviated journal title.
			self.years_published.append(record["DP"][0:4]) #Get publication year. 
			

	#Plot the number of articles published in each year. 
	def view_articles_per_year(self):
		c = Counter(self.years_published)
		c = collections.OrderedDict(sorted(c.items()))

		plt.bar(range(len(c)), c.values(), align='center')
		plt.xticks(range(len(c)), list(c.keys()), rotation=70)
		plt.title("Articles Published by %s per Year" % self.name)
		plt.show()

	#Plot the number of articles published in each journal (encompassing entire career).
	def view_articles_per_jour(self):
		c = Counter(self.list_of_journals)
		c = collections.OrderedDict(sorted(c.items()))

		plt.bar(range(len(c)), c.values(), align='center')
		plt.xticks(range(len(c)), list(c.keys()), rotation=70)
		plt.title("Articles Published by %s in Different Journals" % self.name)
		plt.show()


#PI_name = input("Enter the name of a researcher (Last name First_InitialMiddleInitial (e.g. Greten TF: ")
pi_name = PI_stats("wolchok jd")
pi_name.total_num_articles()
print("PMID List: ")
print(pi_name.get_ID_list())

#Now calculate stats and then visualize them!
pi_name.get_pub_stats()
pi_name.view_articles_per_jour()
pi_name.view_articles_per_year()















#Ignore below (just for my reference, it's old code... sorry).

#temp_string = "" #Stores Journal Name. 
			#temp_year = ""   #Stores Public. Year. 
			#print(record["JT"])
			#print(record["DP"][0:4])
			#for item in record["SO"]:
				
			#	if item != ".":
		#			temp_string = temp_string + item
	#			elif item == ".":
	#				self.list_of_journals.append(temp_string)
	#				temp_record = record["SO"].lstrip(temp_string+". ")
	#				#temp_string += ". "
	#				#temp_record = record["SO"][len(temp_string):]
	#				for i in range(0,4):
	##				self.years_published.append(temp_year)
	#				break

		#Just checking to see if it works.
		#print("All Journals")
		#print(self.list_of_journals)
		#print("All Publication Years")
		#print(self.years_published)
