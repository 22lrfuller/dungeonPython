from sys import exit as endGame
from random import randint as randNum
from pygame.locals import *
import pygame
import sys
pygame.init()

global white, grey, red, yellow, green, blue
global randDoor, randBlock

# Board size constants
xSize = 12
ySize = 8
# Maximum index for board coordinates
xMax = xSize - 1
yMax = ySize - 1
# Non-Color Variables
displayWidth = xSize*100
displayHeight = (ySize+1)*100
xBox = 0
yBox = 0
scene = 'startPage'
gameOver = False
imageType = None
firstTime = True
randBlock = randNum(1,10)
gameBoard = []
entrancePos = []
posPath = []

# Images
startScreen = pygame.transform.scale(pygame.image.load('gameArt/startScreen.png'),(1000,1000))
playerImg = pygame.transform.scale(pygame.image.load('gameArt/pixelChar.png'), (75, 75))

path = pygame.transform.scale(pygame.image.load('gameArt/path.png'), (100,100))
crackedPath = pygame.transform.scale(pygame.image.load('gameArt/cracked.path.png'), (100,100))
flowerPath = pygame.transform.scale(pygame.image.load('gameArt/flower.path.png'), (100,100))
crackedFlowerPath = pygame.transform.scale(pygame.image.load('gameArt/crackedFlower.path.png'),(100,100))
aBlock = pygame.transform.scale(pygame.image.load('gameArt/aBlock.png'),(100,100))
flowerABlock = pygame.transform.scale(pygame.image.load('gameArt/flower.aBlock.png'),(100,100))
wall = pygame.transform.scale(pygame.image.load('gameArt/wall.png'),(100,100))
crackedWall = pygame.transform.scale(pygame.image.load('gameArt/cracked.wall.png'),(100,100))
door = pygame.transform.scale(pygame.image.load('gameArt/door.png'),(100,100))
flowerDoor = pygame.transform.scale(pygame.image.load('gameArt/flower.door.png'),(100,100))

# Colors
white = (255, 255, 255)
grey = (125, 125, 125)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 210, 0)
blue = (0, 125, 255)

def printBoard():
	column_width = 16
	print("     ", end="")
	for x in range(xSize):
		print("x={}".format(x).ljust(column_width), end="")
	sys.stdout.write("\n")
	for y in range(ySize):
		print("y={} (".format(y), end="")
		for x in range(xSize):
			    print("{}".format(gameBoard[y][x]).ljust(column_width), end="")
		print(")")

def getBlockType(blockX, blockY, blockKind): # Defining blocks in the grid
	global entrancePos
	if(blockKind == 'origPath'):
		randBlock = randNum(1,5)
		if(randBlock <= 4): return 'path'
		return 'actionBlock'
	if(blockKind == 'other'):
		if(blockX == 0 or blockX == xMax or blockY == 0 or blockY == yMax):
			if(blockY == yMax and randDoor == blockX):
				entrancePos = [randDoor,blockY]
				return 'entrance'
			return 'border'
		randBlock = randNum(1,25)
		if(randBlock <= 9): return 'path'
		if(randBlock > 9 and randBlock < 24): return 'wall'
		return 'actionBlock'

def getArt(blockKind): # Gets the Random Art for that type
	if(blockKind == 'path'):
		randomVar = randNum(1,4)
		if(randomVar == 1): return 'path'
		if(randomVar == 2): return 'cracked.path'
		if(randomVar == 3): return 'flower.path'
		if(randomVar == 4): return 'crackedFlower.path'
	if(blockKind == 'actionBlock'):
		randomVar = randNum(1,2)
		if(randomVar == 1): return 'aBlock'
		if(randomVar == 2): return 'flower.aBlock'
	if(blockKind == 'wall' or blockKind == 'border'):
		randomVar = randNum(1,2)
		if(randomVar == 1): return 'wall'
		if(randomVar == 2): return 'cracked.wall'
	if(blockKind == 'entrance' or blockKind == 'exit'):
		randVar = randNum(1,2)
		if(randVar == 1): return 'door'
		if(randVar == 2): return 'flower.door'

def getDir(entrancePos): # Creating the random path
	global posPath
	blockX = entrancePos[0]
	blockY = entrancePos[1]
	print(int(round(xSize/2.0)))
	while(blockY-1 != 0):
		randomVar = randNum(1,3)
		if blockX+1 > xMax:
			import pdb; pdb.set_trace()
		if(randomVar == 1 and gameBoard[blockY][blockX-1][0] != 'border'): # Left
			blockX -= 1
		if(randomVar == 2 and gameBoard[blockY-1][blockX][0] != 'border'): # Up
			blockY -= 1
		if(randomVar == 3 and gameBoard[blockY][blockX+1][0] != 'border'): # Right
			blockX += 1
		while(blockY-1 == 0 and blockX < int(round((xSize-1)/2.0))):
			blockX += 1
			posPath.append([blockX, blockY])
		posPath.append([blockX, blockY])
	exitPos = [blockX, blockY-1]
	for i in range(len(posPath)):
		gameBoard[posPath[i][1]][posPath[i][0]] = [getBlockType(posPath[i][0],posPath[i][1],'origPath')]
	gameBoard[exitPos[1]][exitPos[0]] = ['exit']

def keyUp(event, funcX, funcY): # Start Movement on Key Down
	if(event.key == K_UP or event.key == K_w):
		if(funcY-1 >= 0 and funcY-1 <= yMax):
			if(gameBoard[funcY-1][funcX][0] != 'wall' and gameBoard[funcY-1][funcX][0] != 'border'):
				funcY -= 1
	elif(event.key == K_DOWN or event.key == K_s):
		if(funcY+1 >= 0 and funcY+1 <= yMax):
			if(gameBoard[funcY+1][funcX][0] != 'wall' and gameBoard[funcY+1][funcX][0] != 'border'):
				funcY += 1
	elif(event.key == K_LEFT or event.key == K_a):
		if(funcX-1 >= 0 and funcX-1 <= xMax):
			if(gameBoard[funcY][funcX-1][0] != 'wall' and gameBoard[funcY][funcX-1][0] != 'border'):
				funcX -= 1
	elif(event.key == K_RIGHT or event.key == K_d):
		if(funcX+1 >= 0 and funcX+1 <= xMax):
			if(gameBoard[funcY][funcX+1][0] != 'wall' and gameBoard[funcY][funcX+1][0] != 'border'):
				funcX += 1
	return funcX, funcY

# Creating the game board in a row-major format
# Everything will be referenced [y][x] in the array
gameBoard = [[[''] for x in range(xSize)] for y in range(ySize)]
for loopY in range(ySize):
	randDoor = randNum(1,int(round((xSize-1)/4.0)))
	for loopX in range(xSize):
		blockType = getBlockType(loopX,loopY,'other')
		gameBoard[loopY][loopX][0] = blockType

getDir(entrancePos) #Generates Random Path
# printBoard()

# Making art for the game after the path is generated
for loopY in range(0,ySize):
	for loopX in range(0,xSize):
		if(loopX == entrancePos[0] and loopY == entrancePos[1]):
			art = getArt('entrance')
		else:
			art = getArt(gameBoard[loopY][loopX][0])
		gameBoard[loopY][loopX].append(art)

xBox, yBox = entrancePos # Sets the player's position

# Creates the pygame screen
screen = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Dungeon Game')
clock = pygame.time.Clock()

startButton = pygame.draw.rect(screen, blue,(400,700,200,100))

# Main Game Loop
while(gameOver == False):
	for event in pygame.event.get():
		if(event.type == pygame.MOUSEBUTTONDOWN):
			mousePos = pygame.mouse.get_pos()
			if(startButton.collidepoint(mousePos)):
				scene = 'game'
		if(event.type == pygame.KEYUP and scene == 'game'):
			xBox, yBox = keyUp(event, xBox, yBox)
		if(event.type == pygame.QUIT):
			gameOver = True
	screen.fill(white)
	if(scene == 'startPage'): # Prints the start screen
		screen.blit(startScreen,(0,0))
		startButton = pygame.draw.rect(screen, blue,(400,700,200,100))
		screen.blit(pygame.font.SysFont('calibri', 30).render('Start', False, red),(400,700))
	elif(scene == 'game'): # Prints the two-dimensional array to the screen
		for y in range(len(gameBoard)):
			for x in range(len(gameBoard[y])):
				screen.blit(pygame.transform.scale(pygame.image.load('gameArt/' + str(gameBoard[y][x][1]) + '.png'),(100,100)),(x*100, y*100))
		screen.blit(pygame.transform.scale(pygame.image.load('gameArt/invBG.png'),(1200,100)),(0,800))
		# for i in range(xSize-1): #TODO add to the inventory
			# if(i != 0 or i != xSize-1):

		screen.blit(playerImg,(xBox*100+12, yBox*100+12))

	pygame.display.update()
	clock.tick(60)
endGame()
