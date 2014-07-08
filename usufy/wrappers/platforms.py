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

import urllib2
import os

class Platform():
	""" 
		<Platform> abstract class.
	"""
	def __init__(self):
		""" 
			Constructor without parameters...
		"""
		#self.platformName = "Abstract Class"
		# These tags will be the one used to label this platform
		#self.tags = []
		# CONSTANT OF TEXT TO REPLACE
		#self.NICK_WILDCARD = "HERE_GOES_THE_NICK"
		# Usually it will contain a phrase like  \"<HERE_GOES_THE_NICK>\" that will be the place where the nick will be included
		#self.url = "http://test.com/" + self.NICK_WILDCARD
		# Text to find when the user was NOT found
		#self.notFoundText = []
		#self.score= 0.0
		pass

	def _genURL(self, nick):
		"""	
			Private method that returns an URL for a given nick. 
			
			Return values:
				string containing a URL
		"""
		return self.url.replace(self.NICK_WILDCARD, nick)

	def _getResourceFromUser(self, url):
		""" 
			Este método privado de la clase padre puede ser sobreescrito por cada clase hija si la verificación
			a realizar es más compleja que la verificación estándar.

			Valores retornados:
				html	Si el usuario en cuestión existe en esta red social.
				None	Si el usuario en cuestión no existe en esta red social.
		"""
		try:
			recurso = urllib2.urlopen(url)
		except :
			# no se ha conseguido retornar una URL de perfil, por lo que se devuelve None
			#print ">\tERROR: Something happened when trying to recover the resource..."
			return None
		
		html = recurso.read()
	
		for t in self.notFoundText:
			# si se encuentra el contenido en cuestión que confirma que el usuario no existe
			if t in html:
				# Returning that it does not exist
				return None
		return html
	
	def getUserPage(self, nick, outputF=None, avoidProcessing=True):
		""" 
			Este método público es el que se encarga de recuperar la información de la página del usuario a buscar y de procesar si procede la descrga.
			
			List of parameters used by this method:
				nick:		nick to search
				outputF:	will contain a valid path to the outputFolder
				avoidProcessing:will define whether a further process is performed
	
			Return values:
				url	URL del usuario en cuestión una vez que se haya confirmado su validez.
				None	En el caso de que no se haya podido obtener una URL válida.
		"""
		# generando la URL para el nick dado
		url = self._genURL(nick)
		
		# en función de la respuesta, se hace la comprobación de si el perfil existe o no
		html = self._getResourceFromUser(url) 
		if html != None:
			if not avoidProcessing:
				# Storing file if the user has NOT said to avoid the process...		
					
				outputPath = os.path.join(outputF, nick)
				if not os.path.exists(outputPath):
					os.makedirs(outputPath)
				self._processProfile(os.path.join(outputPath, nick + "_" + str(self).lower()), html)
			return url
		else:
		#	raise Exception, "UserNotFoundException: the user was not found in " + self.socialNetworkName
			return None

	def _processProfile(self, oP, html):
		"""	
			Method to process an URL depending on the functioning of the site. By default, it stores the html downloaded on a file.
			This method might be overwritten by each and every class to perform different actions such as indexing the contents with tools like pysolr, for example.

			Return values:
				None
		"""
		with open (oP, "w") as oF:
			oF.write(html)
		return True

	def __str__(self):
		""" 
			Función para obtener el texto que se representará a la hora de imprimir el objeto.
			
			Return values:
				self.platformName
		"""
		return self.platformName
