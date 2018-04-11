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
