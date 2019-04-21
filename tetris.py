import random, copy, time

class Piece:
	""" represented by array of arbitrary size indicating 
	what sqaures from a base square that is assumed to be bottom left are filled
	ie the 'line' piece when vertical would be:
	{[0, 0] ... [0, 4]}"""

	def __init__(self, rotations):
		self.rotations = rotations

	def getRotations(self):
		return self.rotations

	@staticmethod
	def findXOffset(rot):
		return max([tup[0] for tup in rot])

	@staticmethod
	def findYOffset(rot):
		return max([tup[1] for tup in rot])

	def toStringHelper(self, rot):
		grid = [
				[" ", " ", " ", " "],
				[" ", " ", " ", " "],
				[" ", " ", " ", " "],
				[" ", " ", " ", " "]
			   ]
		print (self.rotations[rot])
		for i, j in self.rotations[rot]:
			grid[i][j] = "#"

		return "\n".join(["".join(i) for i in grid if "#" in i]) 


	def __str__(self):
		return "\n \n".join([self.toStringHelper(i) for i in range(len(self.rotations))])


class PieceFactory:
	def __init__(self, bagLen = 1):
		self.bagLen = 1
		self.queuedPieces = []
		self.possPieces = [Piece(value) for key, value in PieceFactory.getPiecesDict().iteritems()]


	@staticmethod
	def getPiecesDict():
		return {
			'line'  :   [[(0, 0), (0, 1), (0, 2), (0, 3)],
						[(0, 0), (1, 0), (2, 0), (3, 0)]],

			'square':   [[(0, 0), (0, 1), (1, 0), (1, 1)]],

			'l-1'   :   [[(0, 0), (0, 1), (0, 2), (1, 2)],
						[(0, 0), (1, 0), (0, 1), (2, 0)], 
						[(0, 0), (1, 0), (1, 1), (1, 2)],
						[(0, 1), (1, 1), (2, 1), (2, 0)]],

			't'     :   [[(1, 0), (0, 1), (1, 1), (1, 2)],
						[(0, 0), (0, 1), (0, 2), (1, 1)],
						[(0, 0), (1, 0), (2, 0), (1, 1)],
						[(0, 1), (1, 1), (1, 0), (2, 1)]],

			'dog-1' :   [[(0, 0), (0, 1), (1, 1), (1, 2)],
						[(1, 0), (2, 0), (1, 1), (0, 1)]],

			'dog-2' :   [[(0,2),(0,1),(1,1),(1,0)],
						[(0,0),(1,0),(1,1),(2, 1)]],

			'l-2'   :   [[(0,0),(0,1),(0,2),(1,0)],
						[(0,0),(0,1),(1,1),(2,1)],
						[(0,2),(1,0),(1,1),(1,2)],
						[(0,0),(1,0),(2,0),(2,1)]]

		}

	def nextPiece(self):
		if self.queuedPieces:
			return self.queuedPieces.pop()

		else:
			random.shuffle(self.possPieces)
			self.queuedPieces = list(self.possPieces)
			return self.queuedPieces.pop()


class State:
	#board object stripped of methods, used to pass between
	#eval and test functions
	def __init__(self, w, h):
		self.pf = self.pf = [[0 for i in range(w)] for j in range(h)]
		self.w = w
		self.h = h

	def printState(self):
		h = [" ", "#", "@"]
		for row in self.pf:
			temp = ""
			for ele in row:
				temp += h[ele]
			print ("|" + temp + "|")
		print ("~"*(self.w + 2))


	def fill(self, pts):
		for x, y in pts:
			self.pf[y][x] = 1
		self.clearRows()
		return self

	def clearRows(self):
		count = 0
		for i, row in enumerate(self.pf):
			if State.isClearable(row):
				count += 1
				self.pf.remove(row)
				
				self.pf = [[0 for i in range(self.w)]] + self.pf

	@staticmethod
	def isClearable(row):
		return True if not [i for i in row if i != 1] else False


