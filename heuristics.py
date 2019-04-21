class Evaluator:
	"""
	evaluate method takes functions and weights to produce an
	approximation of how strong a state is
	"""
	def __init__(self, funcList, cList):
		assert (len(funcList) == len(cList)), "More coefficients than functions"

		self.funcList = funcList
		self.cList = cList 

	def evaluate(self, state):
		return sum([func(state, c) for func, c in zip(self.funcList, self.cList)])
		


def hermit(state, coef):
	count = 0
	for i in range(state.h):
		for j in range(state.w):
			if (state.pf[i][j]==0):
				#look above if above has piece then add to cave count
				for k in range(i):
					if (state.pf[k][j]==1):
						count = count + 1
	return count*coef


def contig(state, coef):
	count = 0
	for i1, row in enumerate(state.pf[1:-1]):
		for i2, e in enumerate(row[1:-1]):
			if e:
				if not (state.pf[i1][i2-1] and state.pf[i1][i2+1] and state.pf[i1-1][i2] and state.pf[i1+1][i2]):
					count += 1
	return count*coef


def aggHeight(state, coef):
	agg = 0
	for i in range(state.w):
		for j in range(state.h):
			if state.pf[j][i]:
				agg += state.h - j
				break
	return agg*coef


def highestPiece(state, coef):
	for i in range(state.h):
		for j in range(state.w):
			if (state.pf[i][j] == 1):
				return (state.h - i)
	return 0




