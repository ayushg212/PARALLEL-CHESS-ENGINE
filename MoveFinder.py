import random
import multiprocessing
import copy

pieceScore = { 'K':20000, 'Q': 1000, 'R': 500, 'B': 325, 'N': 325, 'P':100 }
CHECKMATE = 1000000
STALEMATE = 0
DEPTH = 6


mirror = [
    56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 ,
    48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 ,
    40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 ,
    32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 ,
    24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 ,
    16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 ,
    8  , 9  , 10 , 11 , 12 , 13 , 14 , 15 ,
    0  , 1  , 2  , 3  , 4  , 5  , 6  , 7
    ]


PAWN_SQ_VAL = [
    0  , 0  , 0  , 0   , 0   , 0  , 0  , 0  ,
    10 , 10 , 0  , -10 , -10 , 0  , 10 , 10 ,
    5  , 0  , 0  , 5   , 5   , 0  , 0  , 5  ,
    0  , 0  , 10 , 20  , 20  , 10 , 0  , 0  ,
    5  , 5  , 5  , 10  , 10  , 5  , 5  , 5  ,
    10 , 10 , 10 , 20  , 20  , 10 , 10 , 10 ,
    20 , 20 , 20 , 30  , 30  , 20 , 20 , 20 ,
    0  , 0  , 0  , 0   , 0   , 0  , 0  , 0  
    ]

KNIGHT_SQ_VAL = [
    0  , -10 , 5  , 0  , 0  , 5  , -10 , 0  ,
    0  , 0   , 0  , 5  , 5  , 0  , 0   , 0  ,
    0  , 0   , 10 , 10 , 10 , 10 , 0   , 0  ,
    0  , 5   , 10 , 20 , 20 , 10 , 5   , 0  ,
    5  , 10  , 15 , 20 , 20 , 15 , 10  , 5  ,
    10 , 15  , 15 , 25 , 25 , 15 , 15  , 10 ,
    0  , 0   , 5  , 10 , 10 , 5  , 0   , 0  ,
    0  , 0   , 0  , 0  , 0  , 0  , 0   , 0
    ]

BISHOP_SQ_VAL = [
    -5 , 0  , -10 , 0  , 0  , -10 , 0  , -5 ,
    0  , 20 , 0   , 15 , 15 , 0   , 20 , 0  ,
    0  , 0  , 15  , 10 , 10 , 15  , 5  , 0  ,
    0  , 10 , 0   , 15 , 15 , 10  , 5  , 5  ,
    0  , 10 , 0   , 15 , 15 , 10  , 10 , 0  ,
    0  , 0  , 15  , 5  , 5  , 15  , 0  , 0  ,
    0  , 15 , 0   , 10 , 10 , 0   , 15 , 0  ,
    -5 , 0  , 0   , 0  , 0  , 0   , 0  , -5
    ]


ROOK_SQ_VAL = [
    0  , 0  , 5  , 10 , 10 , 5  , 0  , 0  ,
    0  , 0  , 5  , 10 , 10 , 5  , 0  , 0  ,
    0  , 0  , 5  , 10 , 10 , 5  , 0  , 0  ,
    0  , 0  , 5  , 10 , 10 , 5  , 0  , 0  ,
    0  , 0  , 5  , 10 , 10 , 5  , 0  , 0  ,
    0  , 0  , 5  , 10 , 10 , 5  , 0  , 0  ,
    25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 ,
    0  , 0  , 5  , 10 , 10 , 5  , 0  , 0
    ]

QUEEN_SQ_VAL = [
    0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
    0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
    0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
    0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
    0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
    0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
    0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
    0 , 0 , 0 , 0 , 0 , 0 , 0 , 0
    ]

KING_SQ_VAL_END = [
    -50 , -10 , 0  , 0  , 0  , 0  , -10 , -50 ,
    -10 , 0   , 10 , 10 , 10 , 10 , 0   , -10 ,
    0   , 10  , 15 , 15 , 15 , 15 , 10  , 0   ,
    0   , 10  , 15 , 20 , 20 , 15 , 10  , 0   ,
    0   , 10  , 15 , 20 , 20 , 15 , 10  , 0   ,
    0   , 10  , 15 , 15 , 15 , 15 , 10  , 0   ,
    -10 , 0   , 10 , 10 , 10 , 10 , 0   , -10 ,
    -50 , -10 , 0  , 0  , 0  , 0  , -10 , -50
    ]

KING_SQ_VAL = [
    0   , 10  , 10  , -10 , 0   , -10  , 20  , 5   ,
    0   , 0   , 5   , 0   , 0   , 0   , 5   , 0   ,
    -10 , -10 , -10 , -10 , -10 , -10 , -10 , -10 ,
    -70 , -70 , -70 , -70 , -70 , -70 , -70 , -70 ,
    -70 , -70 , -70 , -70 , -70 , -70 , -70 , -70 ,
    -70 , -70 , -70 , -70 , -70 , -70 , -70 , -70 ,
    -70 , -70 , -70 , -70 , -70 , -70 , -70 , -70 ,
    -70 , -70 , -70 , -70 , -70 , -70 , -70 , -70
    ]

pieceTable = {'P' : PAWN_SQ_VAL, 'N': KNIGHT_SQ_VAL, 'B' : BISHOP_SQ_VAL, 'R': ROOK_SQ_VAL , 
              'Q': QUEEN_SQ_VAL, 'K' : [KING_SQ_VAL , KING_SQ_VAL_END] }

def getTableScores(r, c, piece, piececount):
    assert piece != '--'
    pos = r*8 + c
    if piece[0] == 'w':
        pos = mirror[pos]
    if piece[1] != 'K':
        return pieceTable[piece[1]][pos]
    else:
        if piececount <= 8:
            return KING_SQ_VAL_END[pos]
        else:
            return KING_SQ_VAL[pos]
        

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def runMoveScoreFunctionInNewProcess(moveIndex, scoreList, gs):
    # score = findMoveScoreMinMax(gs , DEPTH-1)
    score = findMoveScoreMinMaxAlphaBeta(gs, DEPTH-1)
    scoreList[moveIndex] = score


def findBestMoveMinMaxAlphaBetaParallalProcessing(gs, resultInd):
    # bestScore = -CHECKMATE if gs.whiteToMove else CHECKMATE
    if gs.checkMate or gs.staleMate:
        resultInd.value = -1
        return 
    validMoves = gs.getValidMoves()
    processes = []
    scoreList = multiprocessing.Array('i', len(validMoves))
    for ind,move in enumerate(validMoves):
        gs.makeMove(move)
        p = multiprocessing.Process(target=runMoveScoreFunctionInNewProcess, args=(ind, scoreList, copy.deepcopy(gs) ,))
        processes.append(p)
        gs.undoMove()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    scoreList = list(scoreList)
    res = []
    for i in range(0,len(scoreList)):
        res.append((scoreList[i],i))
    res.sort()
    if gs.whiteToMove:
        ind = res[-1][1]
    else:
        ind = res[0][1]
    resultInd.value = ind


def findBestMoveMinMax(gs):
    global count
    count = 0
    bestMove = None
    bestScore = -CHECKMATE if gs.whiteToMove else CHECKMATE
    validMoves = gs.getValidMoves()
    random.shuffle(validMoves)
    for move in validMoves:
        count += 1
        gs.makeMove(move)
        score = findMoveScoreMinMaxAlphaBeta(gs,DEPTH-1)
        gs.undoMove()
        if gs.whiteToMove:
            if score > bestScore:
                bestScore = score
                bestMove = move
        else:
            if score < bestScore:
                bestScore = score
                bestMove = move
    print(count)
    return bestMove


def findBestMoveMinMaxAlphaBeta(gs):
    count = 0
    bestMove = None
    bestScore = -CHECKMATE if gs.whiteToMove else CHECKMATE
    validMoves = gs.getValidMoves()
    random.shuffle(validMoves)
    for move in validMoves:
        gs.makeMove(move)
        score = findMoveScoreMinMaxAlphaBeta(gs,DEPTH-1)
        gs.undoMove()
        if gs.whiteToMove:
            if score > bestScore:
                bestScore = score
                bestMove = move
        else:
            if score < bestScore:
                bestScore = score
                bestMove = move
    return bestMove


def findMoveScoreMinMax(gs, depth):
    if depth == 0:
        return scoreBoard(gs)
    if gs.checkMate:
        return -CHECKMATE if gs.whiteToMove else CHECKMATE
    if gs.staleMate:
        return STALEMATE
    validMoves = gs.getValidMoves()
    bestScore = -CHECKMATE if gs.whiteToMove else CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        score = findMoveScoreMinMax(gs, depth-1)
        gs.undoMove()
        if gs.whiteToMove:
            bestScore = max(bestScore, score)
        else:
            bestScore = min(bestScore, score)
    return bestScore


def findMoveScoreMinMaxAlphaBeta(gs, depth, alpha = -CHECKMATE , beta = CHECKMATE):
    if depth == 0:
        return scoreBoard(gs)
    if gs.checkMate:
        return -CHECKMATE if gs.whiteToMove else CHECKMATE
    if gs.staleMate:
        return STALEMATE
    validMoves = gs.getValidMoves()
    # move ordering
    scoreWithIndex = []
    for ind,move in enumerate(validMoves):
        gs.makeMove(move)
        score = scoreBoard(gs)
        scoreWithIndex.append((score, ind))
        gs.undoMove()
    if gs.whiteToMove:
        scoreWithIndex.sort(reverse = True)
    else:
        scoreWithIndex.sort()
    # beam search
    n = len(validMoves)
    n = min(8,n)
    # if n > 20:
    #     n = (n+4)//5 # only best 20% of child are going to be searched
    # elif 5<=n<=20:
    #     n = 4
    bestScore = -CHECKMATE if gs.whiteToMove else CHECKMATE
    for i in range(0,n):
        gs.makeMove(validMoves[scoreWithIndex[i][1]])
        score = findMoveScoreMinMaxAlphaBeta(gs, depth-1,alpha,beta)
        gs.undoMove()
        if gs.whiteToMove:
            bestScore = max(score,bestScore)
            alpha = max(alpha , bestScore)
            if alpha >= beta:
                break
        else:
            bestScore = min(score, bestScore )
            beta = min(beta, bestScore)
            if beta <= alpha:
                break
    return bestScore


def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE # black wins
        else:
            return CHECKMATE # while wins
    elif gs.staleMate:
        return STALEMATE
    score = 0
    piececount = 0
    for row in gs.board:
        for piece in row:
            if piece != '--':
                piececount += 1
    if len(gs.movelog) > 0:
        if gs.movelog[-1].isCastleMove :
            score = 100 if gs.whiteToMove else -100
    for r in range(0,8):
        for c in range(0,8):
            if gs.board[r][c][0] == 'w':
                score += (pieceScore[gs.board[r][c][1]] + getTableScores(r,c,gs.board[r][c], piececount))
            elif gs.board[r][c][0] == 'b':
                score -= (pieceScore[gs.board[r][c][1]] + getTableScores(r,c,gs.board[r][c], piececount))
    return score

