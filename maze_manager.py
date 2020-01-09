from vector import Vector
from numpy import array, full, concatenate
from ANSI_color_printer import ANSIColorPrinter
class MazeManager(object):
	def __init__(self):
		'''	the maze variable is a two dimensional numpy array containing
			integer values which specify the type of tile at the position
			0 --> an unvisited tile
			1 --> a visited tile
			2 --> a wall/corner
			3 --> a passage
			4 --> the end tile
			5 --> an undefined tile
		'''
		# The numbers used in the maze to optimize performance
		self.UNVISITED 	= 0
		self.VISITED 	= 1
		self.WALL 	= 2
		self.PASSAGE 	= 3
		self.END	= 4
		self.UNDEFINED 	= 5
		# The strings to be printed for each grid tile
		self.UNVISITED_DISP 	= "  "
		self.VISITED_DISP	= "::"
		self.WALL_DISP		= ANSIColorPrinter.add_color("  ", "white", highlight = True)
		self.PASSAGE_DISP	= "  "
		self.END_DISP		= ANSIColorPrinter.add_color("  ", "green", highlight = True)
		self.UNDEFINED_DISP	= "<>"
		self.maze = array([	[2, 5, 2],
					[5, 0, 5],
					[2, 5, 2],])
		self.maze_height = 3
		self.maze_width = 3
		self.position = Vector(0, 0)

	# Converts a maze coordinate into a grid coordinate
	def get_grid_coord(self, pos_vector):
		return pos_vector.multiply_vector(2)

	# Moves the robot in the direction of the direction vector
	def move_robot(self, dir_vector):
		self.position = self.position.add_vector(dir_vector)
		self.grid_pos = self.get_grid_coord(self.position)
		if grid_pos.y > self.maze_height or grid_pos.x > self.maze_width:
			self.expand_maze(dir_vector)

	# Expands the maze in the direction of dir_vector
	def expand_maze(self, dir_vector):
		if dir_vector.x == 0:
			self.maze_height += 2
			if dir_vector.y > 0: 	# North
				self.maze = concatenate((full([2, self.maze_width], self.UNDEFINED), self.maze), axis=0)
				row_val = 0
			else:			# South
				self.maze = concatenate((self.maze, full([2, self.maze_width], self.UNDEFINED)), axis=0)
				row_val = self.maze_height - 1
			# If the column is even then it requries a corner tile
			for col_val in range(0, self.maze_width):
				if col_val % 2 == 0:
					self.maze[row_val, col_val] = self.WALL
		else:
			self.maze_width += 2
			if dir_vector.x > 0: 	# East
				self.maze = concatenate((self.maze, full([self.maze_height, 2], self.UNDEFINED)), axis=1)
				col_val = self.maze_width - 1
			else:			# West
				self.maze = concatenate((full([self.maze_height, 2], self.UNDEFINED), self.maze), axis=1)
				col_val = 0
			# If the row is even then it requries a corner tile
			for row_val in range(0, self.maze_height):
				if row_val % 2 == 0:
					self.maze[row_val, col_val] = self.WALL

	def print_maze(self):
		for row in self.maze:
			for col in row:
				if col == self.UNDEFINED:
					print(self.UNDEFINED_DISP, end="")
				if col == self.UNVISITED:
					print(self.UNVISITED_DISP, end="")
				if col == self.VISITED:
					print(self.VISITED_DISP, end="")
				if col == self.WALL:
					print(self.WALL_DISP, end="")
				if col == self.PASSAGE:
					print(self.PASSAGE_DISP, end="")
			print()
