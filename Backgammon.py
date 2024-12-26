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

from BackgammonClasses import Piece

##############################################################################
# VARIABLES
##############################################################################

#CREATE THE EMPTY GAME GRID OBJECT
EMPTY_SQUARE = 0
BLACK_PIECE = 1
WHITE_PIECE = 2
GAMECOLS = 16
GAMEROWS = 20
PIECESIZE = 25
theGameGrid = MyGameGrid(GAMECOLS,GAMECOLS,[EMPTY_SQUARE,BLACK_PIECE,WHITE_PIECE],0)

RIGHT_MOUSE_BUTTON = 3

DEBUG_ON = False

GRID_SIZE_X = 41
GRID_SIZE_Y = 28
TOP_LEFT = (33,40)

SCREEN_WIDTH = 678
SCREEN_HEIGHT = 645

BUTTON_X_VALUE = 587
BUTTON_Y_VALUE  = 614

gridLinesOn = False

GAME_TIME_X = 2
GAME_TIME_Y = BUTTON_Y_VALUE + 5

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#surface.set_colorkey((255, 255, 255))  #White background sprites should now be transparent background!
pygame.display.set_caption('Draughts - Mark Reed (c) 2024')

COL_BLACK = (0,0,0)
COL_WHITE = (255,255,255)
COL_GREEN = (0,255,0)
BACK_FILL_COLOUR = COL_WHITE

backImageName = "./images/backgroundGrid.jpg"
undoImageName = "./images/Undo.jpg"
undoImageGreyName = "./images/UndoGrey.jpg"
muteImageName = "./images/Mute.jpg"
muteImageGreyName = "./images/MuteGrey.jpg"
infoImageName = "./images/Info.jpg"
infoImageGreyName = "./images/InfoGrey.jpg"
rollImageName = "./images/Roll.jpg"
rollImageGreyName = "./images/RollGrey.jpg"

player1PieceImageName = "./images/player1Piece.png"
player2PieceImageName = "./images/player2Piece.png"

#dice
dice1ImageName = "./images/dice1.jpg"
dice2ImageName = "./images/dice2.jpg"
dice3ImageName = "./images/dice3.jpg"
dice4ImageName = "./images/dice4.jpg"
dice5ImageName = "./images/dice5.jpg"
dice6ImageName = "./images/dice6.jpg"

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

gameTime = 0
gameTimeSurface = my_font.render("Time elapsed : {}".format(gameTime), False, (0, 0, 0))
DELAY_1 = 1
myOneSecondTimer = None
if(myOneSecondTimer == None):
    myOneSecondTimer = perpetualTimer(DELAY_1,OneSecondCallback)
    myOneSecondTimer.start()

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
 
    backImage = pygame.image.load(backImageName).convert()

    #Load an image with a white background and set the white to transparent.
    #Will only work if the background is all properly white 255,255,255
    player1PieceImage = pygame.image.load(player1PieceImageName)
    player1PieceImage = pygame.transform.scale(player1PieceImage, (PIECESIZE, PIECESIZE))  #change size first before doing alpha things
    player1PieceImage.set_colorkey((255,255,255))
    player1PieceImage.convert_alpha()

    player2PieceImage = pygame.image.load(player2PieceImageName)
    player2PieceImage = pygame.transform.scale(player2PieceImage, (PIECESIZE, PIECESIZE))  #change size first before doing alpha things
    player2PieceImage.set_colorkey((255,255,255))
    player2PieceImage.convert_alpha()
    
    undoImage = pygame.image.load(undoImageName).convert()
    undoGreyImage = pygame.image.load(undoImageGreyName).convert()
    muteImage = pygame.image.load(muteImageName).convert()
    muteGreyImage = pygame.image.load(muteImageGreyName).convert()
    infoImage = pygame.image.load(infoImageName).convert()
    infoGreyImage = pygame.image.load(infoImageGreyName).convert()
    rollImage = pygame.image.load(rollImageName).convert()
    rollGreyImage = pygame.image.load(rollImageGreyName).convert()

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

    return col,row

def HandleInput(running):
    
    global waitingForYesNo,draggingPiece

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            currentMousePos = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_MOUSE_BUTTON:
                #print ("You pressed the right mouse button")
                for piece in allPieces:
                    if(piece.ClickedOnMe(currentMousePos)):
                        piece._king = not piece._king
            else:
                #did we click on a piece?
                for piece in allPieces:
                    if(piece.ClickedOnMe(currentMousePos)):
                        draggingPiece = piece
                        #The last piece in the allpieces list is draw last, so move the dragged one to last
                        #in the list to make it draw on top of every other piece as you drag it...simples!
                        allPieces.remove(draggingPiece)
                        allPieces.append(draggingPiece)

           
        elif event.type == pygame.MOUSEBUTTONUP:
            currentMousePos = pygame.mouse.get_pos()
            currentSquare = WhatSquareAreWeIn(currentMousePos)
            #print("Square dropped in : ", currentSquare)

            #Let go of a piece if we have one
            if(draggingPiece != None):
                pygame.mixer.Sound.play(clickSound)
                dropLocation = [TOP_LEFT[0] + currentSquare[0]*GRID_SIZE_X+7,TOP_LEFT[1] + currentSquare[1]*GRID_SIZE_Y+2]
                draggingPiece.SetPos(dropLocation)
                draggingPiece = None
                  
    return running

def UndoButtonCallback():
    print("undo pressed...")

    #Use a TKINTER message box :)
    #Turn events off and then back on to stop pygame picking up the mouse click too!
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP) 
    answer = messagebox.askyesno("Question","Do you really to reset the whole game?")
    if(answer):
        PutPiecesInTheStartPositions()
    pygame.event.set_allowed(None)

    
def RollButtonCallback():
    SetRandomDiceAngleAndPos()
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
        for i in range(GAMECOLS):
            pygame.draw.line(surface,COL_GREEN,(TOP_LEFT[0]+i*GRID_SIZE_X, TOP_LEFT[1]),(TOP_LEFT[0]+i*GRID_SIZE_X, TOP_LEFT[1] + (GAMEROWS-1)*GRID_SIZE_Y),width)
        for i in range(GAMEROWS):
            pygame.draw.line(surface,COL_GREEN,(TOP_LEFT[0], TOP_LEFT[1]+i*GRID_SIZE_Y),(TOP_LEFT[0]+(GAMECOLS-1)*GRID_SIZE_X, TOP_LEFT[1]+i*GRID_SIZE_Y),width)

def PutPiecesInTheStartPositions():
    global allPieces
    allPieces = []

    for i in range(5):
        someGamePiece = Piece(player2PieceImage,[TOP_LEFT[0]+7, TOP_LEFT[1] + (i)*GRID_SIZE_Y+2],surface)
        allPieces.append(someGamePiece)
    for i in range(2):
        someGamePiece = Piece(player2PieceImage,[TOP_LEFT[0]+14*GRID_SIZE_X+7, TOP_LEFT[1] + (i)*GRID_SIZE_Y+2],surface)
        allPieces.append(someGamePiece)
    for i in range(3):
        someGamePiece = Piece(player2PieceImage,[TOP_LEFT[0]+4*GRID_SIZE_X+7, TOP_LEFT[1] + (i+16)*GRID_SIZE_Y+2],surface)
        allPieces.append(someGamePiece)
    for i in range(5):
        someGamePiece = Piece(player2PieceImage,[TOP_LEFT[0]+9*GRID_SIZE_X+7, TOP_LEFT[1] + (i+14)*GRID_SIZE_Y+2],surface)
        allPieces.append(someGamePiece)

    for i in range(3):
        someGamePiece = Piece(player1PieceImage,[TOP_LEFT[0]+4*GRID_SIZE_X+7, TOP_LEFT[1] + (i)*GRID_SIZE_Y+2],surface)
        allPieces.append(someGamePiece)

    for i in range(5):
        someGamePiece = Piece(player1PieceImage,[TOP_LEFT[0]+9*GRID_SIZE_X+7, TOP_LEFT[1] + (i)*GRID_SIZE_Y+2],surface)
        allPieces.append(someGamePiece)

    for i in range(5):
        someGamePiece = Piece(player1PieceImage,[TOP_LEFT[0]+7, TOP_LEFT[1] + (i+14)*GRID_SIZE_Y+2],surface)
        allPieces.append(someGamePiece)

    for i in range(2):
        someGamePiece = Piece(player1PieceImage,[TOP_LEFT[0]+14*GRID_SIZE_X+7, TOP_LEFT[1] + (i+17)*GRID_SIZE_Y+2],surface)
        allPieces.append(someGamePiece)
    
    

   
    
    

##############################################################################
# MAIN
##############################################################################
pygame.init()

LoadImages()

SetRandomDiceAngleAndPos()

theUndoButton = MyClickableImageButton(BUTTON_X_VALUE + 30*2,BUTTON_Y_VALUE,undoImage,undoGreyImage,surface,UndoButtonCallback)
theMuteButton = MyClickableImageButton(BUTTON_X_VALUE + 30,BUTTON_Y_VALUE,muteImage,muteGreyImage,surface,MuteButtonCallback)
theInfoButton = MyClickableImageButton(BUTTON_X_VALUE,BUTTON_Y_VALUE,infoImage,infoGreyImage,surface,InfoButtonCallback)
theRollButton = MyClickableImageButton(302,BUTTON_Y_VALUE,rollImage,rollGreyImage,surface,RollButtonCallback)

allPieces = []
PutPiecesInTheStartPositions()

#game loop
while running:
    # Fill the scree with white color - "blank it"
    surface.fill(BACK_FILL_COLOUR)

    # Using blit to copy the background grid onto the blank screen
    surface.blit(backImage, (1, 1))

    DrawGreenLinesOverTheBoard(3)

    theUndoButton.DrawSelf()
    theMuteButton.DrawSelf()
    theInfoButton.DrawSelf()
    theRollButton.DrawSelf()

    running = HandleInput(running)

    #Draw the dice
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