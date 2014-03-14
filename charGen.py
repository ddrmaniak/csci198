#!/usr/bin/python

# -*- coding: UTF-8 -*-



# enable debugging

import cgitb, cgi, MySQLdb, random
cgitb.enable()

info = open('login info.txt','r')

credentials = info.readlines()	


db = MySQLdb.connect(credentials[0][:-1], credentials[1][:-1], credentials[2][:-1], credentials[3])
cursor = db.cursor()
race = "orc"
theClass = "warrior"

print "Content-Type: text/html;charset=utf-8\r\n"
print "<!doctype html>"
def makeChar(myRace, myClass, myLevel = 1):
	#starting off with universal stats
	stats = {'strength':0,'dexterity':0,'constitution':0,'intelligence':0,'wisdom':0,'charisma':0}
	
	#seeding abilities with random scores for NPCs
	stats['strength'] = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
	stats['dexterity'] = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
	stats['constitution'] = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
	stats['intelligence'] = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
	stats['wisdom'] = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
	stats['charisma'] = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
	
	#fetching any stat modifiers from the race 
	cursor.execute('''
	select trait, amount 
	from race_traits, race 
	where ID = rID and race.rName = "%s"
	'''%myRace)
	data = cursor.fetchall()
	
	#if the race has a modifier that isn't already in the dict, then it adds the key
	for row in data:
		if row[0] in stats:
			stats[row[0]] = stats[row[0]] + row[1]
		else:
			stats[row[0]] = row[1]
	
	#fetching the starting HP value
	cursor.execute('''
	select  hitDie
	from classes
	where classes.cName = "%s"
	'''%myClass)
	data = cursor.fetchall()
	for x in data:
		stats['hp'] = x[0]
		
	#fetching the character speed
	cursor.execute('''
	select speed
	from race
	where race.rName = "%s"
	'''%myRace)
	data = cursor.fetchall()
	for x in data:
		stats['speed'] = x[0]
	
	#fetching any stat modifiers from the class
	cursor.execute('''
	select baseAttackBonus, fortSave, refSave, willSave
	from class_table, classes
	where ID = cID and classes.cName = "%s" and cLevel = "%d"
	'''%(myClass,myLevel))
	data = cursor.fetchall()
	
	for x in data:
		stats['baseAttackBonus'] = x[0]
		stats['fortSave'] = x[1]
		stats['refSave'] = x[2]
		stats['willSave'] = x[3]
	
	stats['fortSave'] = stats['fortSave'] + ((stats['constitution']-10)/2)
	stats['refSave'] = stats['refSave'] + ((stats['dexterity']-10)/2)
	stats['willSave'] = stats['willSave'] + ((stats['wisdom']-10)/2)
	
	if 'initiative' in stats:
		stats['initiative'] = stats['initiative'] + ((stats['dexterity']-10)/2)
	else:
		stats['initiative'] = ((stats['dexterity']-10)/2)
		
	stats['ac'] = 10 + ((stats['dexterity']-10)/2)
	return stats
	'''
	blah = stats.keys()
	print '<table>'
	for x in blah:
		print '<tr>'
		myStat = ((stats[x]-10)/2)
		str = ''
		if (x != 'dexterity' and x != 'strength' and x != 'charisma' and x != 'intelligence' and x != 'constitution' and x != 'wisdom'):
			str = ''
		elif myStat >= 0:
			str = '+%s'%myStat
		else:
			str = '%s'%myStat
		print "<td>%s</td>"%x, '<td>', stats[x], '</td>', '<td>',str,'</td>'
		print '</tr>'
	print '</table>'
	'''
for i in range (0, 3):
	myChar = makeChar(race, theClass, 1)
	print '%s %d'%(race,i)
	print '<table border="1">'
	print '<tr>', '<td>', 'HP:', '</td>', '<td>', myChar['hp'], '</td>', '</tr>'
	print '<tr>', '<td>','initiative:', '</td>', '<td>', myChar['initiative'], '</td>', '</tr>'
	print '<tr>', '<td>','speed:', '</td>', '<td>', myChar['speed'], '</td>', '</tr>'
	print '<tr>', '<td>','ac:', '</td>', '<td>', myChar['ac'], '</td>', '</tr>'
	print '<tr>', '<td>','base attack bonus:', '</td>', '<td>',myChar['baseAttackBonus'], '</td>', '</tr>'
	print '<tr>', '<td>','strength:', '</td>', '<td>', myChar['strength'], '</td>',  '</tr>'
	print '<tr>', '<td>','dexterity:', '</td>', '<td>', myChar['dexterity'], '</td>',  '</tr>'
	print '<tr>', '<td>','constitution:', '</td>', '<td>', myChar['constitution'], '</td>', '</tr>'
	print '<tr>', '<td>','intelligence:', '</td>', '<td>', myChar['intelligence'], '</td>', '</tr>'
	print '<tr>', '<td>','wisdom:', '</td>', '<td>', myChar['wisdom'], '</td>', '</tr>'
	print '<tr>', '<td>','charisma:', '</td>', '<td>', myChar['charisma'], '</td>', '</tr>'
	print '</table>'
	print


