# pyTetris
Simple version of tetris with AI player.

Must use python 3.

Args:
  Board width: width of board
  
  Board height: height of board
  
  aggHeight: weight of aggregate height heuristic (rec: 3)
  
  hightestPiece: weight of highest piece (rec: 5)
  
  contig: weight of contiguous area heuristic (rec: 2)
  
  hermit: weight of number of blocks over caves heuristic (rec: .5)
  
  pieceAmount: amount of pieces to play before stopping
  
  lookAhead: 1 for 1 piece lookahead, 0 for 0 piece lookahead. Only 1 and 0 are valid


Example: python3 gordon.py 10 20 3 5 2 .5 100000 1

This command would run the AI on the standard tetris board dimensions with recommended heuristic weights for up to 100k pieces with one piece lookahead.
