import pygame
from UsefulClasses import MyGameGrid
##############################################################################
# CLASSES
##############################################################################
class BackgammonGameGrid(MyGameGrid):

    def __init__(self,newRows,newCols,newListOfAllowedCellItems,newPosOfBlankItem):
        super().__init__(newRows,newCols,newListOfAllowedCellItems,newPosOfBlankItem) 
        self._player1PiecesOnSide = 0
        self._player2PiecesOnSide = 0


    def AddSidePiece(self,someSide):
        if(someSide == 1):
            self._player1PiecesOnSide = self._player1PiecesOnSide + 1
        else:
            self._player2PiecesOnSide = self._player2PiecesOnSide + 1

    def ResetSidePieces(self):
        self._player1PiecesOnSide = 0
        self._player2PiecesOnSide = 0
        
    
    def RemoveSidePiece(self,someSide):
        if(someSide == 1):
            self._player1PiecesOnSide = self._player1PiecesOnSide - 1
        else:
            self._player2PiecesOnSide = self._player2PiecesOnSide - 1

    def AddSidePieceNum(self,someSide):
        if(someSide == 1):
            return self._player1PiecesOnSide
        else:
            return self._player2PiecesOnSide
      
    def DebugPrintSelf(self):
        super().DebugPrintSelf()
        print("player 1 : side pieces",self._player1PiecesOnSide)
        print("player 2 : side pieces",self._player2PiecesOnSide)

class Piece(pygame.sprite.Sprite): 
    def __init__(self, newImage, newPos,newParentSurface,newPlayer): 
        super().__init__() 

        self._image = newImage
        self._pos = newPos
        self._rect = self._image.get_rect()
        self._rect.topleft=(newPos[0],newPos[1])
        self._parentSurface = newParentSurface
        self._player = newPlayer
        self._king = False

    def DrawSelf(self):
        self._parentSurface.blit(self._image, (self._pos[0], self._pos[1]))
        if(self._king):
            pygame.draw.rect(self._parentSurface, (255,0,0), pygame.Rect(self._pos[0]+17, self._pos[1]+17, 10, 10))

    def SetPos(self,newPos):
        self._pos = newPos
        self._rect.topleft=(newPos[0],newPos[1])

    def GetPos(self):
        return self._pos
    
    def ClickedOnMe(self,clickPos):
        if(self._rect.collidepoint(clickPos)):
            return True
        else:
            return False

