import random
import math
class Room:
	def __init__(self, minSize, maxSize):
		self.width = random.randint(minSize,maxSize)
		self.height = random.randint(minSize,maxSize)
		self.cell = None,None
		self.midPoint = 0,0
	def setMid(self, cell, cellSize):
		self.midPoint = (self.cell[0] * cellSize + self.width)/2, (self.cell[1] * cellSize + self.height)/2

def assignCells(rooms, cells, rNum, form, cellsize):
	for i in range(rNum):
		rooms.append(Room(int(form['rSize1'].value),int(form['rSize2'].value)))
		rooms[i].cell = random.randint(0, cellsize - 1),random.randint(0, cellsize - 1)
		
		#make sure that the cell isn't occupied, if it is, then choose a different one
		while cells[rooms[i].cell[0]][rooms[i].cell[1]] == 1:
			rooms[i].cell = random.randint(0, cellsize - 1),random.randint(0, cellsize - 1)
		
		#mark the cell as occupied
		cells[rooms[i].cell[0]][rooms[i].cell[1]] = 1

def A_star(rooms, map, start, destination):
	cSet = []
	#(current node, predecessor, g, f)
	oSet = [(rooms[start].midPoint, rooms[start].midPoint, 0, heuristic(rooms[start].midpoint, rooms[destination].midpoint))]#(node, parent, G, F), F = G+H
	while oSet:
		oSet.sort(key = lambda tup: tup[3])
		current = oSet.pop[0]
		if current[0] == rooms[destination].midpoint:
			return tracePath(current, cSet)
		successors = []
		for i in range (0,4):#checking the validity of the potential successors
			xCoord = current[0][0]+int(math.cos(math.pi*i/2))
			yCoord = current[0][1]+int(math.sin(math.pi*i/2))
			if isValidNode(xCoord, yCoord, map, start, destination):
				successors.append((xCoord,yCoord), current[0], current[2]+1, current[2] + 1 + heuristic((xCoord, yCoord), destination))
		for x in successors:#actually comparing them to the ones in oSet and cSet
			if any(x[0] == y[0] and x[2] >= y[2] for y in oSet):#the one in oSet is already better, discard this successor
				continue
			if any(x[0] == y[0] and x[2] >= y[2] for y in cSet):#the one in cSet is already better, discard this successor
				continue
			oSet = [i for i in oSet if i[0] != x[0]]#remove current successor from oSet
			cSet = [i for i in cSet if i[0] != x[0]]#remove current successor from cSet
			oSet.append(x)#add this successor to oSet
		cSet.append(current)
			
#distance formula
def heuristic(start, destination):
	return math.sqrt((destination[0]-start[0])**2+(destination[1]-start[1])**2)
	
def tracePath(current, cSet):
	#todo:write all this stuff

def isValidNode(xCoord, yCoord, map, start, destination):
	if xCoord < 0 or xCoord > map.length():
		return false
	if yCoord < 0 or yCoord > map.length():
		return false
	for i in range (0,4):
		if map[xCoord+int(math.cos(math.pi*i/2))][yCoord+int(math.sin(math.pi*i/2))] == '@':
			continue
		elif map[xCoord+int(math.cos(math.pi*i/2))][yCoord+int(math.sin(math.pi*i/2))] == str(start):
			continue
		elif map[xCoord+int(math.cos(math.pi*i/2))][yCoord+int(math.sin(math.pi*i/2))] == str(destination):
			continue
		else
			return false
	return true;