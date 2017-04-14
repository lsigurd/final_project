###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.

# Begin filling in instructions....

import random
import re
import requests
from bs4 import BeautifulSoup
import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3

#Write function(s) to get and cache data from Twitter

#Write function(s) to get and cache data from the OMDB API with a movie title search

#define a class Movie.
	#The constructor for class Movie accepts a dictionary called movie_dict
	#some of the instance variables are movie_title, IMDB_rating, and movie_director

#create a class or classes to handle the Twitter data and make it easier for you

#Pick at least 3 movie title search terms for OMDB. Put those strings in a list. 

#Make a request to OMDB on each of those 3 search terms

#create a list of instances of class Movie.

#Make invocations to your Twitter functions. 

#Create a database file with 3 tables:

#Load data into your database!


#Process the data and create an output file!







# Put your tests here, with any edits you now need from when you turned them in with your project plan.




# Write your test cases here.
class CachingTests(unittest.TestCase):
	def test_cache_diction(self):
		self.assertEqual(type(CACHE_DICTION),type({}))

	def test_cache_file(self):
		f = open("206finalproject_caching.json","r")
		s = f.read()
		f.close()
		self.assertEqual(type(s),type("string"))

class RegularTest(unittest.TestCase):
	def test1_self(self):
			value = Movie(movie_dict)
			value1 = value.__str__()
			self.assertEqual(type(value1),str)

	def test2_init(self):
			value = Movie(movie_dict)
			self.assertEqual(type(value), Movie)

	def test3(self):
			value = Movie(movie_dict)
			value1 = value.Actors()
			self.assertEqual(type(value1),list)

	def test4(self):
			value = Movie(movie_dict)
			self.assertEqual(type(value.movie_title),str)	

	def test5(self):
			value = Movie(movie_dict)
			self.assertEqual(type(value.IMDB_rating),int)

	def test6(self):
			value = Movie(movie_dict)
			self.assertEqual(type(value.movie_director),str)


## Remember to invoke all your tests...

unittest.main(verbosity=2) 

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)


