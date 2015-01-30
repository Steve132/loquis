import loquis
import urllib2
from google import search

@loquis.command
def google(query):
	return [list(search(query,stop=10))]

@loquis.command
def wget(query):
	return [urllib2.urlopen(query).read()]

languages={'en':{'google':google}}
