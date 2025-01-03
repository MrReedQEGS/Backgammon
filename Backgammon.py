##############################################################################
# DETAILS
#  A good template for a grid game of some kind
#  Mr Reed - Dec 2024
#
#  Sounds 
#  https://pixabay.com/sound-effects/search/clicks/
#  https://audiotrimmer.com/
#
#  Music
#  https://pixabay.com/music/search/relaxing%20game%20music/
#
##############################################################################

##############################################################################
# IMPORTS
##############################################################################
import pygame, random, time
from pygame.locals import *
from UsefulClasses import perpetualTimer,MyGameGrid,MyClickableImageButton

import tkinter
from tkinter import messagebox

from BackgammonClasses import Piece,BackgammonGameGrid

##############################################################################
# VARIABLES
##############################################################################

APP_NAME = "Backgammon"
COPYRIGHT_MESSAGE = "Mark Reed (c) 2024"
WINDOW_TEXT = APP_NAME + " - " + COPYRIGHT_MESSAGE

PIECESIZE = 25

RIGHT_MOUSE_BUTTON = 3

DEBUG_ON = False

GRID_SIZE_X = 41
GRID_SIZE_Y = 28
TOP_LEFT = (33,40)

SCREEN_WIDTH = 678
SCREEN_HEIGHT = 645

BUTTON_X_VALUE = 557
BUTTON_Y_VALUE  = 614

GAMECOLS = 15
GAMEROWS = 19
EMPTY_SQUARE = 0
PLAYER1 = 1
PLAYER2 = 2
theGameGrid = BackgammonGameGrid(GAMEROWS,GAMECOLS,[EMPTY_SQUARE,PLAYER1,PLAYER2],0)

PLAYER_SIDE_PIECE_HEIGHT = 8
#player1PiecesOnSide = 0
PLAYER1_SIDE_PIECE_X = 352
PLAYER1_SIDE_PIECE_Y = 358
#player2PiecesOnSide = 0
PLAYER2_SIDE_PIECE_X = 298

gridLinesOn = False

GAME_TIME_X = 2
GAME_TIME_Y = BUTTON_Y_VALUE + 5

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#surface.set_colorkey((255, 255, 255))  #White background sprites should now be transparent background!
pygame.display.set_caption(WINDOW_TEXT)

COL_BLACK = (0,0,0)
COL_WHITE = (255,255,255)
COL_GREEN = (0,255,0)
BACK_FILL_COLOUR = COL_WHITE

backImageName = "./images/backgroundGrid.jpg"
undoImageName = "./images/Undo.jpg"
undoImageGreyName = "./images/UndoGrey.jpg"
muteImageName = "./images/Mute.jpg"
muteImageGreyName = "./images/MuteGrey.jpg"
infoImageName = "./images/Eye.jpg"
infoImageGreyName = "./images/EyeGrey.jpg"
rollImageName = "./images/Roll.jpg"
rollImageGreyName = "./images/RollGrey.jpg"
restartImageName = "./images/Restart.jpg"
restartImageGreyName = "./images/RestartGrey.jpg"

player1PieceImageName = "./images/player1Piece.png"
player1SidePieceImageName = "./images/player1PieceSide.png"
player2PieceImageName = "./images/player2Piece.png"
player2SidePieceImageName = "./images/player2PieceSide.png"

#dice
dice1ImageName = "./images/dice1.jpg"
dice2ImageName = "./images/dice2.jpg"
dice3ImageName = "./images/dice3.jpg"
dice4ImageName = "./images/dice4.jpg"
dice5ImageName = "./images/dice5.jpg"
dice6ImageName = "./images/dice6.jpg"

diceRolling = False

PIECE_SIZE = 20
draggingPiece = None

#sounds
pygame.mixer.init()
clickSound = pygame.mixer.Sound("./sounds/click.mp3")
rollSound = pygame.mixer.Sound("./sounds/dicerollshort.mp3")
pygame.mixer.music.load("./sounds/relaxing-music.mp3") 

musicOn = False
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.pause()

#fonts
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 16)

running = True

turn = COL_BLACK

#Timer callbacks
def OneSecondCallback():
    #Update game time
    global gameTime
    gameTime = gameTime + 1

def DiceCallback():
    global diceRolling
    myDiceTimer.Stop()
    diceRolling = False  #Turn of dice animation

gameTime = 0
gameTimeSurface = my_font.render("Time elapsed : {}".format(gameTime), False, (0, 0, 0))
DELAY_1 = 1
myOneSecondTimer = None
if(myOneSecondTimer == None):
    myOneSecondTimer = perpetualTimer(DELAY_1,OneSecondCallback)
    myOneSecondTimer.thread.daemon = True
    myOneSecondTimer.start()

#Dice callback timer
DELAY_DICE = 0.5
myDiceTimer = None

##############################################################################
# SUB PROGRAMS
##############################################################################

def SetRandomDiceAngleAndPos():

    global firstDiceX,firstDiceY,secondDiceX,secondDiceY,firstDiceAngle,secondDiceAngle,currentFirstDiceImage,currentSecondDiceImage

    firstDiceX = random.randint(315,335)
    firstDiceY = random.randint(410,440)
    secondDiceX = random.randint(315,335)
    secondDiceY = random.randint(490,510)
    firstDiceAngle = random.randint(0,180)
    secondDiceAngle = random.randint(0,180)

    currentFirstDiceImage = random.choice(diceList)
    currentSecondDiceImage = random.choice(diceList)

def TurnOffTimers():
        
    global myOneSecondTimer
    if(myOneSecondTimer!=None):
        myOneSecondTimer.cancel()
        myOneSecondTimer = None
        if(DEBUG_ON):
            print("Turnning off timer...myOneSecondTimer")

def LoadImages():
    global backImage,undoImage,undoGreyImage,muteImage,muteGreyImage
    global infoImage,infoGreyImage,player1PieceImage,player2PieceImage
    global dice1Image,dice2Image,dice3Image,dice4Image,dice5Image,dice6Image
    global currentFirstDiceImage,currentSecondDiceImage,diceList,rollImage,rollGreyImage
    global player1PieceSideImage,player2PieceSideImage,restartImage,restartGreyImage
 
    backImage = pygame.image.load(backImageName).convert()

    #Load an image with a white background and set the white to transparent.
    #Will only work if the background is all properly white 255,255,255
    player1PieceImage = pygame.image.load(player1PieceImageName)
    player1PieceImage = pygame.transform.scale(player1PieceImage, (PIECESIZE, PIECESIZE))  #change size first before doing alpha things
    player1PieceImage.set_colorkey((255,255,255))
    player1PieceImage.convert_alpha()

    player1PieceSideImage = pygame.image.load(player1SidePieceImageName)
    player1PieceSideImage = pygame.transform.scale(player1PieceSideImage, (28, PLAYER_SIDE_PIECE_HEIGHT))  #change size first before doing alpha things
    player1PieceSideImage.set_colorkey((255,255,255))
    player1PieceSideImage.convert_alpha()

    player2PieceImage = pygame.image.load(player2PieceImageName)
    player2PieceImage = pygame.transform.scale(player2PieceImage, (PIECESIZE, PIECESIZE))  #change size first before doing alpha things
    player2PieceImage.set_colorkey((255,255,255))
    player2PieceImage.convert_alpha()

    player2PieceSideImage = pygame.image.load(player2SidePieceImageName)
    player2PieceSideImage = pygame.transform.scale(player2PieceSideImage, (28, PLAYER_SIDE_PIECE_HEIGHT))  #change size first before doing alpha things
    player2PieceSideImage.set_colorkey((255,255,255))
    player2PieceSideImage.convert_alpha()
      
    undoImage = pygame.image.load(undoImageName).convert()
    undoGreyImage = pygame.image.load(undoImageGreyName).convert()
    muteImage = pygame.image.load(muteImageName).convert()
    muteGreyImage = pygame.image.load(muteImageGreyName).convert()
    infoImage = pygame.image.load(infoImageName).convert()
    infoGreyImage = pygame.image.load(infoImageGreyName).convert()
    rollImage = pygame.image.load(rollImageName).convert()
    rollGreyImage = pygame.image.load(rollImageGreyName).convert()
    restartImage = pygame.image.load(restartImageName).convert()
    restartGreyImage = pygame.image.load(restartImageGreyName).convert()
    
    #dice time!
    dice1Image = pygame.image.load(dice1ImageName).convert_alpha()
    dice2Image = pygame.image.load(dice2ImageName).convert_alpha()
    dice3Image = pygame.image.load(dice3ImageName).convert_alpha()
    dice4Image = pygame.image.load(dice4ImageName).convert_alpha()
    dice5Image = pygame.image.load(dice5ImageName).convert_alpha()
    dice6Image = pygame.image.load(dice6ImageName).convert_alpha()

    diceList = [dice1Image,dice2Image,dice3Image,dice4Image,dice5Image,dice6Image]

    currentFirstDiceImage = dice1Image
    currentSecondDiceImage = dice2Image
        
def WhatSquareAreWeIn(aPosition):
    #Find out what square somebody clicked on.
    #For example, if we click top left the the answer is row 1 col 1  (aka  "a1")
    currentClickX = aPosition[0]
    currentClickY = aPosition[1]
   
    adjustedX = currentClickX-TOP_LEFT[0]
    col = adjustedX//(GRID_SIZE_X+1) #The +1 in the brackets seems to fix the identifcation of col 6 to 7 which was a bit out?
   
    adjustedY = currentClickY-TOP_LEFT[1]
    row = adjustedY//(GRID_SIZE_Y)
   
    if DEBUG_ON:
        print("Current x = {}\nCurrrent y = {}".format(currentClickX,currentClickY))
        print("Col  =  {}".format(col))
        print("row  =  {}".format(row))

    if(row > GAMEROWS):
        row = GAMEROWS
    if(row < 0):
        row = 0
    if(col > GAMECOLS):
        col = GAMECOLS
    if(col < 0):
        col = 0

    return col,row

def HandleInput(running):
    
    global draggingPiece

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            currentMousePos = pygame.mouse.get_pos()

            #did we click on the "side area"?
            #If so then remove a piece from the side area and put it on the mouse cursor ready to drop
                #if it is a black piece the check we are not trying to put it on its side
            if(currentMousePos[0]>=350 and currentMousePos[0]<=380 and
            currentMousePos[1] >= 205 and  currentMousePos[1] <= 370):
                if(theGameGrid.AddSidePieceNum(1) > 0):
                    theGameGrid.RemoveSidePiece(1)

                    someGamePiece = Piece(player1PieceImage,[TOP_LEFT[0]+7, TOP_LEFT[1] + (i)*GRID_SIZE_Y+2],surface,PLAYER1)
                    allPieces.append(someGamePiece)
                    draggingPiece = someGamePiece
            elif(currentMousePos[0]>=296 and currentMousePos[0]<=327 and
            currentMousePos[1] >= 205 and  currentMousePos[1] <= 370):
                if(theGameGrid.AddSidePieceNum(2) > 0):
                    theGameGrid.RemoveSidePiece(2)

                    someGamePiece = Piece(player2PieceImage,[TOP_LEFT[0]+7, TOP_LEFT[1] + (i)*GRID_SIZE_Y+2],surface,PLAYER2)
                    allPieces.append(someGamePiece)
                    draggingPiece = someGamePiece
                
            else:

                #did we click on a piece?
                for piece in allPieces:
                    if(piece.ClickedOnMe(currentMousePos)):
                        draggingPiece = piece
                        #The last piece in the allpieces list is draw last, so move the dragged one to last
                        #in the list to make it draw on top of every other piece as you drag it...simples!
                        allPieces.remove(draggingPiece)
                        allPieces.append(draggingPiece)

                        #Remove the piece from the game grid and replace it with a zero...
                        currentSquare = WhatSquareAreWeIn(currentMousePos)
                        theGameGrid.SetGridItem(currentSquare,EMPTY_SQUARE)           

        elif event.type == pygame.MOUSEBUTTONUP:
            currentMousePos = pygame.mouse.get_pos()
            currentSquare = WhatSquareAreWeIn(currentMousePos)
            #print("Square dropped in : ", currentSquare)

            #Let go of a piece if we have one
            if(draggingPiece != None):
                
                #if it is a black piece the check we are not trying to put it on its side
                if(currentMousePos[0]>=286 and currentMousePos[0]<=410 and
                currentMousePos[1] >= 205 and  currentMousePos[1] <= 370):
                    theGameGrid.AddSidePiece(draggingPiece._player)
                    allPieces.remove(draggingPiece)

                else:
                    #We are dropping it on the board.  If it is on a column then it should go at the base of that column!

                    dropLocation = [TOP_LEFT[0] + currentSquare[0]*GRID_SIZE_X+7,TOP_LEFT[1]+ currentSquare[1]*GRID_SIZE_Y+2]
                    draggingPiece.SetPos(dropLocation)
                    
                
                    theGameGrid.SetGridItem(currentSquare,draggingPiece._player)

                pygame.mixer.Sound.play(clickSound)
                draggingPiece = None

            theGameGrid.DebugPrintSelf()
                  
    return running

def UndoButtonCallback():
    print("undo pressed...")

def restartButtonCallback():
    #Use a TKINTER message box :)
    #Turn events off and then back on to stop pygame picking up the mouse click too!
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP) 
    answer = messagebox.askyesno("Question","Do you really to reset the whole game?")
    if(answer):
        PutPiecesInTheStartPositions()
    pygame.event.set_allowed(None)

    
def RollButtonCallback():
    global diceRolling,myDiceTimer
    myDiceTimer = perpetualTimer(DELAY_DICE,DiceCallback)
    myDiceTimer.thread.daemon = True
    myDiceTimer.start()
    diceRolling = True
    pygame.mixer.Sound.play(rollSound)

def MuteButtonCallback():
    global musicOn
    if(musicOn):
        musicOn = False
        pygame.mixer.music.pause()
    else:
        musicOn = True
        pygame.mixer.music.unpause()
            
def InfoButtonCallback():
    global gridLinesOn
    gridLinesOn = not gridLinesOn

def DrawGreenLinesOverTheBoard(width): 
    
    if(gridLinesOn):
        for i in range(GAMECOLS+1):
            pygame.draw.line(surface,COL_GREEN,(TOP_LEFT[0]+i*GRID_SIZE_X, TOP_LEFT[1]),(TOP_LEFT[0]+i*GRID_SIZE_X, TOP_LEFT[1] + (GAMEROWS)*GRID_SIZE_Y),width)
        for i in range(GAMEROWS+1):
            pygame.draw.line(surface,COL_GREEN,(TOP_LEFT[0], TOP_LEFT[1]+i*GRID_SIZE_Y),(TOP_LEFT[0]+(GAMECOLS)*GRID_SIZE_X, TOP_LEFT[1]+i*GRID_SIZE_Y),width)

def PutPiecesInTheStartPositions():
    global allPieces
    allPieces = []

    theGameGrid.ResetSidePieces()
    theGameGrid.BlankTheGrid()

    for i in range(5):
        someGamePiece = Piece(player2PieceImage,[TOP_LEFT[0]+7, TOP_LEFT[1] + (i)*GRID_SIZE_Y+2],surface,PLAYER2)
        allPieces.append(someGamePiece)
        theGameGrid.SetGridItem((0,i),PLAYER2)

    for i in range(2):
        someGamePiece = Piece(player2PieceImage,[TOP_LEFT[0]+14*GRID_SIZE_X+7, TOP_LEFT[1] + (i)*GRID_SIZE_Y+2],surface,PLAYER2)
        allPieces.append(someGamePiece)
        theGameGrid.SetGridItem((14,i),PLAYER2)

    for i in range(3):
        someGamePiece = Piece(player2PieceImage,[TOP_LEFT[0]+4*GRID_SIZE_X+7, TOP_LEFT[1] + (i+16)*GRID_SIZE_Y+2],surface,PLAYER2)
        allPieces.append(someGamePiece)
        theGameGrid.SetGridItem((4,i+16),PLAYER2)

    for i in range(5):
        someGamePiece = Piece(player2PieceImage,[TOP_LEFT[0]+9*GRID_SIZE_X+7, TOP_LEFT[1] + (i+14)*GRID_SIZE_Y+2],surface,PLAYER2)
        allPieces.append(someGamePiece)
        theGameGrid.SetGridItem((9,i+14),PLAYER2)

    for i in range(3):
        someGamePiece = Piece(player1PieceImage,[TOP_LEFT[0]+4*GRID_SIZE_X+7, TOP_LEFT[1] + (i)*GRID_SIZE_Y+2],surface,PLAYER1)
        allPieces.append(someGamePiece)
        theGameGrid.SetGridItem((4,i),PLAYER1)

    for i in range(5):
        someGamePiece = Piece(player1PieceImage,[TOP_LEFT[0]+9*GRID_SIZE_X+7, TOP_LEFT[1] + (i)*GRID_SIZE_Y+2],surface,PLAYER1)
        allPieces.append(someGamePiece)
        theGameGrid.SetGridItem((9,i),PLAYER1)

    for i in range(5):
        someGamePiece = Piece(player1PieceImage,[TOP_LEFT[0]+7, TOP_LEFT[1] + (i+14)*GRID_SIZE_Y+2],surface,PLAYER1)
        allPieces.append(someGamePiece)
        theGameGrid.SetGridItem((0,i+14),PLAYER1)

    for i in range(2):
        someGamePiece = Piece(player1PieceImage,[TOP_LEFT[0]+14*GRID_SIZE_X+7, TOP_LEFT[1] + (i+17)*GRID_SIZE_Y+2],surface,PLAYER1)
        allPieces.append(someGamePiece)
        theGameGrid.SetGridItem((14,i+17),PLAYER1)

##############################################################################
# MAIN
##############################################################################
pygame.init()

LoadImages()

SetRandomDiceAngleAndPos()

theRestartButton = MyClickableImageButton(BUTTON_X_VALUE,BUTTON_Y_VALUE,restartImage,restartGreyImage,surface,restartButtonCallback)
theInfoButton = MyClickableImageButton(BUTTON_X_VALUE+ 30,BUTTON_Y_VALUE,infoImage,infoGreyImage,surface,InfoButtonCallback)
theMuteButton = MyClickableImageButton(BUTTON_X_VALUE + 30*2,BUTTON_Y_VALUE,muteImage,muteGreyImage,surface,MuteButtonCallback)
theUndoButton = MyClickableImageButton(BUTTON_X_VALUE + 30*3,BUTTON_Y_VALUE,undoImage,undoGreyImage,surface,UndoButtonCallback)

theRollButton = MyClickableImageButton(302,BUTTON_Y_VALUE,rollImage,rollGreyImage,surface,RollButtonCallback)


restartImage

allPieces = []
PutPiecesInTheStartPositions()

#game loop
while running:
    # Fill the scree with white color - "blank it"
    surface.fill(BACK_FILL_COLOUR)

    # Using blit to copy the background grid onto the blank screen
    surface.blit(backImage, (1, 1))

    DrawGreenLinesOverTheBoard(3)

    theRestartButton.DrawSelf()
    theUndoButton.DrawSelf()
    theMuteButton.DrawSelf()
    theInfoButton.DrawSelf()
    theRollButton.DrawSelf()

    #Draw the pieces that are on their side
    for i in range(theGameGrid.AddSidePieceNum(PLAYER1)):
        surface.blit(player1PieceSideImage, (PLAYER1_SIDE_PIECE_X, PLAYER1_SIDE_PIECE_Y-i*(PLAYER_SIDE_PIECE_HEIGHT+2)))

    for i in range(theGameGrid.AddSidePieceNum(PLAYER2)):
        surface.blit(player2PieceSideImage, (PLAYER2_SIDE_PIECE_X, PLAYER1_SIDE_PIECE_Y-i*(PLAYER_SIDE_PIECE_HEIGHT+2)))

    running = HandleInput(running)

    #Draw the dice
    if(diceRolling):
        SetRandomDiceAngleAndPos()
    rotated_dice1 = pygame.transform.rotate(currentFirstDiceImage,firstDiceAngle)
    surface.blit(rotated_dice1, (firstDiceX, firstDiceY))

    rotated_dice2 = pygame.transform.rotate(currentSecondDiceImage,secondDiceAngle)
    surface.blit(rotated_dice2, (secondDiceX, secondDiceY))
       
    #We may be dragging a particular piece!
    currentMousePos = pygame.mouse.get_pos()    
    if(draggingPiece != None):  
        dragLocation = [currentMousePos[0]-GRID_SIZE_X//2,currentMousePos[1]-GRID_SIZE_Y//2]
        draggingPiece.SetPos(dragLocation)

    for piece in allPieces:
        piece.DrawSelf()
       
    if(running):
        gameTimeSurface = my_font.render("Time elapsed : {}".format(gameTime), False, (0, 0, 0))
        surface.blit(gameTimeSurface, (GAME_TIME_X,GAME_TIME_Y))
        pygame.display.flip()

TurnOffTimers()

pygame.quit()