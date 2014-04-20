#!/usr/bin/python

# -*- coding: UTF-8 -*-



# enable debugging
import cgitb, cgi, random,roomDefs
cgitb.enable()

form = cgi.FieldStorage()

#deciding the number of rooms
rNum = random.randint(int(form['rNum1'].value), int(form['rNum2'].value))

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

#update the map grid with the room locations
for i in range(rNum):
	for j in range (rooms[i].height):
		for k in range (rooms[i].width):
			map[rooms[i].cell[0]*cellsize+j][rooms[i].cell[1]*cellsize+k] = str(i)

#print out the HTML
print "Content-Type: text/html;charset=utf-8\r\n"
print
print "<!doctype html>"
print "<html><body>"
print "<style>body {font-family:'Courier New';}</style>"
print '<table bordercolor="000000" style="border-collapse:collapse">'
for i in range(len(map)):
	print '<tr>'
	for j in range(len(map)):
		if map[i][j] == '@':
			print '<td bgcolor="000000">','_'*(len(str(len(rooms)))),'</td>'
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
			print '<td bgcolor="',num,'">',map[i][j],'</td>'
	print '</tr>'
print '</table>'
for i in range(len(rooms)):
	print i,':',rooms[i].width,'x',rooms[i].height,' color: <table style="display:inline;"><tr><td bgcolor="',hex(avg*(i+1))[2:],'">&nbsp;&nbsp;</td></tr></table><br>'
print "</body></html>"