# Imports
import sys
import pygame
from pygame.locals import KEYDOWN, K_q
import numpy as np
from time import sleep


# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 800, 600
GRIDSIZE= ROWS, COLS = 12,16
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
WHITE = (255,255,255)
# VARS:
_VARS = {'surf': False}


# functions
def main():
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    GRID = np.zeros((ROWS,COLS))
    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        drawGrid(GRID)
        pygame.display.update()
        GRID = updateGrid(GRID)
        sleep(0.01)



def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()

def updateGrid(grid):
  rows,cols = grid.shape
  
  neighboursMax=np.ones((rows,cols))*3
  neighboursMax[0,0]=2
  neighboursMax[0,cols-1]=2
  neighboursMax[rows-1,0]=2
  neighboursMax[rows-1,cols-1]=2
  neighboursMax[1:rows-1,1:cols-1]=4

  gridWithBorder=np.zeros((rows+2,cols+2))
  gridWithBorder[1:rows+1,1:cols+1]=grid

  neighbourLeft=gridWithBorder[1:rows+1,0:cols]
  neighbourRight=gridWithBorder[1:rows+1,2:cols+2]
  neighbourTop=gridWithBorder[0:rows,1:cols+1]
  neighbourBottom=gridWithBorder[2:rows+2,1:cols+1]
  neighboursCount = neighbourTop+neighbourLeft+neighbourBottom+neighbourRight

  newGrid=np.zeros((rows,cols))
  for i in range(rows):
    for j in range(cols):
      value=grid[i,j]

      denominator=neighboursMax[i,j]+1
      if value==0:
        numerator=neighboursCount[i,j]+1
      if value==1:
        numerator=neighboursCount[i,j]
      
      p = numerator / denominator
      newValue = np.random.choice([0,1],p=[p,1-p])

      newGrid[i,j]=newValue

  return newGrid

def drawRect(i,j,value):
  SIZE=20
  pygame.draw.rect(
    _VARS['surf'], 
    BLACK,
    (j*SIZE, i*SIZE, SIZE-1, SIZE-1),
    not bool(value),
  )


def drawGrid(grid):
  for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
      drawRect(i, j, grid[i,j])


if __name__ == '__main__':
    main()