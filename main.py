import curses
import tetris

#init curses
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
curses.curs_set(0)
screen.keypad(1)

window = curses.newwin(25,80,0,0)
window.keypad(1)
panel = curses.newpad(22,20)
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
pieces = []
currentPiece = None
p = tetris.Piece()
pieces.append(p)
currentPiece = p
while True:
	panel.clear()
	for piece in pieces:
		drawableCoords = piece.getDrawableCoords()
		for item in drawableCoords:
			if item[0] < width and item[0] >=0 and item[1] < height and item[1] >= 0:
				panel.move(item[1],item[0])
				panel.addstr(" ",curses.color_pair(piece.piece+1))
	screen.refresh()
	window.refresh()
	panel.refresh(0,0,0,0,height,width)
	c = window.getch()
	if c==ord('q'):
		currentPiece.rotateLeft()
	elif c==ord('e'):
		currentPiece.rotateRight()
	elif c==ord('a'):
		currentPiece.moveLeft()
	elif c==ord('d'):
		currentPiece.moveRight()
curses.nocbreak()
curses.keypad()
curses.curs_set(1)
curses.echo()
curses.endwin()