class Vector(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return f"({self.x}, {self.y})"

	# Returns the sum of the current vector and the argument vector
	def add_vector(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	# Multiplies a vector by the value
	def multiply_vector(self, value):
		return Vector(self.x * value, self.y * value)

	# Multiplies a vector by a value component-wise
	def multiply_vectors(self, other):
		return Vector(self.x * other.x, self.y * other.y)

	# Gets the vector 180 degrees in opposition to the current vector
	def get_inverse(self):
		return Vector(-self.x, -self.y)

	def abs(self):
		self.x = abs(self.x)
		self.y = abs(self.y)
		return self
