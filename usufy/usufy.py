# !/usr/bin/python
# -*- coding: cp1252 -*-
#
##################################################################################
#
#	This program is free software: you can redistribute it and/or modify
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
""" 
usufy.py Copyright (C) F. Brezo and Y. Rubio (i3visio) 2014
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
For details, run:
	python usufy.py --license
"""
__author__ = "Felix Brezo, Yaiza Rubio "
__copyright__ = "Copyright 2014, i3visio"
__credits__ = ["Felix Brezo", "Yaiza Rubio"]
__license__ = "GPLv3"
__version__ = "v1.0.2"
__maintainer__ = "Felix Brezo"
__email__ = "contacto@i3visio.com"

import argparse
import urllib2
import os

from multiprocessing import Process, Queue
import time

import config_usufy as config

def resultsToCSV(res):
	""" Method to generate the text to be appended to a CSV file.

	Return values:
		csvText as the string to be written in a CSV file.				
	"""
	print "Generating .csv..."
	csvText = ""
	for r in res.keys():
		for p in res[r].keys():
			csvText += str(r) + ";" + str(p) + ";" + res[r][p] + "\n" 
	return csvText

def resultsToJson(profiles):
        """ 
                Method to generate the text to be appended to a Json file.
		
		List of parameters that the method receives:
		profiles:	a dictionary with the information of the profiles

                Return values:
                        jsonText as the string to be written in a Json file.                              
        """
	print "Generating .json..."
	import json
	aux = {}
	for user in profiles.keys():
		aux[user] = {}
		for platform in profiles[user].keys():
			aux[user][str(platform)]  = profiles[user][platform]
        jsonText =  json.dumps(aux)
        return jsonText
	
def getPageWrapper(p, nick, rutaDescarga, avoidProcessing, outQueue=None):
	"""
		Method that wraps the call to the getUserPage.

		List of parameters that the method receives:
		p:		platform where the information is stored.
		nick:		nick to be searched.
		rutaDescarga:	local file where saving the obtained information.
		avoidProcessing:boolean var that defines whether the profiles will NOT be processed (stored in this version).
		outQueue:	Queue where the information will be stored.

                Return values:
			None if a queue is provided. Note that the values will be stored in the outQueue
			Else (p, url).
	"""
	print "\tLooking for profiles in " + str(p) + "..."
	url = p.getUserPage(nick, rutaDescarga, avoidProcessing)			
	if url != None:
		if outQueue != None:
			print "\t" + str(p) +" - User profile found:\t" + url
			# Storing in the output queue the values
			outQueue.put((p, url))
		else:
			# If no queue was given, return the value normally
			return (p, url)
	else:
		print "\t" + str(p) +" - User profile not found..."	

def processNickList(nicks, platforms=None, rutaDescarga=None, avoidProcessing=True):
	""" 
		Method that receives as a parameter a series of nicks and verifies whether those nicks have a profile associated in different social networks.

		List of parameters that the method receives:
		nicks:		list of nicks to process.
		platforms:	list of <Platform> objects to be processed. 
		rutaDescarga:	local file where saving the obtained information.
		avoidProcessing:boolean var that defines whether the profiles will NOT be processed (stored in this version).

		Return values:
			Returns a dictionary where the key is the nick and the value another dictionary where the keys are the social networks and te value is the corresponding URL.
	"""
	if platforms == None:
		platforms = config.getPlatforms()

	res = {}

	# Processing the whole list of terms...
	for nick in nicks:
		print "Processing " + nick + "..."
		# defining the Queue where the results will be stored
		outQueue = Queue()

		# List of processes to be used
		processes = []
		for p in platforms:
			# We're setting all the arguments to be used, adding the output queue
			proc = Process(target= getPageWrapper, args= (p, nick, rutaDescarga, avoidProcessing, outQueue))
			# Adding the process to a list:
			processes.append(proc)
			# Starting the computing of the process... 
		    	proc.start()

		# Wait for all process to finish
		for p in processes:
			p.join()

		profiles = {}

		# Recovering all results and generating the dictionary
		while not outQueue.empty():
			# Recovering the results
			p, url = outQueue.get() 
			profiles[p] = url

		# Storing in a global variable to be returned
		res[nick] = profiles
	return res

if __name__ == "__main__":
	print "usufy.py Copyright (C) F. Brezo and Y. Rubio (i3visio) 2014"
	print "This program comes with ABSOLUTELY NO WARRANTY."
	print "This is free software, and you are welcome to redistribute it under certain conditions."
	print "For details, run:"
	print "\tpython usufy.py --license"
	print ""

	parser = argparse.ArgumentParser(description='usufy.py - Piece of software that checks the existence of a profile for a given user in a bunch of different platforms.', prog='usufy.py', epilog='Check the README.md file for further details on the usage of this program.', add_help=False)
	parser._optionals.title = "Input options (one required)"

	# Defining the mutually exclusive group for the main options
	general = parser.add_mutually_exclusive_group(required=True)
	# Adding the main options
	general.add_argument('--info', metavar='<action>', choices=['list_platforms', 'list_tags'], action='store', help='select the action to be performed amongst the following: list_platforms (list the details of the selected platforms) or list_tags (list the tags of the selected platforms).')
	general.add_argument('-l', '--list',  metavar='<path_to_nick_list>', action='store', type=argparse.FileType('r'), help='path to the file where the list of nicks to verify is stored (one per line).')
	general.add_argument('-n', '--nicks', metavar='<nick>', nargs='+', action='store', help = 'the list of nicks to process (at least one is required).')

	# Selecting the platforms where performing the search
	groupPlatforms = parser.add_argument_group('Platform selection arguments', 'Criteria for selecting the platforms where performing the search.')
	groupPlatforms.add_argument('-p', '--platforms', metavar='<platform>', choices=['all', 'badoo', 'blip', 'dailymotion', 'delicious', 'douban','ebay', 'facebook', 'foursquare', 'github',  'googleplus', 'hi5', 'instagram', 'karmacracy', 'klout', 'myspace', 'pastebin', 'scribd', 'slideshare', 'pinterest', 'qq', 'tumblr', 'twitter', 'vk', 'youtube'], default = [], nargs='+', required=False, action='store', help='select the platforms where you want to perform the search amongst the following: all, badoo, blip, dailymotion, delicious, douban, ebay, facebook, foursquare, github, googleplus, hi5, instagram, karmacracy, klout, myspace, pastebin, pinterest, qq, scribd, slideshare, tumblr, twitter, vk, youtube. More than one option can be selected.')
	groupPlatforms.add_argument('-t', '--tags', metavar='<tag>', default = [], nargs='+', required=False, action='store', help='select the list of tags that fit the platforms in which you want to perform the search. More than one option can be selected.')

	# Configuring the processing options
	groupProcessing = parser.add_argument_group('Processing arguments', 'Configuring the way in which usufy will process the identified profiles.')
        groupProcessing.add_argument('-a', '--avoid_processing', required=False, action='store_true', default=False, help='argument to force usufy NOT to process the downloaded valid profiles.')
	groupProcessing.add_argument('-e', '--extension', metavar='<sum_ext>', nargs='+', choices=['csv', 'json'], required=False, action='store', help='output extension for the summary files (at least one is required).')
	groupProcessing.add_argument('-o', '--output_folder', metavar='<path_to_output_folder>', required=False, action='store', help='output folder for the generated documents. While if the paths does not exist, usufy.py will try to create; if this argument is not provided, usufy will NOT write any down any data. Check permissions if something goes wrong.')

	# About options
	groupAbout = parser.add_argument_group('About arguments', 'Showing additional information about this program.')
	groupAbout.add_argument('-h', '--help', action='help', help='shows the version of the program and exists.')
        groupAbout.add_argument('--license', required=False, action='store_true', default=False, help='shows the GPLv3 license.')
	groupAbout.add_argument('--version', action='version', version='%(prog)s 0.1', help='shows the version of the program and exists.')

	args = parser.parse_args()	

	if args.license:
		print "Looking for the license..."
		# mostramos la licencia
		try:
			with open ("COPYING", "r") as iF:
				contenido = iF.read().splitlines()
				for linea in contenido:	
					print linea
		except Exception:
			print "ERROR: there has been an error when opening the COPYING file."
			print "\tThe file contains the terms of the GPLv3 under which this software is distributed."
			print "\tIn case of doubts, verify the integrity of the files or contact contacto@i3visio.com."

	else:
		# Recovering the list of platforms to be launched
		listPlatforms = config.getPlatforms(args.platforms, args.tags)

		# Executing the corresponding process...
		if not args.info:
			# Defining the list of users to monitor
			nicks = []

			if args.nicks:
				nicks = args.nicks
			else:
				# Reading the nick files
				try:
					nicks = args.list.read().splitlines()
				except:
					print "ERROR: there has been an error when opening the file that stores the nicks."
					print "\tPlease, check the existence of this file."		

			if args.output_folder != None:	
				# if Verifying an output folder was selected
				print "Creating the output folder..."
				if not os.path.exists(args.output_folder):
					os.makedirs(args.output_folder)
				# Launching the process...
				res = processNickList(nicks, listPlatforms, args.output_folder, args.avoid_processing)
			else:
				res = processNickList(nicks, listPlatforms)
					
			# Generating summary files for each ...
			if args.extension:
				# Storing the file...
				if not args.output_folder:
					args.output_folder = "./"
				else:
					# Verifying if the outputPath exists
					if not os.path.exists (args.output_folder):
						os.makedirs(args.output_folder)
				if  "csv" in args.extension:
					with open (os.path.join(args.output_folder, "results.csv"), "w") as oF:
						oF.write( resultsToCSV(res) + "\n" )
				if  "json" in args.extension:
					with open (os.path.join(args.output_folder, "results.json"), "w") as oF:
						oF.write( resultsToJson(res) + "\n")				
			if res.keys():
				print "Summing up details..."
				for nick in res.keys():
					print nick + ":"
					print "\tPlatforms where the nick '" + nick + "' has been found..."
					tags = []
					for plat in res[nick].keys():
						print "\t\t" + str(plat) + ":\t" + res[nick][plat]		

		# Information actions...
		elif args.info == 'list_platforms':
			print "List of platforms:"
			print "------------------"
			for p in listPlatforms:
				print "\t" + str(p) + ": " + str(p.tags)
		elif args.info == 'list_tags':
			print "List of tags:"
			print "-------------"
			tags = {}
			# Going through all the selected platforms to get their tags
			for p in listPlatforms:
				for t in p.tags:
					if t not in tags.keys():
						tags[t] = 1
					else:
						tags[t] += 1
			# Displaying the results in a sorted list
			for t in tags.keys().sort():
				print "\t" + t + ": " + str(tags[t]) + "  times"
