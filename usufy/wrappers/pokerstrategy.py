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

from platforms import Platform

class Pokerstrategy(Platform):
	""" 
		A <Platform> object for Pokerstrategy.
	"""
	def __init__(self):
		""" 
			Constructor... 
		"""
		self.platformName = "Pokerstrategy"
		self.tags = ["gambling", "poker"]
		self.NICK_WILDCARD = "<HERE_GOES_THE_NICK>"
		self.url = "http://es.pokerstrategy.com/community/profile/" + self.NICK_WILDCARD
		self.notFoundText = ["Disculpa, ¡la página no se ha encontrado!"]
		self.score= 10.0	
