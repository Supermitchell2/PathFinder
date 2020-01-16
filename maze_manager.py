from vector import Vector
from numpy import array, full, concatenate
from random import randint
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
		# The strings to be printed for each grid tile
		self.UNVISITED 		= "  "
		self.VISITED		= "::"
		self.WALL		= ANSIColorPrinter.add_color("  ", "white", highlight = True)
		self.PASSAGE		= "  "
		self.END		= ANSIColorPrinter.add_color("  ", "green", highlight = True)
		self.UNDEFINED		= ANSIColorPrinter.add_color("  ", "white", highlight = True)
		self.maze = array([	[self.UNDEFINED, 	self.UNDEFINED, 	self.UNDEFINED],
					[self.UNDEFINED,	self.VISITED,		self.UNDEFINED],
					[self.UNDEFINED,	self.UNDEFINED, 	self.UNDEFINED],])
		self.maze_height = 3
		self.maze_width = 3
		self.offset = Vector(1, 1)
		self.position = Vector(0, 0)
		self.wall_probability = 0.2
		self.grid_pos = Vector(0, 0)

		'''self.expand_maze(Vector(0, 1))
		self.expand_maze(Vector(1, 0))
		self.expand_maze(Vector(0, -1))
		self.expand_maze(Vector(-1, 0))'''

	# Converts a maze coordinate into a grid coordinate
	def get_grid_coord(self, pos_vector):
			return_vector = pos_vector.multiply_vectors(Vector(2, -2)).add_vector(self.offset)
			#print(f"{pos_vector} --> {return_vector}")
			return return_vector

	# Moves the robot in the direction of the direction vector
	def move_robot(self, dir_vector):
		print("Moving in direction: " + str(dir_vector))
		print("offset: " + str(self.offset))
		self.position = self.position.add_vector(dir_vector)
		# THIS SECTION NEEDS TO DEFINE A WAY TO EXPAND MAZE WITHOUT GRID COORDS
		# Calling method to define grid coordinate before the maze has been offset
		self.grid_pos = self.get_grid_coord(self.position)
		if 	(self.grid_pos.y > self.maze_height - 1 or self.grid_pos.y < 0 or
			self.grid_pos.x > self.maze_width - 1 or self.grid_pos.x < 0):
			self.expand_maze(dir_vector)
			self.grid_pos = self.get_grid_coord(self.position)
		self.maze[self.grid_pos.y, self.grid_pos.x] = self.VISITED
		self.generate_surroundings()

	# Generates the surrounding walls/passages. Must have had move_robot(...) called prior.
	def generate_surroundings(self):
		dir_vectors = [Vector(0, 1), Vector(1, 0), Vector(0, -1), Vector(-1, 0)]
		self.grid_pos = self.get_grid_coord(self.position)
		for dir_vector in dir_vectors:
			if self.maze[self.grid_pos.y, self.grid_pos.x] == self.UNDEFINED:
				if randint(0, 100) < self.wall_probability: # If the generator chooses wall
					self.maze[self.grid_pos.y, self.grid_pos.x] = self.WALL
				else:
					self.maze[self.grid_pos.y, self.grid_pos.x] = self.PASSAGE
					self.grid_pos = self.grid_pos.add_vector(dir_vector)
					self.maze[self.grid_pos.y, self.grid_pos.x] = self.UNVISITED

	# Expands the maze in the direction of dir_vector
	def expand_maze(self, dir_vector):
		if dir_vector.x == 0:
			self.maze_height += 2
			if dir_vector.y > 0: 	# North
				self.maze = concatenate((full([2, self.maze_width], self.UNDEFINED), self.maze), axis=0)
				self.offset = self.offset.add_vector(Vector(0, 2))
				print("offset: " + str(self.offset))
			else:			# South
				self.maze = concatenate((self.maze, full([2, self.maze_width], self.UNDEFINED)), axis=0)
		else:
			self.maze_width += 2
			if dir_vector.x > 0: 	# East
				self.maze = concatenate((self.maze, full([self.maze_height, 2], self.UNDEFINED)), axis=1)
			else:			# West
				self.offset = self.offset.add_vector(Vector(2, 0))
				print("offset: " + str(self.offset))
				self.maze = concatenate((full([self.maze_height, 2], self.UNDEFINED), self.maze), axis=1)

	def print_maze(self):
		for row in self.maze:
			for col in row:
				print(col, end="")
			print()
