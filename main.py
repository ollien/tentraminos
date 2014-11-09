import curses
import tetris
from threading import Timer
from time import sleep
#init curses
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
curses.curs_set(0)
screen.keypad(1)
screen.nodelay(1)
window = curses.newwin(25,80,0,0)
window.nodelay(1)
window.keypad(1)
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
		self.timer = Timer(1,self.gravityCallback)
	def run(self):
		self.generatePiece()
		self.timer.start()
		while True:
			panel.clear()
			for piece in self.pieces:
				drawableCoords = piece.getDrawableCoords()
				for item in drawableCoords:
					if item[0] < width and item[0] >=0 and item[1] < height and item[1] >= 0:
						panel.move(item[1],item[0])
						panel.addstr(" ",curses.color_pair(piece.piece+1))
			self.refresh()
			c = window.getch()
			if c==ord('q'):
				self.currentPiece.rotateLeft()
			elif c==ord('e'):
				self.currentPiece.rotateRight()
			elif c==ord('a'):
				self.currentPiece.moveLeft()
			elif c==ord('d'):
				self.currentPiece.moveRight()
			sleep(1.0/60)
	def refresh(self):
		screen.refresh()
		window.refresh()
		panel.refresh(0,0,0,0,height,width)
	def generatePiece(self):
		p = tetris.Piece()
		self.pieces.append(p)
		self.currentPiece = p
	def checkValidGravity(self):
		for piece in self.pieces:
			if piece != self.currentPiece:
				for coord in self.currentPiece.getDownCoords():
					if coord in piece: 
						return False
		return True
	def gravityCallback(self):
		if self.currentPiece!=None:
			if self.checkValidGravity():
				self.currentPiece.moveDown()
				self.refresh()
		self.timer = Timer(1,self.gravityCallback)
		self.timer.start()
		
g = Game()
g.run()
curses.nocbreak()
screen.keypad(0)
window.keypad(0)
curses.curs_set(1)
curses.echo()
curses.endwin()