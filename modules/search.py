import loquis
import urllib2
from google import search

@loquis.command
def google(query):
	return [list(search(query,stop=10))]

languages={'en':{'google':google}}
