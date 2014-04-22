import random
import math
class Room:
	def __init__(self, minSize, maxSize):
		self.width = random.randint(minSize,maxSize)
		self.height = random.randint(minSize,maxSize)
		self.cell = None,None
		self.midPoint = 0,0
	def setMid(self, cellSize):
		self.midPoint = (self.cell[0] * cellSize + self.height/2), (self.cell[1] * cellSize + self.width/2)

def assignCells(rooms, cells, rNum, form, cellsSqrt):
	for i in range(rNum):
		rooms.append(Room(int(form['rSize1'].value),int(form['rSize2'].value)))
		rooms[i].cell = random.randint(0, cellsSqrt - 1),random.randint(0, cellsSqrt - 1)
		
		#make sure that the cell isn't occupied, if it is, then choose a different one
		while cells[rooms[i].cell[0]][rooms[i].cell[1]] == 1:
			rooms[i].cell = random.randint(0, cellsSqrt - 1),random.randint(0, cellsSqrt - 1)
		
		#mark the cell as occupied
		cells[rooms[i].cell[0]][rooms[i].cell[1]] = 1

def A_star(rooms, map, start, destination):
	cSet = []
	#(current node, predecessor, g, f)
	oSet = [(rooms[start].midPoint, rooms[start].midPoint, 0, heuristic(rooms[start].midPoint, rooms[destination].midPoint))]#(node, parent, G, F), F = G+H
	while oSet:
		oSet.sort(key = lambda tup: tup[3])
		current = oSet.pop(0)
		if current[0] == rooms[destination].midPoint:
			return tracePath(current, cSet)
		successors = []
		for i in range (0,4):#checking the validity of the potential successors
			xCoord = current[0][0]+int(math.cos(math.pi*i/2))
			yCoord = current[0][1]+int(math.sin(math.pi*i/2))
			if isValidNode(xCoord, yCoord, map, start, destination):
				successors.append(((xCoord,yCoord), current[0], current[2]+1, current[2] + 1 + heuristic((xCoord, yCoord), rooms[destination].midPoint)))
		for x in successors:#actually comparing them to the ones in oSet and cSet
			if any(x[0] == y[0] and x[2] >= y[2] for y in oSet):#the one in oSet is already better, discard this successor
				continue
			if any(x[0] == y[0] and x[2] >= y[2] for y in cSet):#the one in cSet is already better, discard this successor
				continue
			oSet = [i for i in oSet if i[0] != x[0]]#remove current successor from oSet
			cSet = [i for i in cSet if i[0] != x[0]]#remove current successor from cSet
			oSet.append(x)#add this successor to oSet
		cSet.append(current)
	return False

#distance formula
def heuristic(start, destination):
	return math.sqrt((destination[0]-start[0])**2+(destination[1]-start[1])**2)
	
def tracePath(goal, cSet):
	curr = goal
	path = [curr[0]]
	while(curr[0] != curr[1]):#repeats until current = current's parent
		path.append(curr[1])
		curr = [i for i in cSet if i[0] == curr[1]][0]#sets curr to the parent of the current node
	return path

def makePaths(rooms, map):
	weights = []
	paths = []
	mst, free  = [rooms[0]], rooms[1:]
	for i in range (1, len(rooms)):#this gets some initial values into weights
		weights.append((0, i, heuristic(rooms[0].midPoint,rooms[i].midPoint)))
		
	while free:
		low = min(weights, key = lambda tup: tup[2])
		#weights = [i for i in weights if i[1] == low[0]]
		
		for f in mst:#eliminates all weights between each member of mst as they are added
			mp = rooms[rooms.index(f)].midPoint
			weights.remove((rooms.index(f),low[1],heuristic(rooms[low[1]].midPoint,mp)))
			
		try:#sometimes it makes a connection to something already in mst, so I threw in this try/catch
			free.remove(rooms[low[1]])#remove the room that we're making a connection to
			mst.append(rooms[low[1]])#and add it to the MST that we're building
		except myError:
			pass
			
		path = A_star(rooms, map, low[0], low[1])#uses A* to make a path between two rooms
		paths.append(path)#adds it to the list of paths that will be returned
		
		for i in free:#adds new weights from mst's newly added room to everything in free
			weights.append((low[1],rooms.index(i), heuristic(rooms[low[1]].midPoint,i.midPoint)))
			
	return paths

	
def isValidNode(xCoord, yCoord, map, start, destination):
	if xCoord < 0 or xCoord > len(map):
		return False
	if yCoord < 0 or yCoord > len(map):
		return False
	for i in range (0,4):
		if len(map) <= xCoord+int(math.cos(math.pi*i/2)):
			return False
		elif len(map[int(math.cos(math.pi*i/2))]) <= yCoord+int(math.sin(math.pi*i/2)):
			return False
		elif map[xCoord+int(math.cos(math.pi*i/2))][yCoord+int(math.sin(math.pi*i/2))] == '@':
			continue
		elif map[xCoord+int(math.cos(math.pi*i/2))][yCoord+int(math.sin(math.pi*i/2))] == str(start):
			continue
		elif map[xCoord+int(math.cos(math.pi*i/2))][yCoord+int(math.sin(math.pi*i/2))] == str(destination):
			continue
		else:
			return False
	return True