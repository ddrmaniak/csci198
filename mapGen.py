#!/usr/bin/python

# -*- coding: UTF-8 -*-



# enable debugging
import cgitb, cgi, random, roomDefs, charDefs
cgitb.enable()

form = cgi.FieldStorage()

def makeEncounters(rooms, PL):
	encounters = [[]]
	encounterNumbers = [[1,None,None,None,None,None,None,None,None,None,None,None],
						[2,1,None,None,None,None,None,None,None,None,None,None],
						[3,2,1,None,None,None,None,None,None,None,None,None],
						[5,3,2,1,1,None,None,None,None,None,None,None],
						[6,4,3,2,1,1,None,None,None,None,None,None],
						[7,5,4,3,2,2,1,1,1,None,None,None],
						[8,6,5,4,3,3,2,2,2,1,1,1],
						[9,7,6,5,4,4,3,3,3,2,2,2],	
						[10,8,7,6,5,5,4,4,4,3,3,3],
						[11,9,8,7,6,6,5,5,5,4,4,4],
						[12,10,9,8,7,7,6,6,6,5,5,5],
						[13,11,10,9,8,8,7,7,7,6,6,6],
						[14,12,11,10,9,9,8,8,8,7,7,7],
						[15,13,12,11,10,10,9,9,9,8,8,8],
						[16,14,13,12,11,11,10,10,10,9,9,9],
						[17,15,14,13,12,12,11,11,11,10,10,10],
						[18,16,15,14,13,13,12,12,12,11,11,11],
						[19,17,16,15,14,14,13,13,13,12,12,12]
						]
	eLimit = 1.0
	roomCntr = 0
	while eLimit > .2 and roomCntr < len(rooms):
		encLvl = random.randint(1,PL+2)
		if encLvl <= PL:
			eLimit -= .2/(2**((PL-encLvl)/2))
		else:
			eLimit -= .2*(encLvl-PL)
		tblLimit = 11
		while not encounterNumbers[encLvl-1][tblLimit]:
			tblLimit -= 1
		numMonsters = random.randint(1,min(max(tblLimit,1), (rooms[roomCntr].width*rooms[roomCntr].height)/3))
		for i in range(0, numMonsters):
			encounters[roomCntr].append(charDefs.makeChar('orc', 'warrior', encounterNumbers[encLvl-1][numMonsters-1]))
		roomCntr += 1
		encounters.append([])
	return encounters


page = ""
#print out the HTML
print "Content-Type: text/html;charset=utf-8\r\n"
print
print "<!doctype html>"
print "<html><body>"
print "<style>body {font-family:'Courier New';}</style>"
print '<div id="map">'
noErr = True
try:
	int(form['rNum1'].value)
	int(form['rNum2'].value)
	int(form['rSize1'].value)
	int(form['rSize2'].value)
	int(form['EL'].value)
except ValueError:
	page = "All text fields must be integers."
	noErr = False

if noErr:
	if int(form['rNum2'].value) < int(form['rNum1'].value):
		page = "The second room number value must be greater than or equal to the first value."
		noErr = False
	if int(form['rSize2'].value) < int(form['rSize1'].value):
		page = "The second room size value must be greater than or equal to the first value."
		noErr = False
	if int(form['rSize2'].value) <= 0 or int(form['rSize1'].value) <= 0 or int(form['rNum1'].value) <= 0 or int(form['rNum2'].value) <= 0 or int(form['EL'].value) <= 0:
		page = "All values must be grater than 0."
		noErr = False
	
if noErr:
	#deciding the number of rooms
	if int(form['rNum1'].value) < int(form['rNum2'].value):
		rNum = random.randint(int(form['rNum1'].value), int(form['rNum2'].value))
	else:
		rNum = int(form['rNum1'].value)
	
	#deciding the number of cells. it should be the second lowest perfect square greater than the number of rooms * 2
	cellsSqrt = 0
	while cellsSqrt*cellsSqrt <= rNum * 2:
		cellsSqrt += 1
	
	#cell size will always be 1 greater than the size of the largest room. this will prevent two rooms from being flush against eachother
	cellsize = int(form['rSize2'].value)+1
	
	#making the map matrix
	map = [None]*(cellsSqrt*cellsize)
	for i in range (cellsSqrt*cellsize):
		map[i] = ['@']*(cellsSqrt*cellsize)
	
	#making the cells
	cells = [None]*cellsSqrt
	for i in range (cellsSqrt):
		cells[i] = [0]*cellsSqrt
		
	#making each room
	rooms = []
	roomDefs.assignCells(rooms, cells, rNum, form, cellsSqrt)
	for i in rooms:
		i.setMid(cellsize)
		
	
	#update the map grid with the room locations
	for i in range(rNum):
		for j in range (rooms[i].height):
			for k in range (rooms[i].width):
				map[rooms[i].cell[0]*cellsize+j][rooms[i].cell[1]*cellsize+k] = str(i)
				
	paths = roomDefs.makePaths(rooms, map)
	for path in paths:
		for s in path:
			if map[s[0]][s[1]] == '@':
				map[s[0]][s[1]] = ' '
	enc = makeEncounters(rooms,int(form['EL'].value))
	
	#preparing the actual page for printing
	page += '<table bordercolor="000000" style="border-collapse:collapse">'
	for i in range(len(map)):
		page += '<tr>'
		for j in range(len(map)):
			if map[i][j] == '@':
				page += '<td bgcolor="000000">'+'_'*(len(str(len(rooms))))+'</td>\n'
			elif map[i][j] == ' ':
				page += '<td bgcolor="FFFFFF">'+'&nbsp;'*(len(str(len(rooms))))+'</td>\n'
			else:
				avg = 16777215/(len(rooms)+2)
				num = hex(avg*(int(map[i][j])+1))[2:]
				if len(num) == 5:
					num += '0'
				elif len(num) == 4:
					num += '00'
				elif len(num) == 3:
					num += '000'
				elif len(num) == 2:
					num += '0000'
				elif len(num) == 1:
					num += '00000'
				page += '<td bgcolor="'+str(num)+'">'+str(map[i][j])+'</td>\n'
		page += '</tr>\n'
	page += '</table>\n'
	page += '<br>'
	for i in range(len(rooms)):
		page += str(i)+' :'+str(rooms[i].width)+'x'+' color: <table style="display:inline;"><tr><td bgcolor="'+str(hex(avg*(i+1))[2:])+'">&nbsp;&nbsp;</td></tr></table>'+ '<br>'
		if i < len(enc):
			for j in range(0,len(enc[i])):
				page += '<p>&nbsp;&nbsp;&nbsp;&nbsp; HP:'+ str(enc[i][j]['hp'])+ ' init:'+ str(enc[i][j]['initiative'])+ ' sp:'+ str(enc[i][j]['speed'])+'<br>'+'&nbsp;&nbsp;&nbsp;&nbsp; ac:'+str(enc[i][j]['ac'])+' bab:'+str(enc[i][j]['baseAttackBonus'])+' str:'+str(enc[i][j]['strength'])
				page += ' dex:'+str(enc[i][j]['dexterity'])+'<br>'+'&nbsp;&nbsp;&nbsp;&nbsp; con:'+str(enc[i][j]['constitution'])+' int:'+str(enc[i][j]['intelligence'])+' wis:'+str(enc[i][j]['wisdom'])+' cha:'+str(enc[i][j]['charisma'])+'</p>'
		page+= "<br>"
print page
print "</div>"
print "</body></html>"