
from numpy import array
import copy
from Move import Move
from CastleRights import CastleRights

class GameState():
    def __init__(self):
        self.board = array(
            [["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        )
        self.whiteToMove = True
        self.movelog = []
        self.moveFunctions = { 'P': self.getPawnMoves, 'B': self.getBishopMoves , 'R': self.getRookMoves ,
                              'N': self.getKnightMoves , 'Q': self.getQueenMoves , 'K': self.getKingMoves }
        self.whiteKingPosition = (7,4)
        self.blackKingPosition = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = ()  #square where en-passant capture can
        self.enPassantCaptureLog = [()]
        self.currentCastleRights = CastleRights(True ,True, True, True)
        self.castleRightsLog = [ CastleRights(self.currentCastleRights.wks , self.currentCastleRights.bks, 
                                              self.currentCastleRights.wqs, self.currentCastleRights.bqs) ]


    def makeMove(self, move):
        assert self.board[move.endRow][move.endCol][1] != 'K'
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)  #log the move so that we can undo the move later
        self.whiteToMove = not self.whiteToMove  #swap players
        # update kings position
        if move.pieceMoved == "wK":
            self.whiteKingPosition = (move.endRow , move.endCol)
        if move.pieceMoved == "bK":
            self.blackKingPosition = (move.endRow , move.endCol)
        #if pawn moves twice , next move can capture enpassant
        if move.pieceMoved[1] == 'P' and abs( move.endRow - move.startRow ) == 2:
            self.enPassantPossible = ( (move.endRow + move.startRow)//2 , move.endCol )
            self.enPassantCaptureLog.append(copy.copy(self.enPassantPossible))
        else:
            self.enPassantPossible = ()
            self.enPassantCaptureLog.append(())
        # if en-passant move, must update the board to capture the pawn
        if move.enPassant:
            self.board[move.startRow][move.endCol] = "--"
        # if pawn promotion change piece
        if move.pawnPromotion:
            promotedPiece = move.promotedPiece 
            self.board[move.endRow][move.endCol] =  promotedPiece
        # castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #king side castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #moves the rook
                self.board[move.endRow][move.endCol+1] = '--' # erase the old rook
            else: # queen side castle
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]  #moves the rook
                self.board[move.endRow][move.endCol-2] = '--' # erase the old rook
        # update castle rights  - whenever it is a rook or queen side
        self.updateCastleRights(move)
        self.castleRightsLog.append( CastleRights(self.currentCastleRights.wks , self.currentCastleRights.bks, 
                                              self.currentCastleRights.wqs, self.currentCastleRights.bqs) )
        

    def undoMove(self):
        if len(self.movelog)!=0:    #make sure there is a move to undo
            move = self.movelog.pop()
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.whiteToMove = not self.whiteToMove  # turn changes
            # updating kings position
            if move.pieceMoved == 'wK':
                self.whiteKingPosition = (move.startRow , move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingPosition = (move.startRow , move.startCol)
            # undo enpassant log
            self.enPassantCaptureLog.pop()
            self.enPassantPossible = self.enPassantCaptureLog[-1]
            # undo enpassant is different
            if move.enPassant:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            # undo castling rights
            self.castleRightsLog.pop() # get rid of the new castle rights from the move we are undoing
            self.currentCastleRights = self.castleRightsLog[-1] #set the current castle rights to the last one in the list
            # undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: # king side castle
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else: # queen side castle
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'
        self.checkMate = False
        self.staleMate = False


    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK' :
            self.currentCastleRights.wks = False
            self.currentCastleRights.wqs = False
        elif move.pieceMoved == 'bK' :
            self.currentCastleRights.bks = False
            self.currentCastleRights.bqs = False
        elif move.pieceMoved == 'wR' :
            if move.startRow == 7 :
                if move.startCol == 0 : # left rook
                    self.currentCastleRights.wqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastleRights.wks = False
        elif move.pieceMoved == 'bR' :
            if move.startRow == 0 :
                if move.startCol == 0 : # left rook
                    self.currentCastleRights.bqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastleRights.bks = False
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 7:
                    self.currentCastleRights.wks = False
                if move.endCol == 0:
                    self.currentCastleRights.wqs = False
        if move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 7:
                    self.currentCastleRights.bks = False
                if move.endCol == 0:
                    self.currentCastleRights.bqs = False


    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingPosition[0]
            kingCol = self.whiteKingPosition[1]
        else:
            kingRow = self.blackKingPosition[0]
            kingCol = self.blackKingPosition[1]
        moves = []
        if self.inCheck:
            if len(self.checks)==1: # only 1 check, block check or move king
                temp_moves = self.getAllPossibleMoves()
                # to block a check you must move a piece into one the squares between the enemy piece and king
                check = self.checks[0] # check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]  #enemy piece causing the check
                validSquares = [] #squares that piece can move to
                if(pieceChecking[1] == 'N'):
                    validSquares = [(checkRow,checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = ( kingRow + i*check[2] , kingCol + i*check[3] )  #check[2] and check[3] are the check direction
                        validSquares.append(validSquare)
                        if validSquare == (checkRow , checkCol):    # break when you get to piece
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(temp_moves)-1, -1, -1):   # go through backwards when you are removing from list as iterating
                    if (temp_moves[i].pieceMoved[1] == 'K') or (temp_moves[i].endRow , temp_moves[i].endCol) in validSquares: #move doesn't block check or capture piece
                        moves.append(temp_moves[-1])
                    el = temp_moves.pop(-1)
            else: #double checks,king has to move
                self.getKingMoves(kingRow,kingCol,moves)
        else: #not to check so all moves are fine
            moves = self.getAllPossibleMoves()
        if len(moves)==0:
            if(self.inCheck):
                self.checkMate = True
            else:
                self.staleMate = True    
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    '''
    to find wheather current player got the check
    '''
    def isCheck(self):
        if self.whiteToMove:
            return self.isSquareUnderAtteck(self.whiteKingPosition[0], self.whiteKingPosition[1] )
        else:
            return self.isSquareUnderAtteck(self.blackKingPosition[0], self.blackKingPosition[1] )


    def isSquareUnderAtteck(self, r, c):
        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'
        kight_disp = [(-2,-1),(-2,1),(-1,-2),(1,-2),(2,1),(2,-1),(-1,2),(1,2)]
        directions = [ (1,0) , (-1,0) , (0,-1) , (0,1) , (-1,-1) , (-1,1) , (1,-1) , (1,1) ]
        for i in range(len(directions)): # loop for directions
            for j in range(1,8): # loop for movement in direction
                x = r + j*directions[i][0]
                y = c + j*directions[i][1]
                if x<0 or x>=8 or y<0 or y>=8: 
                    # checking if we are outside the grid 
                    break
                if self.board[x][y] == '--':
                    # if no piece is there then then checking further
                    continue
                if self.board[x][y][0] != enemyColor: 
                    #if piece is ally then no need to check further in this direction
                    break
                if j == 1 and self.board[x][y][1] == 'K':
                    # one square away and piece is king
                    return True
                elif j == 1 and self.board[x][y][1] == 'P' and ((enemyColor=='w' and 6<=i<=7 ) or (enemyColor=='b' and 4<=i<=5)):
                    # one square away and piece is pawn
                    return True
                elif self.board[x][y][1] == 'Q':
                    return True
                elif 0<=i<=3 and self.board[x][y][1] == 'R': 
                    # horizonal or vertical direction
                    return True
                elif 4<=i<=7 and self.board[x][y][1] == 'B': 
                    # diagonal direction
                    return True
                else:
                    break
        for d in kight_disp:
            x = r + d[0]
            y = c + d[1]
            if x<0 or x>=8 or y<0 or y>=8 : 
                # checking if we are outside the grid 
                continue
            if self.board[x][y] == enemyColor + 'N':
                return True
        return False

    def printAllSquaresWeatherCanBeAttackedOrNot(self):
        for i in range(0,8):
            for j in range(0,8):
                print(int(self.isSquareUnderAtteck(i,j)) , end=" ")
            print()
        print()

    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # no of rows
            for c in range(len(self.board[r])): # no of columns
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves
    
    def printKingPositions(self):
        print("White king : ", self.whiteKingPosition)
        print("Black king : ", self.blackKingPosition)
        if(self.checkMate):
            print("CheckMate")
        if(self.staleMate):
            print("StaleMate")
        print("BKS = ",self.currentCastleRights.bks  , "BQS = ", self.currentCastleRights.bqs , 
              " WKS =" ,self.currentCastleRights.wks , "WQS = ", self.currentCastleRights.wqs)


    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1]==c:
                piecePinned = True
                pinDirection = ( self.pins[i][2] , self.pins[i][3] )
                break
        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
            allycolor = 'w'
            kingRow, kingCol = self.whiteKingPosition
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
            allycolor = 'b'
            kingRow, kingCol = self.blackKingPosition
        piecesForPawnPromotion = ['Q', 'R', 'B', 'N']
        if self.board[r+moveAmount][c] == '--': # 1 square move
            if not piecePinned or pinDirection == (moveAmount,0):
                if r+moveAmount==backRow:  # if piece gets back rank then it is a pawn promotion
                    for piece in piecesForPawnPromotion:
                        moves.append(Move( (r,c) , (r+moveAmount,c) , self.board , 
                                          pawnPromotion=True, promotedPiece= allycolor + piece) )
                else:
                    moves.append( Move( (r,c) , (r+moveAmount,c) , self.board ) )
                if r==startRow and self.board[r + 2*moveAmount][c] == "--": #2 square move
                    moves.append( Move( (r,c) , ( r + 2*moveAmount , c ) , self.board ) )
        if c-1>=0:  #capture to the left
            if not piecePinned or pinDirection == (moveAmount,-1):
                if self.board[r+moveAmount][c-1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        for piece in piecesForPawnPromotion:
                            moves.append( Move( (r,c) , (r+moveAmount , c-1) , self.board ,
                                               pawnPromotion=True , promotedPiece=allycolor+piece  ) )
                    else:
                        moves.append( Move( (r,c) , (r+moveAmount , c-1) , self.board  ) )
                if (r+moveAmount,c-1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c: #king is left of the pawn
                            insideRange = range(kingCol+1, c-1)
                            outsideRange = range(c+1, 8)
                        else: #king is right to pawn
                            insideRange = range(c+1, kingCol)
                            outsideRange = range(c-2, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != '--':
                                blockingPiece = True
                                break
                        for i in outsideRange:
                            if self.board[r][i] != '--':
                                if self.board[r][[i]] == enemyColor + 'R' or self.board[r][[i]] == enemyColor + 'Q':
                                    attackingPiece = True
                                else:
                                    blockingPiece = True
                                break
                    if blockingPiece or not attackingPiece:
                        moves.append( Move( (r,c) , (r+moveAmount,c-1) , self.board , enPassant = True ) )
        if c+1<=7: #capture to the right
            if not piecePinned or pinDirection == (moveAmount,1):
                if self.board[r+moveAmount][c+1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        for piece in piecesForPawnPromotion:
                            moves.append( Move( (r,c) , (r+moveAmount , c+1) , self.board , 
                                               pawnPromotion = True , promotedPiece=allycolor + piece ) )
                    else:
                        moves.append( Move( (r,c) , (r+moveAmount , c+1) , self.board ) )
                if (r+moveAmount,c+1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c: #king is left of the pawn
                            insideRange = range(kingCol+1, c)
                            outsideRange = range(c+2, 8)
                        else: #king is right to pawn
                            insideRange = range(c+2, kingCol)
                            outsideRange = range(c-1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != '--':
                                blockingPiece = True
                                break
                        for i in outsideRange:
                            if self.board[r][i] != '--':
                                if self.board[r][[i]] == enemyColor + 'R' or self.board[r][[i]] == enemyColor + 'Q':
                                    attackingPiece = True
                                else:
                                    blockingPiece = True
                                break
                    if blockingPiece or not attackingPiece:
                        moves.append( Move( (r,c) , (r+moveAmount,c+1) , self.board , enPassant = True ) )


    def getRookMoves(self, r , c, moves):
        piecePinned = False
        pinDirection = ()
        for d in self.pins:
            if d[0]==r and d[1]==c:
                piecePinned = True
                pinDirection = (d[2],d[3])
                break
        dir = [ (-1,0) , (1,0) , (0,-1) , (0,1) ]
        for d in dir:
            if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                for i in range(1,8):
                    x = r + d[0]*i
                    y = c + d[1]*i
                    if x<0 or x>7 or y<0 or y>7 or self.board[x][y][0] == self.board[r][c][0]:
                        break
                    elif self.board[x][y] == '--':
                        moves.append(Move( (r,c) , (x,y) , self.board ))
                    else:
                        moves.append(Move( (r,c) , (x,y) , self.board ))
                        break


    def getKnightMoves(self, r , c, moves):
        piecePinned = False
        for d in self.pins:
            if d[0]==r and d[1]==c:
                piecePinned = True
                break
        disp = [(-2,-1),(-2,1),(-1,-2),(1,-2),(2,1),(2,-1),(-1,2),(1,2)]
        for d in disp:
            if r+d[0]<0 or r+d[0]>7 or c+d[1]<0 or c+d[1]>7 or self.board[r+d[0]][c+d[1]][0]==self.board[r][c][0]:
                continue
            else:
                if not piecePinned:
                    moves.append(Move((r,c), (r+d[0],c+d[1]), self.board))


    def getQueenMoves(self, r , c, moves):
        # queen is the combination of moves of ROOK and BISHOP
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)


    def getBishopMoves(self, r , c, moves):
        dir = [ (-1,-1) , (-1,1) , (1,-1), (1,1) ]
        piecePinned = False
        pinDirection = ()
        for d in self.pins:
            if d[0]==r and d[1]==c:
                piecePinned = True
                pinDirection = (d[2],d[3])
                break
        for d in dir:
            if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                for i in range(1,8):
                    x = r + d[0]*i
                    y = c + d[1]*i
                    if x<0 or y<0 or x>7 or y>7 or self.board[x][y][0] == self.board[r][c][0]:
                        break
                    elif self.board[x][y] == '--':
                        moves.append( Move( (r,c) , (x,y) , self.board ) )
                    else:
                        moves.append( Move( (r,c) , (x,y) , self.board ) )
                        break


    def getKingMoves(self, r , c, moves):
        disp = [ (-1,-1) , (-1,0) , (-1,1) , (0,-1) , (0,1) , (1,-1) , (1,0) , (1,1) ]
        kingColor = self.board[r][c][0]
        piece = self.board[r][c]
        self.board[r][c] = '--'
        toadd = []
        for d in disp:
            endRow = r + d[0]
            endCol = c + d[1]
            if endRow<0 or endRow>7 or endCol<0 or endCol>7 or self.board[endRow][endCol][0]==kingColor:
                continue
            else:
                if not self.isSquareUnderAtteck(endRow, endCol):
                    toadd.append((endRow,endCol))
        self.board[r][c] = piece
        for (endRow,endCol) in toadd:
            moves.append(Move((r,c), (endRow,endCol), self.board))
        self.getCastleMoves(r, c, moves)

    """
    Generates all valid castle moves for the king at (r, c) and add them to the list of moves 
    """
    def getCastleMoves(self, r, c, moves):
        if self.isCheck():
            return # can't castle while we are in check
        if (self.whiteToMove and self.currentCastleRights.wks) or ( not self.whiteToMove and self.currentCastleRights.bks ):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastleRights.wqs) or ( not self.whiteToMove and self.currentCastleRights.bqs ):
            self.getQueenSideCastleMoves(r, c, moves)
        
        

    def getKingSideCastleMoves(self, r, c, moves ):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.isSquareUnderAtteck(r, c+1) and not self.isSquareUnderAtteck(r,c+2):
                moves.append( Move( (r, c), (r, c+2), self.board, isCastleMove = True ) ) 
            else:
                if self.board[r][c][0] == 'w':
                    self.currentCastleRights.wks = False
                else:
                    self.currentCastleRights.bks = False
            


    def getQueenSideCastleMoves(self, r, c, moves ):
        if self.board[r][c-1] == '--' and self.board[r][c-2]=='--' and self.board[r][c-3]=='--':
            if not self.isSquareUnderAtteck(r, c-1) and not self.isSquareUnderAtteck(r,c-2):
                moves.append( Move( (r, c), (r, c-2), self.board, isCastleMove = True ) ) 
            else:
                if self.board[r][c][0] == 'w':
                    self.currentCastleRights.wqs = False
                else:
                    self.currentCastleRights.bqs = False

    '''
    Returns if the player is in the check, a list of pins , and a list of checks
    '''
    def checkForPinsAndChecks(self):
        pins = [] #squares where the allied pinned piece is and direction pinned from
        checks = [] # squares where enemy is applying a check
        inCheck = False
        # check outward from the king for pins and checks, keep track of pins
        directions = [ (1,0) , (-1,0) , (0,-1) , (0,1) , (-1,-1) , (-1,1) , (1,-1) , (1,1) ]
        if self.whiteToMove :
            allyColor = "w"
            enemyColor = "b"
            startRow = self.whiteKingPosition[0]
            startCol = self.whiteKingPosition[1]
        else:
            allyColor = "b"
            enemyColor = "w"
            startRow = self.blackKingPosition[0]
            startCol = self.blackKingPosition[1]
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # reset possibel pins
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if endRow>=0 and endRow<=7 and endCol>=0 and endCol<=7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == (): # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol , d[0] , d[1])
                        else: # 2nd allied piece so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if ( 0 <=j <= 3  and type=='R' ) or ( 4<=j<=7 and type=='B' ) or (i==1 and type == 'P' and (( enemyColor=='w' and 6<=j<=7 ) or ( enemyColor=='b' and 4<=j<=5 )) ) or (type=='Q') or (i==1 and type=='K'):
                            if possiblePin == (): # no piece blocking direct check
                                inCheck = True
                                checks.append((endRow,endCol, d[0],d[1]))
                            else: #piece blocking so pin
                                pins.append(possiblePin)
                        else: # enemy piece not applying check
                            break
                else:
                    break # off board
        # check for knight checks
        knightMoves = ( (-2,-1) , (-2,1) , (2,-1) , (2,1) , (-1,-2) , (1,-2) , (1,2) , (-1,2) )
        for d in knightMoves:
            endRow = startRow + d[0]
            endCol = startCol + d[1]
            if (0<=endRow<=7) and (0<=endCol<=7):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] =='N':
                    inCheck = True
                    checks.append((endRow, endCol , d[0] , d[1]))
        return inCheck, pins, checks




