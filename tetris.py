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
	def getDrawableCoords(self):
		result = []
		xMap = {}
		for item in self.coords:
			if item[1] not in xMap:
				xMap[item[1]] = [item[0]]
			else:
				xMap[item[1]].append(item[0])
		for item in xMap:
			xMin = min(xMap[item])
			if xMin > 0:
				xMin *=2
			for i in range(xMin,xMin+len(xMap[item])*2):
				result.append((i,item))
		return result
	def getOrigin(self):
		return self.coords[self.origin]
	def inBounds(self,coords):
		minX = min([item[0] for item in coords])
		minY = min([item[1] for item in coords])
		maxX = max([item[0] for item in coords])
		maxY = max([item[1] for item in coords])
		if minX>=0 and minY>=0 and maxX<10 and maxY<20:
			return True
		return False
	def getRotateLeftCoords(self):
		origin = self.getOrigin()
		coordsResult = [((item[0]-origin[0])*-1, (item[1]-origin[1])*-1) for item in self.coords]
		coordsResult = [((item[1]*-1+origin[0]),(item[0]+origin[1])) for item in coordsResult]
		return coordsResult
	def rotateLeft(self):
		coordsResult = self.getRotateLeftCoords()
		if self.inBounds(coordsResult):
			self.coords = coordsResult
	def getRotateRightCoords(self):
		origin = self.getOrigin()
		coordsResult = [((item[0]-origin[0])*-1, (item[1]-origin[1])*-1) for item in self.coords]
		coordsResult = [((item[1]+origin[0]),(item[0]*-1+origin[1])) for item in coordsResult]
		return coordsResult
	def rotateRight(self):
		coordsResult = self.getRotateRightCoords()
		if self.inBounds(coordsResult):
			self.coords = coordsResult
	def moveLeft(self):
		m = min([item[0] for item in self.coords])
		if m>0:
			self.coords = [(item[0]-1,item[1]) for item in self.coords]
	def getMoveLeftCoords(self):
		return [(item[0]-1,item[1]) for item in self.coords]
	def moveRight(self):	
		m = max([item[0] for item in self.coords])+1
		if m<10:
			self.coords = [(item[0]+1,item[1]) for item in self.coords]
	def getMoveRightCoords(self):
		return [(item[0]+1,item[1]) for item in self.coords]
	def moveDown(self):
		m = max([item[1] for item in self.coords])+1
		if m<20:
			self.coords = [(item[0],item[1]+1) for item in self.coords]
	def getMoveDownCoords(self):
		return [(item[0],item[1]+1) for item in self.coords]