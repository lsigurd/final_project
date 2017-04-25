
#Your name: Lauren Sigurdson
#Final Project: Option 2
#Final 

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
import twitter_info
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

#Write a function to get and cache data from Twitter based on a search term
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

#Write a function to get and cache data from the OMDB API with a movie title search
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

#define a class Movie to handle the Movie data 
class Movie():
	def __init__(self, movie_dict):
		self.movie_dict = movie_dict
		self.movie_id = movie_dict["imdbID"]
		self.movie_title = movie_dict["Title"]
		self.movie_director = movie_dict["Director"]
		self.IMDB_rating = movie_dict["imdbRating"]
		self.languages = movie_dict["Language"]
		self.actors = movie_dict["Actors"]
		self.awards = movie_dict["Awards"]

	#Movie class method that returns the actors in a list
	def get_actors_list(self):
		actor_string = self.actors
		self.actors_list = actor_string.split(', ')
		return self.actors_list

	#Movie class method that returns a string of all of the information about the movie
	def __str__(self):
		return "{} by {} is rated {} on imdb, the language is {}, and the actors are {}".format(self.movie_title, self.movie_director, self.IMDB_rating, self.languages, self.actors)

#create a class or classes to handle the Twitter data and make it easier for you
class Tweet():
	def __init__(self, movie_tweet, movie):
		self.movie_tweet = movie_tweet
		self.tweet_id = movie_tweet["id_str"]
		self.tweet_text = movie_tweet["text"]  
		self.user_id = movie_tweet["user"]["id_str"]
		self.movie_search = movie
		self.num_favs = movie_tweet["favorite_count"]
		self.num_user_favs = movie_tweet["user"]["favourites_count"]
		self.retweets = movie_tweet["retweet_count"]
		self.screenname = movie_tweet["user"]["screen_name"]
		self.user_mentions = movie_tweet['entities']['user_mentions']

	#Tweet class method that returns a string of all of the information about the tweet
	def __str__(self):
		return "{} is the tweet that says {} and was posted by {} because the movie {} was searched and has gotten {} favoroites and {} retweets".format(self.tweet_id, self.tweet_text, self.user_id, self.movie_search, self.num_favs, self.retweets)

#list of the 8 hashtagged movies that are searched on Twitter
Tweeted_movies = ["#LaLaLand", "#BeautyandtheBeast", "#TheLostCityofZ", "#Logan", "#Colossal", "#Deadpool", "#TheLegoBatmanMovie", "#Zootopia"]

#list of the 8 movies that are searched for on the IMDB
Movie_list = ["La La Land", "Beauty and the Beast" , "The Lost City of Z" , "Logan" , "Colossal", "Deadpool", "The Lego Batman Movie", "Zootopia"]

# Invoking function get_movie_tweets on 8 hashtagged movies and then making a list of dictionaries of the data for each tweet
Movie_tweets = []
for s in Tweeted_movies: 
	Movie_tweets.append(get_movie_tweets(s))

# Make a list of tweet instances for the 8 tweeted movies
Movie_tweet_instances = []
for i in range(len(Movie_tweets)):
	for s in Movie_tweets[i]:
		Movie_tweet_instances.append(Tweet(s, Movie_list[i]))

# Invoking function get_OMDB_data on 8 movies and then making a list of dictionaries of the data for each movie
Movie_data = []
for s in Movie_list:
	Movie_data.append(get_OMDB_API_data(s))

# Make a list of movie instances for the 8 movies
Movie_data_instances = []
for s in Movie_data:
	Movie_data_instances.append(Movie(s))

#Create a database file with 3 tables:
conn = sqlite3.connect('finalproject_tweets.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
table_spec = 'CREATE TABLE Tweets'
table_spec += '(tweet_id TEXT PRIMARY KEY, tweet_text TEXT, user_id TEXT, movie_search TEXT, num_favs INTEGER, retweets INTEGER)'
cur.execute(table_spec)

cur.execute('DROP TABLE IF EXISTS Users')
table_spec = 'CREATE TABLE Users'
table_spec += '(user_id TEXT PRIMARY KEY, screen_name TEXT, num_user_favs INTEGER)'
cur.execute(table_spec)

cur.execute('DROP TABLE IF EXISTS Movies')
table_spec = 'CREATE TABLE Movies'
table_spec += '(movie_id TEXT PRIMARY KEY, movie_title TEXT, movie_director TEXT, languages TEXT, IMDB_rating INTEGER, first_actor TEXT, awards TEXT)'
cur.execute(table_spec)

#Load data into your database!

#iterate through the tweet instances and loads the data about each tweet into the database
for s in Movie_tweet_instances:
	cur.execute('INSERT OR IGNORE INTO Tweets (tweet_id, tweet_text, user_id, movie_search, num_favs, retweets) VALUES (?, ?, ?, ?, ?, ?)', (s.tweet_id, s.tweet_text, s.user_id, s.movie_search, s.num_favs, s.retweets))

#iterate through the tweet instances and loads the data about each user into the database
for s in Movie_tweet_instances :
	cur.execute('INSERT OR IGNORE INTO Users (user_id, screen_name, num_user_favs) VALUES (?, ?, ?)', (s.user_id, s.screenname, s.num_user_favs))

#iterate through the tweet instances and loads the data about each user mentioned into the database
for s in Movie_tweet_instances:
	for u in s.user_mentions:
		unique_identifier = "user_{}".format(u['screen_name'])
		if unique_identifier in CACHE_DICTION:
			my_var = CACHE_DICTION[unique_identifier]
		else:
			my_var = api.get_user(u['screen_name'])	
			CACHE_DICTION[unique_identifier] = my_var
			f = open(CACHE_FNAME, 'w')
			f.write(json.dumps(CACHE_DICTION))
			f.close()
		cur.execute('INSERT OR IGNORE INTO Users (user_id, screen_name, num_user_favs) VALUES (?, ?, ?)', (my_var["id_str"], my_var["screen_name"], my_var["favourites_count"]))

#iterate through the movie instances and loads the data about each movie into the database
for s in Movie_data_instances:
	actors_list = s.get_actors_list()
	cur.execute('INSERT OR IGNORE INTO Movies (movie_id, movie_title, movie_director, languages, IMDB_rating, first_actor, awards) VALUES (?, ?, ?, ?, ?, ?, ?)', (s.movie_id, s.movie_title, s.movie_director, s.languages, s.IMDB_rating, actors_list[0], s.awards))

conn.commit()

#4 types of processing mechanisms: set comprehension, list comprehension, dictionary accumulation, sorting

# make a query to select all of the movies searched and screennames of the users in the tweets that were tweeted by users who have favorited more than 30,000 tweets.
query = "SELECT Users.screen_name, Tweets.movie_search FROM Tweets INNER JOIN Users ON instr(Tweets.user_id, Users.user_id) WHERE Users.num_user_favs > 30000"
cur.execute(query)
movie_screenname_tuple = cur.fetchall()
movie_list = [i[1] for i in movie_screenname_tuple]
screen_names = [i[0] for i in movie_screenname_tuple]

#make query to get the texts of all of the tweets that were tweeted by users who have favorited more than 30,000 times
query = "SELECT Tweets.tweet_text FROM Tweets INNER JOIN Users ON instr(Tweets.user_id, Users.user_id) WHERE Users.num_user_favs > 30000"
cur.execute(query)
tweet_text_tuple = cur.fetchall()
tweet_text_list = [i[0] for i in tweet_text_tuple]

#make a query to select the awards of all of the movies
query = "SELECT movie_title, awards FROM Movies"
cur.execute(query)
movie_info = cur.fetchall()

#make a dictionary where all of the movies are the keys and all of the award values are the values
award_dict = {}
for s in movie_info:
	if s[1] == "N/A":
		awards = 0
	else:
		temp_var = s[1].split(" win")
		first = temp_var[0].split()
		awards = int(first[-1])
	award_dict[s[0]] = awards

#create a list of awards for the specific movies in the movie_list (from the query)
award_list = [award_dict[s] for s in movie_list]

#zip together the lists of screennames, tweet texts, movies, and number of wins into a list of tuples
movie_tups = zip(screen_names, tweet_text_list, movie_list, award_list)
movie_tups_list = list(movie_tups)

#sort the list based on the number of awards that the movie won (from highest to lowest)
sorted_list = sorted(movie_tups_list, key=lambda movie: movie[3], reverse = True)
print(sorted_list[0])
#use counter to get the most common movie in the list of movies that were tweeted by users who favorited more than 30,000 times
movie_counter = collections.Counter(movie_list).most_common(1)
most_common_movie = movie_counter[0]

#make a query to get a list of tuples of data about each tweet that the users who have favorited more than 30,000 times have made
query = "SELECT * FROM Tweets INNER JOIN Users ON instr(Tweets.user_id, Users.user_id) WHERE Users.num_user_favs > 30000"
cur.execute(query)
tweet_data_tuple = cur.fetchall()

#make a dictionary where all of the movies (that the users with more than 30,000 favorites tweeted about) are the keys and the total number of retweets all the movies got are the values. 
retweeted_movies = {}
for s in tweet_data_tuple:
	if s[3] not in retweeted_movies:
		retweeted_movies[s[3]] = s[5]
	else:
		retweeted_movies[s[3]] += s[5]

file = open("Tweeted_movies_statistics.txt", "w")

file.write("\nTWITTER AND MOVIE STATISTICS\n")

file.write("\nDescription of statistics: This summary page gives the information on the movies that were tweeted by users who have favorited more than 30,000 times. This means that the user is very active on Twitter and might have a good oppinion on what movie to tweet about. This page also gives the number of wins that each movie got to see if that movie was actually worth tweeting about. It also gives the movie that was the most common and how many times it was tweeted by these active Twitter users. At the bottom of the page, the total number of retweets for each movie that was tweeted (by these users who have favorited more than 30,000 times) was printed. \n")

file.write("\n List of movies searched on Twitter : La La Land, Beauty and the Beast , The Lost City of Z , Logan , Colossal, Deadpool, The Lego Batman Movie, Zootopia \n \n")

for s in sorted_list:
	file.write("\nScreenname:  " +s[0])
	file.write("\nTweet Text:  " +s[1])
	file.write("\nMovie:  " +s[2])
	file.write("\nNumber of wins:  " + str(s[3]))

	for x in Movie_data_instances:
		if x.movie_title == s[2]:
			file.write("\nMovie description:  " + x.__str__())
	file.write("\n")


file.write("\nMost Common Movie: " + most_common_movie[0] + ", tweeted " + str(most_common_movie[1]) + " times\n")

file.write("\nWhere users had greater than 30,000 favorites, the total retweets for all of the tweeted movies were:\n")
for key in retweeted_movies.keys():
	file.write("	" + key + ": " + str(retweeted_movies[key]))
	file.write("\n")


#TO CLOSE YOUR DATABASE CONNECTION 
conn.close()

file.close()
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
			self.assertEqual(type(value.get_actors_list()), list)	

	def test5(self):
			my_movie = get_OMDB_API_data("Beauty and the Beast")
			value = Movie(my_movie)
			self.assertEqual(value.IMDB_rating, '8.0')

	def test6(self):
			movie_dict = get_OMDB_API_data("La La Land")
			value = Movie(movie_dict)
			self.assertEqual(value.movie_director, "Damien Chazelle")

	def test7(self):
		tweet_list = get_movie_tweets("#LaLaLand")
		value = Tweet(tweet_list[0], "La La Land")
		self.assertEqual(value.movie_search, "La La Land")

	def test8(self):
		tweet_list = get_movie_tweets("#BeautyandtheBeast")
		value = Tweet(tweet_list[0], "Beauty and the Beast")
		self.assertEqual(type(value.num_favs), int)

	def test9(self):
		tweet_list = get_movie_tweets("#Logan")
		self.assertEqual(type(tweet_list), list)

	def test91(self):
		tweets = get_movie_tweets("#Logan")
		self.assertEqual(type(tweets[3]),type({"#logan":10}))

	def test92(self):
		movie_data = get_OMDB_API_data("Logan")
		self.assertEqual(type(movie_data),type({}))

	def test93(self):
		movie_info = get_OMDB_API_data("The Blind Side")
		self.assertEqual(type(movie_info["Title"]), str)


## Remember to invoke all your tests...

unittest.main(verbosity=2) 

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)


