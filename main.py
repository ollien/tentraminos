import curses
import tetris
from threading import Timer
from time import sleep
from sys import exit
import os.path
import traceback

debug = False
if debug:
	f = open(os.path.join(os.path.expanduser("~"),'tetrislog.txt'),'w')
#init curses
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
curses.curs_set(0)
screen.keypad(1)
screen.nodelay(1)
screen.scrollok(1)
window = curses.newwin(25,80,0,0)
window.nodelay(1)
window.keypad(1)
window.scrollok(1)
panel = curses.newpad(20,20)
nextPanel = curses.newpad(5,15)
height,width = panel.getmaxyx()
nextHeight,nextWidth = nextPanel.getmaxyx()

#Color codes are associated with piece codes + 1
curses.init_pair(1,curses.COLOR_RED, curses.COLOR_RED)
curses.init_pair(2,curses.COLOR_MAGENTA,curses.COLOR_MAGENTA)
curses.init_pair(3,curses.COLOR_BLUE,curses.COLOR_BLUE)
curses.init_pair(4,curses.COLOR_YELLOW,curses.COLOR_YELLOW)
curses.init_pair(5,curses.COLOR_GREEN,curses.COLOR_GREEN)
curses.init_pair(6,curses.COLOR_CYAN,curses.COLOR_CYAN)
curses.init_pair(7,curses.COLOR_WHITE,curses.COLOR_WHITE)
curses.init_pair(8,curses.COLOR_BLACK,curses.COLOR_BLACK)
#The color code 10 is white on black
curses.init_pair(10,curses.COLOR_WHITE,curses.COLOR_BLACK)
window.bkgd(curses.color_pair(7))
panel.bkgd(curses.color_pair(8))
nextPanel.bkgd(curses.color_pair(8))
class Game():
	def __init__(self):
		self.pieces = []
		self.currentPiece = None
		self.timer = Timer(.5 ,self.gravityCallback)
		self.active = True
		self.flashing = False
		self.flashed = False	
		self.flashCount = 0
		self.flashMax = 60
		self.nextPiece = None
		self.flashRows = []
	def run(self):
		self.generatePiece()
		self.timer.start()
		try:
			while self.active:
				panel.clear()
				for piece in self.pieces:
					drawableCoords = piece.getDrawableCoords()
					for item in drawableCoords:
						if item[0] < width and item[0] >=0 and item[1] < height and item[1] >= 0:
							panel.move(item[1],item[0])
							try:
								if self.flashing and item[1] in self.flashRows:
									if self.flashed:
										panel.addstr(" ",curses.color_pair(7))
										self.flashCount+=1
										self.flashed = False
										if self.flashCount>=self.flashMax:
											self.flashing=False
											self.flashed = False
											self.flashCount = 0
											self.removeRow(item[1])
											self.flashRows.remove(item[1])
											self.generatePiece()
									else:
										self.flashed = True
										panel.addstr(" ",curses.color_pair(piece.piece+1))
								else:
									panel.addstr(" ",curses.color_pair(piece.piece+1))
							except curses.error:
								pass
				if self.nextPiece != None:
					drawableCoords = self.nextPiece.getDrawableCoords()
					nextPanel.clear()
					nextPanel.move(0,nextWidth/4)
					nextPanel.addstr("Next Piece",curses.color_pair(10))
					for item in drawableCoords:
						nextPanel.move(item[1]+1,item[0]-1)
						nextPanel.addstr(" ",curses.color_pair(self.nextPiece.piece+1))
				self.refresh()
				c = window.getch()
				if c==ord('q'):
					if self.isValidRotation(self.currentPiece.getRotateLeftCoords()):
						self.currentPiece.rotateLeft()
				elif c==ord('e'):
					if self.isValidRotation(self.currentPiece.getRotateRightCoords()):
						self.currentPiece.rotateRight()
				elif c==ord('a'):
					if self.isValidLeftMove(self.currentPiece.getMoveLeftCoords()):
						self.currentPiece.moveLeft()
				elif c==ord('d'):
					if self.isValidRightMove(self.currentPiece.getMoveRightCoords()):
						self.currentPiece.moveRight()
				elif c==ord('s'):
					self.downFast()
				elif c==ord(' '):
					self.getUpAndSlam()
				sleep(1.0/45)
		except Exception, e:
			if debug:
				f.write(traceback.format_exc())
				f.flush()
				print str(e)
				self.timer.cancel()
			return
	def refresh(self):
		# return False
		screen.noutrefresh()
		window.noutrefresh()
		panel.noutrefresh(0,0,0,0,height,width)
		nextPanel.noutrefresh(0,0,0,width+1,nextHeight+20,nextWidth+20)
		curses.doupdate()
	def generatePiece(self):
		if self.nextPiece == None:
			p = tetris.Piece(xOffset=3,yOffset=0)
			if not self.canSpawn(p):
				self.lose()
				return False
			self.pieces.append(p)
			self.currentPiece = p
		else:
			if not self.canSpawn(self.nextPiece):
				self.lose()
				return False
			self.pieces.append(self.nextPiece)
			self.currentPiece = self.nextPiece
		self.nextPiece = tetris.Piece(xOffset=3,yOffset=0)
	def isValidLeftMove(self,piece):
		if len(piece)>0:
			xMin = min([item[0] for item in piece])
			xMins = [item for item in piece if item[0]==xMin]
			for item in self.pieces:
				if item!=self.currentPiece and item!=piece:
					for item2 in xMins:
						if item2 in item.coords:
							return False
			return True
		return False
	def isValidRightMove(self,piece):
		if len(piece)>0:
			xMax = max([item[0] for item in piece])
			xMaxes = [item for item in piece if item[0]==xMax]
			for item in self.pieces:
				if item!=self.currentPiece and item!=piece:
					for item2 in xMaxes:
						if item2 in item.coords:
							return False
			return True
		return False
	def isValidRotation(self,piece):
		for coord in piece:
			for p in self.pieces:
				if p != self.currentPiece and p!=piece:
					if coord in p.coords:
						return False
		return True
	def checkValidGravity(self,piece):
		for p in self.pieces:
			if p != piece:
				for coord in piece.getMoveDownCoords():
					if coord in p.coords: 
						return False
		return True
	def isOnBottom(self,piece):
		c = piece.getMoveDownCoords()
		if len(piece.coords)>0:
			if max([item[1] for item in piece.coords])==19:
				return True
		return False
				
	def gravityCallback(self):
		try:
			self.checkRow()
			if self.currentPiece!=None:
				if self.isOnBottom(self.currentPiece) and not self.flashing:
					self.generatePiece()
				elif self.checkValidGravity(self.currentPiece) and not self.flashing:
					self.currentPiece.moveDown()
					self.refresh()
				elif not self.flashing:
					self.generatePiece()
			self.timer = Timer(.5,self.gravityCallback)
			self.timer.start()
		except Exception,e:
			if debug:
				f.write(traceback.format_exc())
				f.flush()
	def getUpAndSlam(self): #Slam function
		self.timer.cancel()
		while not self.isOnBottom(self.currentPiece) and self.checkValidGravity(self.currentPiece):
			self.currentPiece.moveDown()
			self.refresh()
		self.gravityCallback()
		self.refresh()
		return False
	def lose(self):
		self.active=False
	def downFast(self):
		if self.currentPiece != None:
			if not self.isOnBottom(self.currentPiece) and self.checkValidGravity(self.currentPiece):
				self.currentPiece.moveDown()	
				self.refresh()
	def checkRow(self):
			rows = {}
			for piece in self.pieces:
				c = sorted(piece.coords, key=lambda x:x[1])
				for item in c:
					if item[1] not in rows:
						rows[item[1]]=[]
					rows[item[1]].append(item[0])
			for item in rows:
				rows[item].sort()
				if rows[item]==range(10):
					if item not in self.flashRows:
						self.flashing = True
						self.flashRows.append(item)
			#TODO: add white flash on removal
			self.refresh()
	def removeRow(self,row):
		for piece in self.pieces:
			for i in range(10):
				if (i,row) in piece.coords:
					piece.coords.remove((i,row))
					if len(piece.coords)==0:
						self.pieces.remove(piece)
		for i in range(len(self.pieces)):
			for j in range(len(self.pieces[i].coords)):
				if self.pieces[i].coords[j][1]<=row:
					self.pieces[i].coords[j] = (self.pieces[i].coords[j][0],self.pieces[i].coords[j][1]+1)
	def canSpawn(self,piece):
		for item in self.pieces:
			for coord in item.coords:
				for c in piece.coords:
					if c==coord:
						return False
		return True
try:		
	g = Game()
	g.run()
except Exception, e:
	if debug:
		f.write(traceback.format_exc())
		f.flush()
finally:
	window.keypad(0)
	window.scrollok(0)
	curses.echo()
	curses.nocbreak()
	screen.keypad(0)
	curses.curs_set(1)
	del window
	del screen
	curses.endwin()