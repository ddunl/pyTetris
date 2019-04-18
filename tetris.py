import random

class Board:
	def __init__ (self, h, w):
		self.h = h
		self.w = w
		self.pf = [[0 for i in range(w)] for j in range(h)]

	def clearRows(self):
		for i, row in enumerate(self.pf):
			if Board.isClearable(row):
				self.pf.remove(row)
				
				self.pf = [[0 for i in range(self.w)]] + self.pf
				


	#checks if row is all solid blocks
	@staticmethod
	def isClearable(row):
		return True if not [i for i in row if i != 1] else False

	def printBoard(self):
		h = [" ", "#", "@"]
		for row in self.pf:
			temp = ""
			for ele in row:
				temp += h[ele]
			print "|" + temp + "|"


		print "~"*(self.w + 2)
		print 
		

		


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
	def findOffset(listp):
		return max([tup[0] for tup in listp])


	def toStringHelper(self, rot):
		grid = [
				[" ", " ", " ", " "],
				[" ", " ", " ", " "],
				[" ", " ", " ", " "],
				[" ", " ", " ", " "]
			   ]
		print self.rotations[rot]
		for i, j in self.rotations[rot]:
			grid[i][j] = "#"

		return "\n".join(["".join(i) for i in grid if "#" in i]) 


	def __str__(self):
		return "\n \n".join([self.toStringHelper(i) for i in range(len(self.rotations))])



class PieceFactory:
	def __init__(self, bagLen = 1):
		self.bagLen = 1
		self.queuedPieces = []
		#make pieces based on dict
		self.possPieces = [Piece(value) for key, value in self.getPiecesDict()]


	@staticmethod
	def getPiecesDict():
		return {
			'line'  : 	[[(0, 0), (0, 1), (0, 2), (0, 3)],
			    		[(0, 0), (1, 0), (2, 0), (3, 0)]],

			'square':   [[(0, 0), (0, 1), (1, 0), (1, 1)]],

			'l-1'	:	[[(0, 0), (0, 1), (0, 2), (1, 2)],
						[(0, 0), (1, 0), (0, 1), (2, 0)], 
						[(0, 0), (1, 0), (1, 1), (1, 2)],
						[(0, 1), (1, 1), (2, 1), (2, 0)]],

			't'     :	[[(1, 0), (0, 1), (1, 1), (1, 2)],
						[(0, 0), (0, 1), (0, 2), (1, 1)],
						[(0, 0), (1, 0), (2, 0), (1, 1)],
						[(0, 1), (1, 1), (1, 0), (2, 1)]],

			'dog-1'	:	[[(0, 0), (0, 1), (1, 1), (1, 2)],
						[(1, 0), (2, 0), (1, 1), (0, 1)]],

			'dog-2' :   [[(0,2),(0,1),(1,1),(1,0)],
						[(0,0),(1,0),(1,1),(2, 1)]],

			'l-2'	:	[[(0,0),(0,1),(0,2),(1,0)],
						[(0,0),(0,1),(1,1),(2,1)],
						[(0,2),(1,0),(1,1),(1,2)],
						[(0,0),(1,0),(2,0),(2,1)]]

		}

	def nextPiece(self):
		if self.queuedPieces:
			return self.queuedPieces.pop()

		else:
			self.queuedPieces = random.shuffle(list(self.possPieces))
			return self.queuedPieces.pop()




b = Board(20, 10)

b.pf[2] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]



p = Piece(PieceFactory.getPiecesDict()["dog-2"])

print p 






