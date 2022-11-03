import curses, time
from random import randint
from enum import Enum, auto

class HorizontalAlignment(Enum):
	LEFT = auto()
	CENTER = auto()
	RIGHT = auto()

class VerticalAlignment(Enum):
	TOP = auto()
	CENTER = auto()
	BOTTOM = auto()

class Snake:
	def __init__(
		self, stdscr, initial_length
	):
		self.cells = [
			(
				(
					stdscr.getmaxyx()[
						0
					]
					// 2
				)
				+ x,
				stdscr.getmaxyx()[1]
				// 2,
			)
			for x in range(
				initial_length
			)
		]
		self.direction = (0, 0)

def addstr_multiline_aligned(
	stdscr,
	strings,
	horizontal_alignment=HorizontalAlignment.LEFT,
	vertical_alignment=VerticalAlignment.TOP,
):
	y = vertically_align_text(
		stdscr,
		strings,
		vertical_alignment,
	)
	for string in strings:
		lines = string.split("\n")
		x = horizontally_align_text(
			stdscr,
			string,
			horizontal_alignment,
		)
		for line in lines:
			stdscr.addstr(
				y, x, line
			)
			y += 1

# Calculates column the text should 
# start at (i.e. the argument x for the
# addstr method) when aligned using the
# given alignment
def horizontally_align_text(
	stdscr, string, alignment
):
	window_width = (
		stdscr.getmaxyx()[1]
	)
	window_left = stdscr.getbegyx()[
		1
	]

	# The input text may contain multiple lines
	# The overall width of the text is the length of the longest line
	lines = string.split("\n")
	text_width = max(
		map(len, lines)
	)

	if (
		alignment
		== HorizontalAlignment.RIGHT
	):
		window_right = (
			window_left
			+ window_width
			- 1
		)
		text_left = (
			window_right
			- text_width
			+ 1
		)
	elif (
		alignment
		== HorizontalAlignment.CENTER
	):
		text_left = center(
			text_width,
			window_left,
			window_width,
		)
	else:
		text_left = 0

	return text_left

# Calculates line the text should start at (i.e. the argument y for the addstr method) when aligned using the given
# alignment
def vertically_align_text(
	stdscr, strings, alignment
):
	window_height = (
		stdscr.getmaxyx()[0]
	)
	window_top = stdscr.getbegyx()[
		0
	]

	# The input text may contain multiple lines
	# The overall height of the text is the number of lines in each string summed up
	text_height = sum(
		map(
			lambda string: len(
				string.split("\n")
			),
			strings,
		)
	)

	if (
		alignment
		== VerticalAlignment.BOTTOM
	):
		window_right = (
			window_top
			+ window_height
			- 1
		)
		text_top = (
			window_right
			- text_height
			+ 1
		)
	elif (
		alignment
		== VerticalAlignment.CENTER
	):
		text_top = center(
			text_height,
			window_top,
			window_height,
		)
	else:
		text_top = 0

	return text_top

def center(
	text_size,
	window_min,
	window_size,
):
	return (
		window_min
		+ ((window_size - 1) // 2)
		- (text_size // 2)
	)

def curses_main(stdscr):
	# Initialise colours
	curses.init_pair(
		1,
		curses.COLOR_CYAN,
		curses.COLOR_BLACK,
	)
	curses.init_pair(
		2,
		curses.COLOR_YELLOW,
		curses.COLOR_BLACK,
	)

	# Show cursor
	curses.curs_set(1)

	settings = {
		"snake_wrapping": {
			"name": "Snake wraps around screen edge",
			"key": "b",
			"value": False
		},
		"missions" : [
			" abcdefghij",
			" abcdefghijklmnopqrstuvwxyz", 
			" bit-of-a-test-for-fun4-this one will-go-on-for-a-bit-longer4"
		]
	}
	mission = 0

	show_title_screen(
		stdscr, settings
	)
	show_mission_screen(
		stdscr, settings, mission
	)

	# Hide cursor
	curses.curs_set(1)

	score = show_game_screen(
		stdscr, settings, mission
	)

	# Show cursor
	curses.curs_set(1)

	show_game_over_screen(
		stdscr, score
	)

def next_mission(
	stdscr, 
	settings, 
	mission
):
	time.sleep(4)
	mission = mission+1

	show_mission_screen(
		stdscr, settings, mission
	)

	score = show_game_screen(
		stdscr, settings, mission
	)

	# Show cursor
	curses.curs_set(1)

	show_game_over_screen(
		stdscr, score
	)

def show_title_screen(
	stdscr, settings
):
	finished = False
	while not finished:
		stdscr.clear()

		addstr_multiline_aligned(
			stdscr,
			[
				"Snake, by Ruben Dougall.",
				"Adapted for Canute 360 by Ed Rogers.",
				"Move the snake/= by tapping:",
				"left, right, up, down.",
				"Avoid the snake's tail/1 and the edges",
				"whilst completing the missions.",
				"Press Q to end the game",
				"Press any key to start..."
			],
			HorizontalAlignment.CENTER,
			VerticalAlignment.CENTER,
		)

		stdscr.move(0, 0)
		stdscr.refresh()

		key = stdscr.getch()
		finished = True

def show_mission_screen(
	stdscr, settings, mission
):
	finished = False
	while not finished:
		stdscr.clear()

		addstr_multiline_aligned(
			stdscr,
			[
				"You have a new mission:",
				"Eat all these letters, in order,",
				"to move on to the next mission:",
				"",
				settings["missions"][mission][:39],
				"",
				"Press any key to start...",
			],
			HorizontalAlignment.CENTER,
			VerticalAlignment.CENTER,
		)

		stdscr.move(0, 0)
		stdscr.refresh()

		key = stdscr.getch()
		finished = True

def show_game_screen(
	stdscr, settings, mission
):
	snake = Snake(stdscr, 1)
	pellet = (
		randint(
			2,
			stdscr.getmaxyx()[0]
			- 2,
		),
		randint(
			1,
			stdscr.getmaxyx()[1]
			- 1,
		),
	)

	key = None
	# getch return value of 27 corresponds to escape key - doesn't look like curses has a constant for this
	# 3rd condition checks if snake has "eaten" (intersected with) itself, i.e. whether any cells re-appear in the list
	while (
		key != 27
		and key != ord("q")
		and len(snake.cells)
		== len(set(snake.cells))
	):
		# Update
		(
			game_over,
			pellet
		) = update_game_screen(
			stdscr,
			key,
			snake,
			pellet,
			settings
		)
		if game_over:
			break

		if len(settings["missions"][mission]) == len(snake.cells):
			next_mission(
				stdscr, 
				settings, 
				mission
			)

		# Draw
		draw_game_screen(
			stdscr, snake, pellet, settings["missions"][mission]
		)

		# Set the maximum amount of time to block for a key press
		# This is effectively the update interval
		stdscr.timeout(10000)
		key = (
			stdscr.getch()
		)  # TODO: Do this last to prevent waiting before drawing game screen

	# For user input, remove the timeout but keep blocking enabled
	stdscr.nodelay(False)

	# Return score
	return len(snake.cells)-1

def update_game_screen(
	stdscr,
	key,
	snake,
	pellet,
	settings
):
	# Set new direction based on the key input
	# If an arrow key wasn't pressed then continue in same direction
	if key == curses.KEY_LEFT:
		new_direction = (0, -1)
	elif key == curses.KEY_RIGHT:
		new_direction = (0, 1)
	elif key == curses.KEY_UP:
		new_direction = (-1, 0)
	elif key == curses.KEY_DOWN:
		new_direction = (1, 0)
	else:
		new_direction = (
			snake.direction
		)

	# Prevent the snake reversing on itself, i.e. check that the snake's current and new directions aren't the reverse
	# of one another
	new_direction_reversed = (
		-new_direction[0],
		-new_direction[1],
	)
	if (
		snake.direction
		!= new_direction_reversed
	):
		snake.direction = (
			new_direction
		)

	#
	current_front = snake.cells[0]
	new_front = (
		current_front[0]
		+ snake.direction[0],
		current_front[1]
		+ snake.direction[1],
	)
	if not settings[
		"snake_wrapping"
	]["value"] and (
		new_front[0] < 0
		or new_front[0]
		>= stdscr.getmaxyx()[0]
		or new_front[1] < 0
		or new_front[1]
		>= stdscr.getmaxyx()[1]
	):
		return True, pellet
	new_front = (
		new_front[0]
		% stdscr.getmaxyx()[0],
		new_front[1]
		% stdscr.getmaxyx()[1],
	)
	snake.cells.insert(0, new_front)

	# If the snake just "ate" (intersected with) a pellet:
	# * Effectively increase the length by 1, by not removing a cell to compensate for the one just added
	# * Move the pellet to a random position
	# If the snake didn't just "eat" a pellet:
	# * Remove a cell to compensate for the one just added, so length of the snake stays the same
	# * Obviously leave the pellet where it is
	if pellet in snake.cells:
		pellet = (
			randint(
				2,
				stdscr.getmaxyx()[0]
				- 4,
			),
			randint(
				2,
				stdscr.getmaxyx()[1]
				- 4,
			),
		)
	else:
		snake.cells.pop()

	return False, pellet

def draw_game_screen(
	stdscr, snake, pellet, mission
):
	stdscr.clear()

	mission_progress = mission[0:len(snake.cells)]

	# Display score
	stdscr.addstr(
		0,
		0,
		f"  Score {len(snake.cells)-1}/{len(mission)}: {mission_progress[-10:]}",
	)

	# Draw pellet
	if curses.has_colors():
		stdscr.attron(
			curses.color_pair(2)
		)

	try:
		stdscr.addch(
			pellet[0],
			pellet[1],
			mission[len(snake.cells)],
		)
	except curses.error as e:  # Ignore error when writing to bottom-right corner of window
		pass

	if curses.has_colors():
		stdscr.attroff(
			curses.color_pair(2)
		)

	# Draw snake
	for cell in snake.cells:

		if cell == snake.cells[0]:
			snake_head = "="
		else:
			snake_head = "1"

		if curses.has_colors():
			stdscr.attron(
				curses.color_pair(1)
			)

		try:
			stdscr.addch(
				cell[0],
				cell[1],
				snake_head,
			)
		except curses.error as e:  # Ignore error when writing to bottom-right corner of window
			pass

		if curses.has_colors():
			stdscr.attroff(
				curses.color_pair(1)
			)

		stdscr.move(0, 0)
		stdscr.refresh()

def show_game_over_screen(
	stdscr, score
):
	stdscr.addstr(
		0,
		0,
		f"  Final score: {score}                                    "[-38:],
	)
	addstr_multiline_aligned(
		stdscr,
		[
			" Game over! Press any key to exit... ",
		],
		HorizontalAlignment.CENTER,
		VerticalAlignment.CENTER,
	)
	stdscr.getch()
	time.sleep(4)

def main():
	curses.wrapper(curses_main)

if __name__ == "__main__":
	main()
