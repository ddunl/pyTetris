class Board:
	def __init__ (self, h, w):
		self.h = h
		self.w = w
		self.pf = [[0 for i in range(w)] for j in range(h)]

	def clearRows(self):
		for i, row in enumerate(self.pf):
			if self.isClearable(row):
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

	def getRotations(self):
		pass


	







b = Board(20, 10)

b.pf[2] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]



b.printBoard()

b.clearRows()

b.printBoard()