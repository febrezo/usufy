# -*- coding: cp1252 -*-
#
##################################################################################
#
#	This file is part of usufy.py.
#
#	Usufy is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################################################################################

# Importing Classes of <Platform> objects that will be used in the script. The files are stored in the wrappers folder.
from wrappers.badoo import Badoo
from wrappers.blip import Blip
from wrappers.dailymotion import Dailymotion
from wrappers.delicious import Delicious
from wrappers.douban import Douban
from wrappers.ebay import Ebay
from wrappers.facebook import Facebook
from wrappers.favstar import Favstar
from wrappers.flickr import Flickr
from wrappers.fotolog import Fotolog
from wrappers.foursquare import Foursquare
from wrappers.getsatisfaction import Getsatisfaction
from wrappers.googleplus import GooglePlus
from wrappers.github import Github
from wrappers.hi5 import Hi5
from wrappers.instagram import Instagram
from wrappers.issuu import Issuu
from wrappers.karmacracy import Karmacracy
from wrappers.klout import Klout
#from wrappers.linkedin import Linkedin
from wrappers.myspace import Myspace
from wrappers.pastebin import Pastebin
from wrappers.pinterest import Pinterest
from wrappers.pokerstrategy import Pokerstrategy
from wrappers.qq import QQ
from wrappers.ratemypoo import Ratemypoo
from wrappers.scribd import Scribd
from wrappers.slideshare import Slideshare
from wrappers.tumblr import Tumblr
from wrappers.twitter import Twitter
from wrappers.vk import Vk
from wrappers.youtube import Youtube
# Add any additinal import here
#from wrappers.any_new_social_network import Any_New_Social_Network
# ...
# Please, notify the authors if you have written a new wrapper.

def getPlatforms(sites=["all"], tags=[]):
	""" 
		Method that defines the list of <Platform> objects to be processed... Note that <Facebook> or <Twitter> objects inherit from <Platform>.

		Return values:
			Returns a list [] of <Platform> objects.
	"""
	listAll = []
	listAll.append(Badoo())	
	listAll.append(Blip())
	listAll.append(Dailymotion())
	listAll.append(Douban())
	# Pending of solving Issue #03
	#listAll.append(Delicious())	
	listAll.append(Ebay())	
	listAll.append(Facebook())
	#listAll.append(Favstar())
	listAll.append(Flickr())
	#listAll.append(Fotolog())
	listAll.append(Foursquare())
	listAll.append(Getsatisfaction())
	listAll.append(GooglePlus())
	listAll.append(Github())
	listAll.append(Hi5())
	listAll.append(Instagram())
	listAll.append(Issuu())
	listAll.append(Karmacracy())
	listAll.append(Klout())
	# listAll.append(Linkedin())
	listAll.append(Myspace())
	listAll.append(Pastebin())
	listAll.append(Pinterest())
	listAll.append(Pokerstrategy())
	listAll.append(QQ())
	listAll.append(Ratemypoo())
	listAll.append(Scribd())
	listAll.append(Slideshare())
	listAll.append(Tumblr())
	listAll.append(Twitter())
	listAll.append(Vk())
	listAll.append(Youtube())
	# append to the list variable whatever new <Platform> object that you want to add.
	#listAll.append(Any_New_Social_Network())
	if "all" in sites:
		return listAll
	else:
		listSelected = []
		for site in listAll:

			if site.platformName.lower() in sites:
				listSelected.append(site)		
			else:
				for tag in tags:
					if tag in site.tags:
						listSelected.append(site)		
		if len(listSelected) > 0:
			return listSelected
		else:
			return listAll


def calculateScore(res):
	"""
		Calculating the score from a dictionary:
			{'Twitter': 'twitter.com/nick', 'Facebook': 'facebook.com/nick', ...}

		Values returned:
			score:	a float number.
	"""
	score = 0.0
	# recovering all the possible platforms
	platforms = getPlatforms()

	for p in platforms:
		for r in res.keys():
			if r == str(p):
				score += p.score
			if score >= 100.00:
				score = 100.00
				break

	print "Score:\t" + str(score)
	
	return score

