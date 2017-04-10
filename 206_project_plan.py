## Your name: Lauren Sigurdson
## The option you've chosen: 2

# Put import statements you expect to need here!

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