#UICNetidChecker by Anne Celestino
import datetime
import time
import urllib2
import HTMLParser
import json
import re
import sys
from bs4 import BeautifulSoup

class NetidCheck(object):

	def __init__(self, name=None):
		if(name is not None):
			self.user = name

	#make a web request to the uic website for the entered netid
	def get_html(self):
		html_results = []
		netid = self.user
		#Format the URL to contain the netid
		url = "http://www.uic.edu/htbin/ldap_search/index.pl?lastname=&firstname=&netid=" + netid + "&department=&style=uic&Submit=SEARCH"

		#open a connection to a website at the specified url
		w = urllib2.urlopen(url)
		#save the results
		soup = BeautifulSoup(w.read())
		#close connection to web server
		w.close()

		#search for the table that contains information about the requested netid
		for table in soup.findAll('table', id="phone-results"):
			#save the info in the table to html_results
			html_results = table

		#return html_results
		return html_results

	#function to parse the HTML table returned from get_html
	def parse_html(self, var_results):
		parse_table = []

		html_results_tr = [tr.findAll('td') for tr in var_results.findAll('tr')]

		if (len(html_results_tr) > 3):
			for row in html_results_tr:
				#clean the html table up and make it easier to parse through and look at if need be
		 		parse_table.append([cell.text.replace(u'\n', u'').replace(u'\t', u'') for cell in row]) 
		else:
			parse_table.append('This person is a student.')
		
		return parse_table

def main_funtion():

	uic_netid = ''

	if(len(sys.argv) == 1):
		uic_netid = raw_input('Netid:')
	else:
		uic_netid = sys.argv[1]

	bot = NetidCheck(uic_netid)

	#function call to open connection to website
	html = bot.get_html()
	#print html

	#if we didn't find a table called phone-results we didn't search for an active netid
	if(len(html) != 0):
		#function to take html and take out just the table
		lala = bot.parse_html(html)
		#print lala
