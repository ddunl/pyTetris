from tetris import *
from heuristics import *
import sys



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
		


def getAllStates(state, piece):
    allstates=[]

    for rot in piece.getRotations():
        for xval in range(state.w-piece.findXOffset(rot)):

            free_state = state.copy()
            if test(free_state,rot,xval):
            	allstates.append(free_state.fill(test(free_state,rot,xval)))

    return allstates


def lookahead(stateList, piece, evaluator):
	best = None
	bestScore = None
	for state in stateList:
		fStateList = getAllStates(state, piece)
		for fState in fStateList:
			
			if best is None or evaluator.evaluate(fState) < bestScore:
				best = state
				bestScore = evaluator.evaluate(fState)

	return best







# factory = PieceFactory()

# s = State(10, 24)

# judge = Evaluator([aggHeight, highestPiece, contig, hermit], [3, 5, 2, .5])
# for i in range(20000):
# 	s = lookahead(getAllStates(s, factory.nextPiece()), factory.peekPiece(), judge)

# 	s.printState()
# 	print i

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print "Takes BoardWidth, BoardHeight, \n aggHeight(rec: 3), highestPiece(rec : 5), contig(rec : 2), hermit(rec : .5) \n pieceAmount, \n lookAhead? (1/0)"
		sys.exit()


	f = PieceFactory()
	bw = int(sys.argv[1])
	bh = int(sys.argv[2])

	s = State(bw, bh)

	hWeights = [float(arg) for arg in sys.argv[3:7]]

	e = Evaluator([aggHeight, highestPiece, contig, hermit], hWeights)

	pieceAmount = int(sys.argv[7])

	if int(sys.argv[8]):
		for i in range(pieceAmount):
			s = lookahead(getAllStates(s, f.nextPiece()), f.peekPiece(), e)
			s.printState()
			print i + 1

	else:
		for i in range(pieceAmount):
			s = e.choose(getAllStates(s, f.nextPiece()))
			s.printState()
			print i + 1




