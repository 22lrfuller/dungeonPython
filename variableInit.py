# Importing needed modules
from random import randint as randNum
import pygame

# Board size constants
xSize = 12
ySize = 8

# Maximum index for board coordinates
xMax = xSize - 1
yMax = ySize - 1

xBox = 0 # Tile x position
yBox = 0 # Tile y position

diamonds = 0 # Diamond count
animCount = 0 # Animation counter
curFrame = 0 # Keeps track of current frame

scene = 'startPage' # Will either be start or game
playerDir = 'front' # What direction the player is facing

gameOver = False # Game runs while False
animRun = False # Animation runs while True
firstAnim = True # Checks if it is the first time going through that animation

chestPos = [] # Stores the position of the chest the player opens
entrancePos = [] # Stores the entrance position
posPath = [] # Stores the blocks in the entrance to exit path

displayWidth = xSize*100 # The width of the screen
displayHeight = (ySize+1)*100 # The height of the screen
randBlock = randNum(1,10) # Variable used for random operations
frameObj = pygame.Surface([100, 100]) # Holds the size of each frame in a spritesheet

# Colors in (RGB) format
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 125, 255)

# GUI images
startScreen = pygame.transform.scale(pygame.image.load('gameArt/startScreen.png'), (1000,1000))
invBG = pygame.transform.scale(pygame.image.load('gameArt/invBG.png'), (1200,100))
invObj = pygame.transform.scale(pygame.image.load('gameArt/invObj.png'), (75,75))
diamondPic = pygame.transform.scale(pygame.image.load('gameArt/diamond.png'), (75,75))

# Block images
path = pygame.transform.scale(pygame.image.load('gameArt/path.png'), (100,100))
crackedPath = pygame.transform.scale(pygame.image.load('gameArt/cracked.path.png'), (100,100))
flowerPath = pygame.transform.scale(pygame.image.load('gameArt/flower.path.png'), (100,100))
crackedFlowerPath = pygame.transform.scale(pygame.image.load('gameArt/crackedFlower.path.png'), (100,100))
cBlock = pygame.transform.scale(pygame.image.load('gameArt/cBlock.png'), (100,100))
flowerCBlock = pygame.transform.scale(pygame.image.load('gameArt/flower.cBlock.png'), (100,100))
wall = pygame.transform.scale(pygame.image.load('gameArt/wall.png'), (100,100))
crackedWall = pygame.transform.scale(pygame.image.load('gameArt/cracked.wall.png'), (100,100))
door = pygame.transform.scale(pygame.image.load('gameArt/door.png'), (100,100))
flowerDoor = pygame.transform.scale(pygame.image.load('gameArt/flower.door.png'), (100,100))

# Spritesheets
cBlockSS = pygame.transform.scale(pygame.image.load('gameArt/cBlockSS.png'), (100,1000))
flowerCBlockSS = pygame.transform.scale(pygame.image.load('gameArt/flower.cBlockSS.png'), (100,1000))

# Character images
charDict = {
'front':pygame.transform.scale(pygame.image.load('gameArt/charFront.png'), (75, 75)),
'back':pygame.transform.scale(pygame.image.load('gameArt/charBack.png'), (75, 75)),
'left':pygame.transform.scale(pygame.image.load('gameArt/charLeft.png'), (75, 75)),
'right':pygame.transform.scale(pygame.image.load('gameArt/charRight.png'), (75, 75))
}

# Number images
numberImg = {
'zero':pygame.transform.scale(pygame.image.load('gameArt/numbers/zero.png'),(75,75)),
'one':pygame.transform.scale(pygame.image.load('gameArt/numbers/one.png'),(75,75)),
'two':pygame.transform.scale(pygame.image.load('gameArt/numbers/two.png'),(75,75)),
'three':pygame.transform.scale(pygame.image.load('gameArt/numbers/three.png'),(75,75)),
'four':pygame.transform.scale(pygame.image.load('gameArt/numbers/four.png'),(75,75)),
'five':pygame.transform.scale(pygame.image.load('gameArt/numbers/five.png'),(75,75)),
'six':pygame.transform.scale(pygame.image.load('gameArt/numbers/six.png'),(75,75)),
'seven':pygame.transform.scale(pygame.image.load('gameArt/numbers/seven.png'),(75,75)),
'eight':pygame.transform.scale(pygame.image.load('gameArt/numbers/eight.png'),(75,75)),
'nine':pygame.transform.scale(pygame.image.load('gameArt/numbers/nine.png'),(75,75))
}
