

import pygame as p
import GameState
import MoveFinder
from numpy import array
import multiprocessing
from Button import Button

WIDTH = HEIGHT = 640 #400 is also a option
DIMENSION = 8 # for chess it is 8X8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60 
IMAGES = {}
IMAGES_FOR_PAWN_PROMOTION = {}
pieces = array(['K','N','R','P','B','Q'])
color = array(['w','b'])
piecesForPawnPromotion = ['Q', 'R', 'B', 'N']
cordinatesForPawnPromotion = [ (1,1), (1,4), (4,1), (4,4) ]
board_colors = array([p.Color("#eeeed2") , p.Color("#769656")])
pawnPromotionBackgroundColor = board_colors[0]


def loadImages():
	for clr in color:
		for piece in pieces:
			res = clr + piece
			IMAGES[res] = p.transform.smoothscale(p.image.load('images/new/' + res + '.png') , (SQ_SIZE, SQ_SIZE))
	# we can access the images by IMAGES['wP']


def loadImagesForPawnPromotion():
	for clr in color:
		for piece in piecesForPawnPromotion:
			res = clr + piece
			IMAGES_FOR_PAWN_PROMOTION[res] = p.transform.smoothscale(p.image.load('images/new/' + res + '.png') ,
																(3*SQ_SIZE, 3*SQ_SIZE))
			
			
def displayPiecesForPawnPromotion(screen, color):  
	for i in range(len(piecesForPawnPromotion)):
		piece = color + piecesForPawnPromotion[i]
		r = cordinatesForPawnPromotion[i][0]
		c = cordinatesForPawnPromotion[i][1]
		rect = p.Rect(c*SQ_SIZE, r*SQ_SIZE, 3*SQ_SIZE, 3*SQ_SIZE)
		screen.blit(IMAGES_FOR_PAWN_PROMOTION[piece], rect)
		if rect.collidepoint(p.mouse.get_pos()):
			 p.draw.rect(screen, "black", p.Rect(c*SQ_SIZE, r*SQ_SIZE, 3*SQ_SIZE, 3*SQ_SIZE), 3)


def getPieceIndPawnPromotion(location):
	row = location[0]//SQ_SIZE
	col = location[1]//SQ_SIZE
	for i in range(len(piecesForPawnPromotion)):
		if col >= cordinatesForPawnPromotion[i][0] and col < cordinatesForPawnPromotion[i][0] + 3 :
			if row >= cordinatesForPawnPromotion[i][1] and row < cordinatesForPawnPromotion[i][1] + 3:
				return i
	return -1


def getPawnPromotionInputPiece(screen, color , clock):
	running = True
	while running:
		for e in p.event.get():
			if e.type == p.QUIT:
				exit()
			elif e.type == p.MOUSEBUTTONDOWN:
				location = p.mouse.get_pos()
				pos = getPieceIndPawnPromotion(location)
				if pos != -1:
					return color + piecesForPawnPromotion[pos]
		location = p.mouse.get_pos()
		print(location)
		print(getPieceIndPawnPromotion(location))
		screen.fill(pawnPromotionBackgroundColor)
		displayPiecesForPawnPromotion(screen, color)
		clock.tick(MAX_FPS)
		p.display.flip()


def displayMenuAndGetChoiceFromUser():
	BG = p.transform.scale(p.image.load("images/MenuImage.png"),(WIDTH,HEIGHT))
	running = True
	p.display.set_caption("Menu")
	multiplayerButton = Button((WIDTH/2,HEIGHT/2 - SQ_SIZE),"MULTIPLAYER",p.font.SysFont("Helvitca", SQ_SIZE, True, False), "Black","White")
	computerButton = Button((WIDTH/2,HEIGHT/2 + 0.5*SQ_SIZE ),"COMPUTER",p.font.SysFont("Helvitca", SQ_SIZE, True, False), "Black","White")
	quitButton = Button((WIDTH/2,HEIGHT/2+ 2*SQ_SIZE),"QUIT",p.font.SysFont("Helvitca", SQ_SIZE, True, False), "Black","White")
	while running:
		for e in p.event.get():
			if e.type == p.QUIT:
				quit()
			if e.type == p.MOUSEBUTTONDOWN:
				pos = p.mouse.get_pos()
				if multiplayerButton.checkForInput(pos):
					return [0,-1]
				if computerButton.checkForInput(pos):
					return [1, displayPieceChoicesAndGetChoiceFromUser()]
				if quitButton.checkForInput(pos):
					quit()
		screen.blit(BG, (0,0))
		multiplayerButton.update(screen,p.mouse.get_pos())
		computerButton.update(screen, p.mouse.get_pos())
		quitButton.update(screen, p.mouse.get_pos())
		clock.tick(60)
		p.display.flip()


def displayPieceChoicesAndGetChoiceFromUser():
	p.display.set_caption("Piece Choice")
	font = p.font.SysFont("Helvitca", SQ_SIZE, True, False)
	text_input = "CHOOSE ONE SIDE" 
	BG = p.transform.scale(p.image.load("images/PieceChoiceBackground.jpg"),(WIDTH,HEIGHT))
	whiteImg = p.transform.scale(p.image.load("images/whitePiece2.png"),(2*SQ_SIZE, 5*SQ_SIZE))
	blackImg = p.transform.scale(p.image.load("images/blackPiece2.png"),(2*SQ_SIZE, 5*SQ_SIZE))
	text = font.render(text_input, True, "White")
	rectWhitePiece = p.Rect(SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE, 5*SQ_SIZE)
	rectBlackPiece = p.Rect(5*SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE, 5*SQ_SIZE)
	running = True 
	extra = SQ_SIZE//7
	while running:
		for e in p.event.get():
			if e.type == p.QUIT:
				quit()
			elif e.type == p.MOUSEBUTTONDOWN:
				pos = p.mouse.get_pos()
				if rectWhitePiece.collidepoint(pos):
					return 0
				if rectBlackPiece.collidepoint(pos):
					return 1
		screen.blit(BG, (0,0))
		screen.blit(text , ( 4*SQ_SIZE - text.get_width()/2 , SQ_SIZE - text.get_height()/2))
		screen.blit(whiteImg, rectWhitePiece)
		screen.blit(blackImg, rectBlackPiece)
		if rectWhitePiece.collidepoint(p.mouse.get_pos()):
			p.draw.rect(screen, 'Black' , p.Rect(SQ_SIZE-extra, 2*SQ_SIZE-extra, 2*SQ_SIZE+2*extra, 5*SQ_SIZE+2*extra) , extra//2 )
		if rectBlackPiece.collidepoint(p.mouse.get_pos()):
			p.draw.rect(screen, 'white' , p.Rect(5*SQ_SIZE-extra, 2*SQ_SIZE-extra, 2*SQ_SIZE+2*extra, 5*SQ_SIZE+2*extra) , extra//2 )
		clock.tick(60)
		p.display.flip()


def runMultiplayerMode():
	gs = GameState.GameState()
	validMoves = gs.getValidMoves()
	print("Possible moves :",len(validMoves))
	loadImages() 
	loadImagesForPawnPromotion()
	running = True
	sqSelected = () 
	playerClicks = [] 
	gameOver = False
	turn = 0
	while(running):
		assert (turn==0 and gs.whiteToMove) or (turn==1 and not gs.whiteToMove)
		for e in p.event.get():
			if e.type == p.QUIT:
				quit()
			elif e.type == p.MOUSEBUTTONDOWN :
				if not gameOver:
					location = p.mouse.get_pos() 
					col = location[0]//SQ_SIZE
					row = location[1]//SQ_SIZE
					if(sqSelected == (row,col) ): 
						sqSelected = () 
						playerClicks = [] 
					else:
						sqSelected = (row,col)
						playerClicks.append(sqSelected)
					if len(playerClicks) == 2:
						move = GameState.Move(playerClicks[0], playerClicks[1], gs.board)
						if isPawnPromotionMove(move, validMoves):
							color = 'w' if gs.whiteToMove else 'b'
							piece = getPawnPromotionInputPiece(screen, color, clock)
							move.pawnPromotion = True
							move.promotedPiece = piece
						moveMade = False
						for i in range(len(validMoves)):
							if move == validMoves[i]:
								gs.makeMove(validMoves[i])
								animateMove(validMoves[i], screen, gs.board, clock)
								turn = (turn+1)%2
								moveMade = True
								validMoves = gs.getValidMoves()
								sqSelected = () 
								playerClicks = [] 
								break
						if not moveMade:
							playerClicks = [sqSelected]
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z:
					if len(gs.movelog) > 0:
						turn = (turn + 1)%2 
						gs.undoMove()
						validMoves = gs.getValidMoves()
					gameOver = False
					sqSelected = () 
					playerClicks = [] 
				if e.key == p.K_r:
					gs = GameState.GameState()
					validMoves = gs.getValidMoves()
					turn = 0
					gameOver = False
					sqSelected = ()
					playerClicks = []		
		drawGameState(screen, gs, validMoves , sqSelected , gs.movelog)
		if gs.checkMate:
			gameOver = True
			if gs.whiteToMove:
				drawText(screen, 'Black wins by CheckMate')
			else:
				drawText(screen, 'White wins by CheckMate')
		if gs.staleMate:
			gameOver = True
			drawText(screen, 'StaleMate')
		clock.tick(MAX_FPS)
		p.display.flip()

def runComputerMode():
	gs = GameState.GameState()
	validMoves = gs.getValidMoves()
	print("Possible moves :",len(validMoves))
	loadImages() 
	loadImagesForPawnPromotion()
	running = True
	sqSelected = () 
	playerClicks = [] 
	gameOver = False
	humanTurn = [whiteIsHuman, blackIsHuman]
	turn = 0
	task = None
	thinking = False
	while(running):
		assert (turn==0 and gs.whiteToMove) or (turn==1 and not gs.whiteToMove)
		for e in p.event.get():
			if e.type == p.QUIT:
				if task != None and task.is_alive():
					task.terminate()
				quit()
			elif e.type == p.MOUSEBUTTONDOWN :
				if humanTurn[turn] and not gameOver:
					location = p.mouse.get_pos() 
					col = location[0]//SQ_SIZE
					row = location[1]//SQ_SIZE
					if(sqSelected == (row,col) ): 
						sqSelected = () 
						playerClicks = [] 
					else:
						sqSelected = (row,col)
						playerClicks.append(sqSelected)
					if len(playerClicks) == 2:
						move = GameState.Move(playerClicks[0], playerClicks[1], gs.board)
						if isPawnPromotionMove(move, validMoves):
							color = 'w' if gs.whiteToMove else 'b'
							piece = getPawnPromotionInputPiece(screen, color, clock)
							move.pawnPromotion = True
							move.promotedPiece = piece
						moveMade = False
						for i in range(len(validMoves)):
							if move == validMoves[i]:
								gs.makeMove(validMoves[i])
								animateMove(validMoves[i], screen, gs.board, clock)
								turn = (turn+1)%2
								moveMade = True
								validMoves = gs.getValidMoves()
								sqSelected = () 
								playerClicks = [] 
								break
						if not moveMade:
							playerClicks = [sqSelected]
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z:
					if task != None and task.is_alive():
						task.terminate()
						thinking = False
						if len(gs.movelog) > 0:
							turn = (turn + 1)%2 
							gs.undoMove()
							validMoves = gs.getValidMoves()
					elif len(gs.movelog) >= 2:
						gs.undoMove()
						gs.undoMove()
						validMoves = gs.getValidMoves()
					gameOver = False
					sqSelected = () 
					playerClicks = [] 
				if e.key == p.K_r:
					if task != None and task.is_alive():
						task.terminate()
						thinking = False
					gs = GameState.GameState()
					validMoves = gs.getValidMoves()
					turn = 0
					gameOver = False
					sqSelected = ()
					playerClicks = []		
		if not humanTurn[turn] and not gameOver:
			# AI move
			if not thinking:
				moveInd = multiprocessing.Value('i')
				task = multiprocessing.Process(target=MoveFinder.findBestMoveMinMaxAlphaBetaParallalProcessing,args=(gs, moveInd, ))
				task.start()
				thinking = True
			if not task.is_alive():
				task.join()
				thinking = False
				if moveInd.value != -1:
					gs.makeMove(validMoves[moveInd.value])
					animateMove(validMoves[moveInd.value], screen, gs.board, clock)
					validMoves = gs.getValidMoves()
					turn = (turn+1)%2
		drawGameState(screen, gs, validMoves , sqSelected , gs.movelog)
		if gs.checkMate:
			gameOver = True
			if gs.whiteToMove:
				drawText(screen, 'Black wins by CheckMate')
			else:
				drawText(screen, 'White wins by CheckMate')
		if gs.staleMate:
			gameOver = True
			drawText(screen, 'StaleMate')
		clock.tick(MAX_FPS)
		p.display.flip()

def isPawnPromotionMove(move , validMoves):
	for mv in validMoves:
		if mv.startRow == move.startRow and mv.startCol == move.startCol:
			if mv.endRow == move.endRow and mv.endCol == move.endCol:
				if mv.pawnPromotion:
					return True
	return False


def drawText(screen, text):
	font = p.font.SysFont("Helvitca", 4*SQ_SIZE//5 , True, False)
	textObject = font.render(text, 0, 'Grey')
	textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2 , HEIGHT/2 - textObject.get_height()/2)
	screen.blit(textObject, textLocation)
	textObject = font.render(text, 0, 'Blue')
	screen.blit(textObject, textLocation.move(2,2))


def highlightSquares(screen , gs , validMoves, sqSelected, movelog):
	if gs.inCheck:
		if gs.whiteToMove:
			r,c = gs.whiteKingPosition
		else:
			r,c = gs.blackKingPosition
		s = p.Surface((SQ_SIZE, SQ_SIZE))
		s.set_alpha(255)
		s.fill('red')
		screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE) )
		p.draw.rect(screen , 'black' , p.Rect(c*SQ_SIZE, r*SQ_SIZE ,SQ_SIZE, SQ_SIZE ) , SQ_SIZE//22 )
	if len(movelog) > 0:
		s = p.Surface((SQ_SIZE, SQ_SIZE))
		s.set_alpha(255)
		s.fill('white')
		r, c = (movelog[-1].startRow , movelog[-1].startCol)
		screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE) )
		p.draw.rect(screen , 'brown' , p.Rect(c*SQ_SIZE, r*SQ_SIZE ,SQ_SIZE, SQ_SIZE ) , SQ_SIZE//22 )
		r, c = (movelog[-1].endRow , movelog[-1].endCol)
		screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE) )
		p.draw.rect(screen , 'brown' , p.Rect(c*SQ_SIZE, r*SQ_SIZE ,SQ_SIZE, SQ_SIZE ) , SQ_SIZE//22 )
	if sqSelected != ():
		r, c = sqSelected
		if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
			#highlight selected square
			s = p.Surface((SQ_SIZE, SQ_SIZE))
			s.set_alpha(200) # transparency value -> 0 transparent, 255 opaque
			s.fill('#6f00ff')
			screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE) )
			p.draw.rect(screen , 'white' , p.Rect(c*SQ_SIZE, r*SQ_SIZE ,SQ_SIZE, SQ_SIZE ) , SQ_SIZE//22 )
			# highlight moves from that squares
			s.set_alpha(255)
			s.fill('#f2ca5c')
			for move in validMoves:
				if move.startRow == r and move.startCol == c:
					screen.blit(s, (move.endCol*SQ_SIZE , move.endRow*SQ_SIZE))
					p.draw.rect(screen , 'white' , p.Rect(move.endCol*SQ_SIZE , move.endRow*SQ_SIZE ,SQ_SIZE, SQ_SIZE ) , SQ_SIZE//22 )


def drawGameState(screen, gs , validMoves, sqSelected, movelog):
	drawBoard(screen) # draw squares on  board
	highlightSquares(screen, gs, validMoves, sqSelected, movelog)
	drawPieces(screen, gs.board) # draw pieces on the board
	hoverEffect()


def drawBoard(screen):
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			color = board_colors[((r+c)%2)]
			rect = p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)
			p.draw.rect(screen,color,rect)

def hoverEffect():
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			rect = p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)
			if rect.collidepoint(p.mouse.get_pos()):
				p.draw.rect(screen, "black", rect, SQ_SIZE//22)


def drawPieces(screen, board):
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			if board[r][c] != "--": #piece is not empty
				piece = board[r][c]
				screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animateMove(move, screen, board, clock):
	dR = move.endRow - move.startRow
	dC = move.endCol - move.startCol
	frameCount = 20
	for frame in range(frameCount + 1):
		r, c = (move.startRow + dR*frame/frameCount , move.startCol + dC*frame/frameCount )
		# print("r= ",r , " c=", c)
		drawBoard(screen)
		drawPieces(screen, board)
		# erase the piece moved from its ending square
		color = board_colors[(move.endRow + move.endCol)%2];
		endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
		p.draw.rect(screen, color, endSquare)
		# draw captured piece onto rectangle
		if move.pieceCaptured != '--':
			screen.blit( IMAGES[move.pieceCaptured] , endSquare )
		# draw moving pieces
		screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
		p.display.flip()
		clock.tick(60)

		
if __name__ == "__main__":
	p.init()
	screen = p.display.set_mode((WIDTH,HEIGHT))
	clock = p.time.Clock()
	screen.fill(p.Color("white"))
	whiteIsHuman = True 
	blackIsHuman = True
	userChoice = displayMenuAndGetChoiceFromUser()
	p.display.set_caption("CHESS BOARD : Press Z for UNDO the move and R for RESET the board")
	print("User Choice" , userChoice)
	if userChoice[0] == 0:
		runMultiplayerMode()
	elif userChoice[0] == 1:
		if userChoice[1] == 0:
			blackIsHuman = False
		elif userChoice[1] == 1:
			whiteIsHuman = False
		runComputerMode()