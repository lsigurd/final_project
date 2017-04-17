
#Your name: Lauren Sigurdson
#Final Project: Option 2

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

# Begin filling in instructions....


#Write function(s) to get and cache data from Twitter

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


CACHE_FNAME = "SI206_finalproject_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

#A function to get and cache data based on a search term
def get_movie_tweets(movie):
	unique_identifier = "twitter_{}".format(movie)
	if unique_identifier in CACHE_DICTION:
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		twitter_results = api.search(q = movie)
		CACHE_DICTION[unique_identifier] = twitter_results
		f = open(CACHE_FNAME,'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	movie_tweets = [] # collect 'em all!
	for tweet in twitter_results["statuses"]:
		movie_tweets.append(tweet)
	return movie_tweets
#print(get_movie_tweets("#LaLaLand"))

#A function to get and cache data about a Twitter user
# def get_user_tweets(username):
# 	unique_identifier = "twitter_{}".format(username) # seestring formatting chapter
# 	# see if that username+twitter is in the cache diction!
# 	if unique_identifier in CACHE_DICTION: # if it is...
# 		print('using cached data for', username)
# 		twitter_results = CACHE_DICTION[unique_identifier] # grab the data from the cache!
# 	else:
# 		print('getting data from internet for', username)
# 		twitter_results = api.user_timeline(username) # get it from the internet
# 		# but also, save in the dictionary to cache it!
# 		CACHE_DICTION[unique_identifier] = twitter_results # add it to the dictionary -- new key-val pair
# 		# and then write the whole cache dictionary, now with new info added, to the file, so it'll be there even after your program closes!
# 		f = open(CACHE_FNAME,'w') # open the cache file for writing
# 		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
# 		f.close()
# 	tweeter = [] # collect 'em all!
# 	for tweet in twitter_results:
# 		tweeter.append(tweet)
# 	return tweeter
# #print(get_user_tweets('UMSI'))


#Write function(s) to get and cache data from the OMDB API with a movie title search
def get_OMDB_API_data(title):
	base_url = "http://www.omdbapi.com/?"
	unique_identifier = "omdb_{}".format(title)

	if unique_identifier in CACHE_DICTION:
		movie_dict = CACHE_DICTION[unique_identifier]
	else: 
		params_diction = {}
		params_diction['t'] = title
		response = requests.get(base_url, params = params_diction)
		movie_dict = json.loads(response.text) 
		CACHE_DICTION[unique_identifier] = movie_dict 
		f = open(CACHE_FNAME,'w')
		f.write(json.dumps(CACHE_DICTION)) 
		f.close() 
	return movie_dict


#define a class Movie.
	#The constructor for class Movie accepts a dictionary called movie_dict
	#some of the instance variables are movie_title, IMDB_rating, and movie_director
class Movie(object):
	def __init__(self, movie_dict):
		self.movie_title = movie_dict["Title"]
		self.movie_director = movie_dict["Director"]
		self.IMDB_rating = movie_dict["imdbRating"]
		self.languages = movie_dict["Language"]

	def actors(self, movie_dict):
		actor_string = movie_dict["Actors"]
		self.actors = actor_string.split(', ')
		return self.actors

	def __str__(self):
		return "{} by {} is rated {} on imdb, the language is {}, and the actors are {}".format(self.movie_title, self.movie_director, self.IMDB_rating, self.languages, self.actors)

value = Movie(get_OMDB_API_data("Finding Nemo"))
value1 = value.__str__()
print(value)

#create a class or classes to handle the Twitter data and make it easier for you

#Pick at least 3 movie title search terms for OMDB. Put those strings in a list. 

#Make a request to OMDB on each of those 3 search terms

#create a list of instances of class Movie.

#Make invocations to your Twitter functions. 

La_La_Land_tweets = get_movie_tweets("#LaLaLand")
La_La_Land_data = get_OMDB_API_data("La La Land")
#print(La_La_Land_data)
my_movie = Movie(La_La_Land_data)

#Create a database file with 3 tables:

conn = sqlite3.connect('finalproject_tweets.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
table_spec = 'CREATE TABLE Tweets'
table_spec += '(tweet_id TEXT PRIMARY KEY, tweet_text TEXT, user_id TEXT, movie_search TEXT, num_favs INTEGER, retweets INTEGER)'
cur.execute(table_spec)

cur.execute('DROP TABLE IF EXISTS Users')
table_spec = 'CREATE TABLE Users'
table_spec += '(user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER)'
cur.execute(table_spec)

cur.execute('DROP TABLE IF EXISTS Movies')
table_spec = 'CREATE TABLE Movies'
table_spec += '(movie_id TEXT PRIMARY KEY, movie_title TEXT, movie_director TEXT, languages TEXT, IMDB_rating INTEGER, first_actor TEXT)'
cur.execute(table_spec)

#Load data into your database!

for s in La_La_Land_tweets:
	cur.execute('INSERT OR IGNORE INTO Tweets (tweet_id, tweet_text, user_id, movie_search, num_favs, retweets) VALUES (?, ?, ?, ?, ?, ?)', (s["id_str"], s["text"], s["user"]["id_str"], "#LaLaLand", s["user"]["favourites_count"], s["retweet_count"]))

for s in La_La_Land_tweets:
	cur.execute('INSERT OR IGNORE INTO Users (user_id, screen_name, num_favs) VALUES (?, ?, ?)', (s["user"]["id_str"], s["user"]["screen_name"], s["user"]["favourites_count"]))

for s in La_La_Land_tweets:
	for u in s['entities']['user_mentions']:
		unique_identifier = "user_{}".format(u['screen_name'])
		if unique_identifier in CACHE_DICTION:
			my_var = CACHE_DICTION[unique_identifier]
		else:
			my_var = api.get_user(u['screen_name'])	
			CACHE_DICTION[unique_identifier] = my_var
			f = open(CACHE_FNAME, 'w')
			f.write(json.dumps(CACHE_DICTION))
			f.close()
		cur.execute('INSERT OR IGNORE INTO Users (user_id, screen_name, num_favs) VALUES (?, ?, ?)', (my_var["id_str"], my_var["screen_name"], my_var["favourites_count"]))

actors_list = my_movie.actors(La_La_Land_data)
cur.execute('INSERT OR IGNORE INTO Movies (movie_id, movie_title, movie_director, languages, IMDB_rating, first_actor) VALUES (?, ?, ?, ?, ?, ?)', (La_La_Land_data["imdbID"], my_movie.movie_title, my_movie.movie_director, my_movie.languages, my_movie.IMDB_rating, actors_list[0]))

conn.commit()

#set comprehension

#list comprehension

#dictionary comprehension

#dictionary accumulation




#TO CLOSE YOUR DATABASE CONNECTION 
conn.close()

#Process the data and create an output file!

# Put your tests here, with any edits you now need from when you turned them in with your project plan.

# Write your test cases here.
class CachingTests(unittest.TestCase):
	def test_cache_diction(self):
		self.assertEqual(type(CACHE_DICTION),type({}))

	def test_cache_file(self):
		f = open("SI206_finalproject_cache.json","r")
		s = f.read()
		f.close()
		self.assertEqual(type(s),type("string"))

class RegularTest(unittest.TestCase):
	def test1_self(self):
			value = Movie(get_OMDB_API_data("Finding Nemo"))
			value1 = value.__str__()
			self.assertEqual(type(value1),str)

	def test2_init(self):
			value = Movie(get_OMDB_API_data("Twilight"))
			self.assertEqual(type(value), Movie)

	def test3(self):
			value = Movie(get_OMDB_API_data("Bridesmaids"))
			self.assertEqual(type(value.movie_title), str)

	def test4(self):
			movie = get_OMDB_API_data("Superbad")
			value = Movie(movie)
			self.assertEqual(type(value.actors(movie)), list)	

	def test5(self):
			my_movie = get_OMDB_API_data("Beauty and the Beast")
			value = Movie(my_movie)
			self.assertEqual(value.IMDB_rating, '8.0')

	def test6(self):
			movie_dict = get_OMDB_API_data("La La Land")
			value = Movie(movie_dict)
			self.assertEqual(value.movie_director, "Damien Chazelle")



## Remember to invoke all your tests...

unittest.main(verbosity=2) 

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)


