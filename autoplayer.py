from tetris import *
from heuristics import *


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
		


def test_all_x(state, rot, evaluator):
	low_score = 1000
	in_for_score = 1000
	idx = 0
	max_x = state.w-Piece.findXOffset(rot)
	#pure_state = copy.deepcopy(state)
	for i in range(max_x):
		temp_state = copy.deepcopy(state)
		if test(temp_state,rot,i):
			in_for_score = evaluator.evaluate(temp_state.fill(test(temp_state,rot,i)))
		if(in_for_score<low_score):
			low_score=in_for_score
			idx = i
	outstate = state.fill(test(state, rot, idx))
	return outstate



def test_all_rot_and_x(state, piece, evaluator):
	loop_len = len(piece.getRotations())
	low_score=1000
	idx = 0
	for i in range(loop_len):
		rot_piece = piece.getRotations()[i]
		temp_state = copy.deepcopy(state)
		inner_score = evaluator.evaluate(test_all_x(temp_state, rot_piece, evaluator))
		if (inner_score<low_score):
			low_score = inner_score
			idx = i 
	outstate = test_all_x(state, piece.getRotations()[idx], evaluator)
	return outstate



factory = PieceFactory()

s = State(10, 24)

judge = Evaluator([aggHeight, highestPiece, contig, hermit], [3, 5, 2, .5])

for i in range(1000):
	print "Turn", i + 1
	s = test_all_rot_and_x(s, factory.nextPiece(), judge)
	s.printState()



