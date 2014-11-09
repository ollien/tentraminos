import curses
import tetris

# print tetris.Piece(6).coords

#init curses
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
curses.curs_set(0)
screen.keypad(1)

window = curses.newwin(25,80,0,0)
window.keypad(1)
panel = curses.newpad(22,10)
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

piece = 1
t = tetris.Piece(piece)
while True:
	panel.clear()
	for i in range(height):
		for j in range(width):
			for item in t.coords:
				if item[0] == j and item[1] == i:
					panel.move(i,j)
					panel.addstr(" ",curses.color_pair(piece+1))
	screen.refresh()
	window.refresh()
	panel.refresh(0,0,0,0,height,width)
	c = window.getch()
	if c==ord('s'):
		if piece < 6:
			piece+=1
		else:
			piece = 0
		t = tetris.Piece(piece)
	elif c==ord('q'):
		t.rotateLeft()
	elif c==ord('e'):
		t.rotateRight()
	elif c==ord('a'):
		t.moveLeft()
	elif c==ord('d'):
		t.moveRight()
curses.nocbreak()
curses.keypad()
curses.curs_set(1)
curses.echo()
curses.endwin()