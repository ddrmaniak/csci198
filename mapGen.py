#!/usr/bin/python

# -*- coding: UTF-8 -*-



# enable debugging

import cgitb, cgi, random
cgitb.enable()

form = cgi.FieldStorage()

rNum = random.randint(int(form['rNum1'].value), int(form['rNum2'].value))
cellsSqrt = 0
while cellsSqrt*cellsSqrt <= rNum * 2:
	cellsSqrt += 1

class Room:
	def __init__(self, minSize, maxSize):
		self.height = random.randint(minSize,maxSize)
		self.width = random.randint(minSize,maxSize)
		self.cell = None,None

cellsize = int(form['rSize2'].value)+1
#making the map matrix
map = [None]*(cellsSqrt*cellsize)
for i in range (cellsSqrt*cellsize):
	map[i] = ['@']*(cellsSqrt*cellsize)

cells = [None]*cellsSqrt
for i in range (cellsSqrt):
	cells[i] = [0]*cellsSqrt
rooms = []
for i in range(rNum):
	rooms.append(Room(int(form['rSize1'].value),int(form['rSize2'].value)))
	rooms[i].cell = random.randint(0, cellsSqrt - 1),random.randint(0, cellsSqrt - 1)
	while cells[rooms[i].cell[0]][rooms[i].cell[1]] == 1:
		rooms[i].cell = random.randint(0, cellsSqrt - 1),random.randint(0, cellsSqrt - 1)
	cells[rooms[i].cell[0]][rooms[i].cell[1]] = 1

for i in range(rNum):
	for j in range (rooms[i].height):
		for k in range (rooms[i].width):
			map[rooms[i].cell[0]*cellsize+j][rooms[i].cell[1]*cellsize+k] = str(i)


print "Content-Type: text/html;charset=utf-8\r\n"
print
print "<!doctype html>"
print "<html><body>"
print "<style>body {font-family:'Courier New';} </style>"
print '<table bordercolor="000000" style="border-collapse:collapse">'
for i in range(len(map)):
	print '<tr>'
	for j in range(len(map)):
		if map[i][j] == '@':
			print '<td bgcolor="000000" width="20" height = "20">',map[i][j],'</td>'
		else:
			avg = 16777215/(len(rooms)+2)
			num = hex(avg*(int(map[i][j])+1))[2:]
			if len(num) == 5:
				num.append('0')
			elif len(num) == 4:
				num.append('00')
			elif len(num) == 3:
				num.append('000')
			elif len(num) == 2:
				num.append('0000')
			elif len(num) == 1:
				num.append('00000')
			print '<td bgcolor="',num,'">',map[i][j],'</td>'
	print '</tr>'
print '</table>'
for i in range(len(rooms)):
	print i,': ',rooms[i].width,' x ',rooms[i].height,' color: ',hex(avg*(i+1))[2:],'<br>'
print "</body></html>"