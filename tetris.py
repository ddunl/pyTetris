import random
import copy


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
			print ("|" + temp + "|")


		print ("~"*(self.w + 2))
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
		#make pieces based on dict
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
	def __init__(self, board):
		self.pf = board.pf
		self.w = board.w
		self.h = board.h

	def printState(self):
		h = [" ", "#", "@"]
		for row in self.pf:
			temp = ""
			for ele in row:
				temp += h[ele]
			print ("|" + temp + "|")
		print ("~"*(self.w + 2))
		print 


	def fill(self, pts):
		for x, y in pts:
			self.pf[y][x] = 1
		self.clearRows()
		return self

	def clearRows(self):
		for i, row in enumerate(self.pf):
			if State.isClearable(row):
				self.pf.remove(row)
				
				self.pf = [[0 for i in range(self.w)]] + self.pf

	@staticmethod
	def isClearable(row):
		return True if not [i for i in row if i != 1] else False

	""" Find the y location of highest piece for evaluation """

	def highestPiece(self):
		for i in range(self.h):
			for j in range(self.w):
				if (self.pf[i][j]==1):
					return (self.h-i)
		return 0

 

	""" Counts the caves in the current state """

	def hermit(self):
		count = 0
		for i in range(self.h):
			for j in range(self.w):
				if (self.pf[i][j]==0):
					#look above if above has piece then add to cave count
					for k in range(i):
						if (self.pf[k][j]==1):
							count = count + 1
		return count

	def eval(self):
		score = (2*self.hermit()) + self.highestPiece()
		return score


def evaluate(state):
	score = 0
	score = state.hermit() + state.highestPiece()
	return score



def test(state, rot, xval):
	"""
	takes state, a specific rotation of a piece,
	xvalue for key pixel
	returns a state with the piece hard dropped
	(or false in the case that the piece can't be placed)
	"""

	depth = 0

	max_x = Piece.findXOffset(rot)
	if xval > max_x: # if x invalid, test fails
		#return False
		pass

	if not getPixels(state.pf, xval, 0, rot):
		return False
	else:
		lastValidPlacement = getPixels(state.pf, xval, 0, rot)

	for yval in range(0, state.h - Piece.findYOffset(rot) + 1):
		t = getPixels(state.pf, xval, yval, rot)
		
		if t:
			lastValidPlacement = t
		else:
			return lastValidPlacement

	return lastValidPlacement
		


def getPixels(twoDimArr, row, col, pointsToCheck):
	#makes sure rot can be placed at certain key pixel,
	#if so, returns the pixels it would occupy, else False

	points = []
	for x, y in pointsToCheck:
		try: 
			if twoDimArr[col + y][row + x]:
				return False
			else:
				points.append((row + x, col + y))

			
		except IndexError: 
			return False

	return points


def test_all_x(state, rot):
	low_score = 1000
	idx = 0
	max_x = state.w-Piece.findXOffset(rot)
	#pure_state = copy.deepcopy(state)
	for i in range(max_x):
		temp_state = copy.deepcopy(state)
		in_for_score = temp_state.fill(test(temp_state,rot,i)).eval()
		if(in_for_score<low_score):
			low_score=in_for_score
			idx = i
	outstate = state.fill(test(state, rot, idx))
	return outstate

def test_all_rot_and_x(state,Piece):
	loop_len = len(Piece.getRotations())
	low_score=1000
	idx = 0
	for i in range(loop_len):
		rot_piece = Piece.getRotations()[i]
		temp_state = copy.deepcopy(state)
		inner_score = test_all_x(temp_state,rot_piece).eval()
		if (inner_score<low_score):
			low_score = inner_score
			idx = i 
	outstate = test_all_x(state,Piece.getRotations()[idx])
	return outstate


b = Board(20, 10)

factory = PieceFactory()
p = Piece(PieceFactory.getPiecesDict()["l-2"])
s = State(b)

print("TESTING...Test_all_x-and_all_rot")

for i in range(1000):
	print ("Turn", i + 1)
	s = test_all_rot_and_x(s,factory.nextPiece())
	s.printState()



'''
rot = p.getRotations()[1]
print("Figure out rotations possible")
print(len(p.getRotations()))





s = test_all_x(s,rot)
s = test_all_x(s,rot)
s.printState()
'''


'''
#state_two = copy.deepcopy(s)

#state_two.fill(test(state_two, rot, 0))
#s = test_all_x(s, rot)

#state_two.printState()

testing = s.w-Piece.findXOffset(rot)
print("testing x offset")
print(testing)


print("tesing method after fill")
print(s.fill(test(s, rot, 0)).eval())

s.fill(test(s, rot, 0))

value = evaluate(s)

print(value)
print("Calc using Methods")
print(s.eval())

s.printState()
'''