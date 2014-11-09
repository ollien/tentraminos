import random

class Piece(object):
	def __init__(self,piece=None):
		self.piece = piece
		if self.piece==None or self.piece > 6 or self.piece < 0:
			self.piece=random.randint(0,6)
		self.coords = []
		# Horizontal Piece
		#
		# ****
		
		if self.piece == 0:
			self.coords = [(i,0) for i in range(4)]
			self.origin = 1
		# L Piece 1
		#
		# *
		# ***
		
		elif self.piece == 1:
			self.coords.append((0,0))
			self.coords += [(i,1) for i in range(3)]
			self.origin = 2
		# L Piece 2
		#
		#   *
		# ***
		
		elif self.piece == 2:
			self.coords.append((2,0))
			self.coords += [(i,1) for i in range(3)]
			self.origin = 2
		# Block Piece 
		# 
		# **
		# **
		
		elif self.piece == 3:
			self.coords.append((0,0))
			self.coords.append((1,1))
			self.coords.append((0,1))
			self.coords.append((1,0))
			self.origin = 0
		# WTF Peice 1
		#  **
		# **
		
		elif self.piece == 4:
			self.coords.append((1,0))
			self.coords.append((2,0))
			self.coords.append((0,1))
			self.coords.append((1,1))
			self.origin = 3
		# WTF Peice 2
		#
		#**
		# **
		
		elif self.piece == 5:
			self.coords.append((0,0))
			self.coords.append((1,0))
			self.coords.append((1,1))
			self.coords.append((2,1))
			self.origin = 2
		#T Peice
		#
		# *
		#***
		
		elif self.piece == 6:
			self.coords.append((1,0))
			self.coords += [(i,1) for i in range(3)]
			self.origin = 2
	def getOrigin(self):
		return self.coords[self.origin]
	def inBounds(self,coords):
		minX = min([item[0] for item in coords])
		minY = min([item[1] for item in coords])
		maxX = max([item[0] for item in coords])
		maxY = max([item[1] for item in coords])
		if minX>=0 and minY>=0 and maxX<22 and maxY>10:
			return True
		return False
	def rotateLeft(self):
		origin = self.getOrigin()
		coordsResult = [((item[0]-origin[0])*-1, (item[1]-origin[1])*-1) for item in self.coords]
		coordsResult = [((item[1]*-1+origin[0]),(item[0]+origin[1])) for item in coordsResult]
		if self.inBounds(coordsResult):
			self.coords = coordsResult
		# if m<0:
		# 	self.coords = [(item[0]-m,item[1]) for item in self.coords]
	def rotateRight(self):
		origin = self.getOrigin()
		coordsResult = [((item[0]-origin[0])*-1, (item[1]-origin[1])*-1) for item in self.coords]
		coordsResult = [((item[1]+origin[0]),(item[0]*-1+origin[1])) for item in coordsResult]
		minX = min([item[0] for item in coordsResult])
		minY = min([item[1] for item in coordsResult])
		if self.inBounds(coordsResult):
			self.coords = coordsResult
	def moveLeft(self):
		m = min([item[0] for item in self.coords])
		if m>0:
			self.coords = [(item[0]-1,item[1]) for item in self.coords]
	def moveRight(self):	
		m = min([item[0] for item in self.coords])
		if m<22:
			self.coords = [(item[0]+1,item[1]) for item in self.coords]