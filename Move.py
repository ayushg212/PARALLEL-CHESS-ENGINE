


class Move():
    def __init__(self, startSq, endSq, board, enPassant=False, pawnPromotion=False , isCastleMove = False , promotedPiece = None):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.enPassant = enPassant
        self.isCastleMove = isCastleMove
        self.pawnPromotion = pawnPromotion
        self.promotedPiece = promotedPiece
        if self.enPassant:
            self.pieceCaptured = 'bP' if self.pieceMoved == 'wP' else 'wP'
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID and self.pawnPromotion==other.pawnPromotion and self.promotedPiece==other.promotedPiece
        return False


