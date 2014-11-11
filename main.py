import curses
import tetris
from threading import Timer
from time import sleep
from sys import exit
import traceback
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
height,width = panel.getmaxyx()

#Color codes are associated with piece codes + 1
curses.init_pair(1,curses.COLOR_RED, curses.COLOR_RED)
curses.init_pair(2,curses.COLOR_MAGENTA,curses.COLOR_MAGENTA)
curses.init_pair(3,curses.COLOR_BLUE,curses.COLOR_BLUE)
curses.init_pair(4,curses.COLOR_YELLOW,curses.COLOR_YELLOW)
curses.init_pair(5,curses.COLOR_GREEN,curses.COLOR_GREEN)
curses.init_pair(6,curses.COLOR_CYAN,curses.COLOR_CYAN)
curses.init_pair(7,curses.COLOR_WHITE,curses.COLOR_WHITE)
curses.init_pair(8,curses.COLOR_BLACK,curses.COLOR_BLACK)
window.bkgd(curses.color_pair(7))
panel.bkgd(curses.color_pair(8))
class Game():
	def __init__(self):
		self.pieces = []
		self.currentPiece = None
		self.timer = Timer(.5 ,self.gravityCallback)
	def run(self):
		self.generatePiece()
		self.timer.start()
		try:
			while True:
				panel.clear()
				for piece in self.pieces:
					drawableCoords = piece.getDrawableCoords()
					for item in drawableCoords:
						if item[0] < width and item[0] >=0 and item[1] < height and item[1] >= 0:
							panel.move(item[1],item[0])
							try:
								panel.addstr(" ",curses.color_pair(piece.piece+1))
							except curses.error:
								pass
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
			print str(e)
			self.timer.cancel()
			return
	def refresh(self):
		# return False
		screen.noutrefresh()
		window.noutrefresh()
		panel.noutrefresh(0,0,0,0,height,width)
		curses.doupdate()
	def generatePiece(self):
		p = tetris.Piece()
		self.pieces.append(p)
		self.currentPiece = p
	def isValidLeftMove(self,piece):
		xMin = min([item[0] for item in piece])
		xMins = [item for item in piece if item[0]==xMin]
		for item in self.pieces:
			if item!=self.currentPiece and item!=piece:
				for item2 in xMins:
					if item2 in item.coords:
						return False
		return True
	def isValidRightMove(self,piece):
		xMax = max([item[0] for item in piece])
		xMaxes = [item for item in piece if item[0]==xMax]
		for item in self.pieces:
			if item!=self.currentPiece and item!=piece:
				for item2 in xMaxes:
					if item2 in item.coords:
						return False
		return True
	def isValidRotation(self,piece):
		for coord in piece:
			for p in self.pieces:
				if p != self.currentPiece and p!=piece:
					if coord in p.coords:
						return False
		return True
	def checkValidGravity(self):
		for piece in self.pieces:
			if piece != self.currentPiece:
				for coord in self.currentPiece.getMoveDownCoords():
					if coord in piece.coords: 
						return False
		return True
	def isOnBottom(self,piece):
		c = piece.getMoveDownCoords()
		if max([item[1] for item in piece.coords])==19:
			return True
		return False
				
	def gravityCallback(self):
		if self.currentPiece!=None:
			if self.isOnBottom(self.currentPiece):
				self.generatePiece()
			elif self.checkValidGravity():
				self.currentPiece.moveDown()
				self.refresh()
			else:
				self.generatePiece()
		self.timer = Timer(.5,self.gravityCallback)
		self.timer.start()
	def getUpAndSlam(self): #Slam function
		while not self.isOnBottom(self.currentPiece) and self.checkValidGravity():
			self.currentPiece.moveDown()
		self.generatePiece()
		self.refresh()
		return False
	def downFast(self):
		if self.currentPiece != None:
			if not self.isOnBottom(self.currentPiece) and self.checkValidGravity():
				self.currentPiece.moveDown()	
				self.refresh()
			
g = Game()
g.run()
curses.nocbreak()
screen.keypad(0)
window.keypad(0)
curses.curs_set(1)
curses.echo()
curses.endwin()