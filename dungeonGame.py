import pygame
from sys import exit as endGame
from random import randint as randNum
from pygame.locals import *
from variableInit import *
pygame.init()

global randDoor, curFrame, posPath

def getBlockType(blockX, blockY, blockKind): # Defining blocks in the grid
	global entrancePos
	if (blockKind == 'origPath'):
		randBlock = randNum(1,20) # 95% chance for path, 5% for chestBlock
		if (randBlock <= 19):
			return 'path'
		return 'cBlock'
	if (blockKind == 'other'):
		if (blockX == 0 or blockX == xSize - 1 or blockY == 0 or blockY == ySize - 1):
			if (blockY == ySize - 1 and randDoor == blockX):
				entrancePos = [randDoor,blockY]
				return 'entrance'
			return 'border'
		randBlock = randNum(1,40)
		if (randBlock <= 20):
			return 'path'
		if (randBlock > 20 and randBlock < 39):
			return 'wall'
		return 'cBlock'

def getArt(blockKind): # Gets the Random Art for that type
	randomVar = randNum(1,4)
	if (blockKind == 'path'):
		if (randomVar == 1): return 'path'
		if (randomVar == 2): return 'cracked.path'
		if (randomVar == 3): return 'flower.path'
		if (randomVar == 4): return 'crackedFlower.path'

	randomVar = randNum(1,2)
	if (blockKind == 'cBlock'):
		if (randomVar == 1): return 'cBlock'
		if (randomVar == 2): return 'flower.cBlock'
	if (blockKind == 'wall' or blockKind == 'border'):
		if (randomVar == 1): return 'wall'
		if (randomVar == 2): return 'cracked.wall'
	if (blockKind == 'entrance' or blockKind == 'exit'):
		if (randomVar == 1): return 'door'
		if (randomVar == 2): return 'flower.door'

def getDir(entrancePos): # Creating the random path
	blockX = entrancePos[0]
	blockY = entrancePos[1]
	while (blockY - 1 != 0):
		randomVar = randNum(1,3)
		if (randomVar == 1 and gameBoard[blockY][blockX - 1][0] != 'border'): # Left
			blockX -= 1
		if (randomVar == 2 and gameBoard[blockY - 1][blockX][0] != 'border'): # Up
			blockY -= 1
		if (randomVar == 3 and gameBoard[blockY][blockX + 1][0] != 'border'): # Right
			blockX += 1
	while (blockY - 1 == 0 and blockX < int(round(xSize - (xSize / 4.0)))):
		blockX += 1
		posPath.append([blockX, blockY])
		posPath.append([blockX, blockY])
	exitPos = [blockX, blockY - 1]
	for i in range(len(posPath)):
		gameBoard[posPath[i][1]][posPath[i][0]] = [getBlockType(posPath[i][0],posPath[i][1],'origPath')]
	gameBoard[exitPos[1]][exitPos[0]] = ['exit']

def keyUp(event, funcX, funcY, playerDir): # Start Movement on Key Down
	if (event.key == K_UP or event.key == K_w):
		if (playerDir == 'back' and funcY - 1 >= 0 and funcY - 1 <= ySize - 1 and
			gameBoard[funcY - 1][funcX][0] != 'wall' and gameBoard[funcY - 1][funcX][0] != 'border'):
				funcY -= 1
		else:
			playerDir = 'back'

	elif (event.key == K_DOWN or event.key == K_s):
		if (playerDir == 'front' and funcY + 1 >= 0 and funcY + 1 <= ySize - 1 and
			gameBoard[funcY + 1][funcX][0] != 'wall' and gameBoard[funcY + 1][funcX][0] != 'border'):
				funcY += 1
		else:
			playerDir = 'front'

	elif (event.key == K_LEFT or event.key == K_a):
		if (playerDir == 'left' and funcX - 1 >= 0 and funcX - 1 <= xSize - 1 and
			gameBoard[funcY][funcX - 1][0] != 'wall' and gameBoard[funcY][funcX - 1][0] != 'border'):
				funcX -= 1
		else:
			playerDir = 'left'

	elif (event.key == K_RIGHT or event.key == K_d):
		if (playerDir == 'right' and funcX + 1 >= 0 and funcX + 1 <= xSize - 1 and
			gameBoard[funcY][funcX + 1][0] != 'wall' and gameBoard[funcY][funcX + 1][0] != 'border'):
				funcX += 1
		else:
			playerDir = 'right'

	return playerDir, funcX, funcY

def checkForward(playerDir, xBox, yBox, chestPos, animRun, diamonds):
	if (playerDir == 'front' and gameBoard[yBox + 1][xBox][0] == 'cBlock'):
		chestPos = [yBox + 1, xBox]
		animRun, diamonds = True, diamonds + 1
	if (playerDir == 'back' and gameBoard[yBox-1][xBox][0] == 'cBlock'):
		chestPos = [yBox - 1, xBox]
		animRun, diamonds = True, diamonds + 1
	if (playerDir == 'left' and gameBoard[yBox][xBox - 1][0] == 'cBlock'):
		chestPos = [yBox, xBox - 1]
		animRun, diamonds = True, diamonds + 1
	if (playerDir == 'right' and gameBoard[yBox][xBox + 1][0] == 'cBlock'):
		chestPos = [yBox, xBox + 1]
		animRun, diamonds = True, diamonds + 1
	return chestPos, animRun

def openChestAnim(diamonds, firstAnim, frameObj, animRun, chestPos, animCount, curFrame):
	yOpen = chestPos[0]
	xOpen = chestPos[1]
	if (animCount == 3 or firstAnim == True):
		if (gameBoard[yOpen][xOpen][1] == "cBlock"):
			frameObj.blit(cBlockSS, (0, 0), (0, 100 * curFrame, 100, 100))
		if (gameBoard[yOpen][xOpen][1] == "flower.cBlock"):
			frameObj.blit(flowerCBlockSS, (0, 0), (0, 100 * curFrame, 100, 100))
		curFrame += 1
		animCount = 0
		firstAnim = False
	screen.blit(frameObj,(xOpen*100,yOpen*100))
	if (curFrame == 10):
		gameBoard[yOpen][xOpen][0] = 'path'
		gameBoard[yOpen][xOpen][1] = getArt('path')
		diamonds += 1
		animRun = False
		firstAnim = True
		curFrame = 0
	return diamonds, firstAnim, animCount, curFrame, animRun

# Creating the game board in a row-major format
# Everything will be referenced [y][x] in the array
gameBoard = [[[''] for x in range(xSize)] for y in range(ySize)]
for loopY in range(ySize):
	randDoor = randNum(1,int(round((xSize-1)/4.0)))
	for loopX in range(xSize):
		gameBoard[loopY][loopX][0] = getBlockType(loopX,loopY,'other')

getDir(entrancePos) # Generates Random Path

# Making art for the game after the path is generated
for loopY in range(0,ySize):
	for loopX in range(0,xSize):
		if(loopX == entrancePos[0] and loopY == entrancePos[1]):
			gameBoard[loopY][loopX].append(getArt('entrance'))
		else:
			gameBoard[loopY][loopX].append(getArt(gameBoard[loopY][loopX][0]))

xBox, yBox = entrancePos # Sets the player's position

# Creates the pygame screen
screen = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Dungeon Game')
clock = pygame.time.Clock()

startButton = pygame.draw.rect(screen, blue,(400,700,200,100))

# Main Game Loop
while(gameOver == False):
	# Pygame event checking
	for event in pygame.event.get():
		if(event.type == pygame.MOUSEBUTTONDOWN):
			mousePos = pygame.mouse.get_pos()
			if(startButton.collidepoint(mousePos)):
				scene = 'game'
		if(event.type == pygame.KEYUP and scene == 'game' and animRun == False):
			if(event.key in [K_UP, K_w, K_DOWN, K_s, K_LEFT, K_a, K_RIGHT, K_d]):
				playerDir, xBox, yBox = keyUp(event, xBox, yBox, playerDir)
			elif(event.key == K_SPACE):
				chestPos, animRun = checkForward(playerDir,xBox,yBox,chestPos,animRun,diamonds)
		if(event.type == pygame.QUIT):
			gameOver = True

	# Putting images on the screen
	screen.fill(black)

	if(scene == 'startPage'): # Prints the start screen
		background = pygame.draw.rect(screen, green,(0,0,1200,900))
		#screen.blit(startScreen,(0,0)) - Blits start screen image to screen
		startButton = pygame.draw.rect(screen, blue,(500,700,200,100))
		screen.blit(pygame.font.SysFont('calibri', 30).render('Start', False, black),(575,730))
		screen.blit(pygame.font.SysFont('calibri', 150).render('dungeon', False, black),(200,200))
		screen.blit(pygame.font.SysFont('calibri', 150).render('game', False, black),(600,400))
	elif(scene == 'game'): # Prints the two-dimensional array to the screen
		for y in range(len(gameBoard)):
			for x in range(len(gameBoard[y])):
				screen.blit(pygame.transform.scale(pygame.image.load('gameArt/' + str(gameBoard[y][x][1]) + '.png'),(100,100)),(x*100, y*100))
		screen.blit(invBG,(0,800))
		for x in range(9): # Creating boxes in the inventory
			if(x == 8):
				screen.blit(diamondPic,((x+1)*110,812))
			if(x != 8):
				screen.blit(invObj,((x+1)*110,812))
		screen.blit(charDict[playerDir],(xBox*100+12, yBox*100+12))

	if(animRun == True):
		diamonds, firstAnim, animCount, curFrame, animRun = openChestAnim(diamonds,firstAnim,frameObj,animRun,chestPos,animCount,curFrame)

	# Other
	if(animRun == True):
		animCount += 1
	pygame.display.update()
	clock.tick(60)
endGame()
