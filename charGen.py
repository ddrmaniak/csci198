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
random.seed()

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
	
	#if the race has a modifier that isn't already in the dict, then it adds the key, otherwise it just applies it
	for row in data:
		if row[0] in stats:
			stats[row[0]] = stats[row[0]] + row[1]
		else:
			stats[row[0]] = row[1]
			
	
	#fetching the starting HP and skillmod values
	cursor.execute('''
	select  hitDie, skillmod
	from classes
	where classes.cName = "%s"
	'''%myClass)
	data = cursor.fetchall()
	
	skillmod = 0 #initializing skillmod for later use
	hd = 0 #initializing hd(hit dice) for later
	
	for x in data:
		stats['hp'] = max(1, x[0] + (stats['constitution']-10)/2)
		hd = x[0] 
		skillmod = x[1]
	
	#initializing skill points count
	skillPoints = (((stats['intelligence']-10)/2) + skillmod)*4	
	
	#leveling up the character
	if myLevel > 1:
		for i in range (2,myLevel):
		
			if i%4 == 0: #every 4th level, increment 1 random ability by 1
				k = random.randint(1,6)
				if k == 1:
					stats['strength'] = stats['strength'] + 1
				elif k == 2:
					stats['dexterity'] = stats['dexterity'] + 1
				elif k == 3:
					if (stats['constitution']-10)/2 < (stats['constitution']-10+1)/2:
						stats['hp'] = stats['hp'] + (i-1)
					stats['constitution'] = stats['constitution'] + 1
				elif k == 4:
					stats['intelligence'] = stats['intelligence'] + 1
				elif k == 5:
					stats['wisdom'] = stats['wisdom'] + 1
				else:
					stats['charisma'] = stats['charisma'] + 1
			
			skillPoints = skillPoints + ((stats['intelligence']-10)/2) + skillmod
			
			stats['hp'] = stats['hp'] + max(1, random.randint(1,hd) + ((stats['constitution']-10)/2))
			

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
	
	
for i in range (0, 3):
	myChar = makeChar(race, theClass, 5)
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


