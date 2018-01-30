import markovify
import re
import random
import time
import ast
import copy
import math
from tkinter import *
from functools import partial

UPDATE_RATE = 1000
MARQUEE_SIZE = 10
testnum = 0
ENEMY_SIZE = 3
PLAYER_SIZE = 3
globalSkills = []
globalChars = []
combatDecks = []
combatHands = []


class App:
	
	def __init__(self, master):
		self.frame = Frame(master,width=10,height=10,bg="", colormap="new")
		self.topBtn= [0]*3
		self.botBtn= [0]*3
		self.handBtn= [0]*10
		self.skillName = ""
		self.skillTargets = []
		self.gameField = Field()
		self.create_frame()
		self.selectedSpot = -1
		self.selectedStatus = -1
		self.globalPlayers = []
		self.selectedPlayer = -1
		self.selectedSkill = -1
		self.ORDER = []
		self.currentTurn = 0
		
		self.start_game()
		
		

	def resetGui(self):
		self.frame.configure(background='white')
	def create_spots(self):
		for x in range(0, ENEMY_SIZE):
			tempButton = Button(self.frame, text=x, fg="black", height=2,width=4,command= partial(self.displayCharInfo,x+PLAYER_SIZE))
			tempButton.grid(row=0,column=x)
			self.topBtn[x] = tempButton
		
		for x in range(0, PLAYER_SIZE):
			tempButton = Button(self.frame, text=x, fg="black", height=2,width=4,command= partial(self.displayCharInfo,x))
			tempButton.grid(row=1,column=x)
			self.botBtn[x] = tempButton
			
		for x in range(0, 10):
			tempButton = Button(self.frame, wraplength=40, text=x, fg="black", height=2,width=8,command= partial(self.display_skill_info,x))
			tempButton.grid(row=2,column=x)
			self.handBtn[x] = tempButton
		
	def update_colors(self):
		for x in range(0, 3):
			if self.gameField.handField[x] != 0:
				self.handBtn[x].config(fg="blue")
			else:
				self.handBtn[x].config(fg="black")
				
	def create_marquee(self):
		self.marqueeFrame = Frame(self.frame,width=10,height=10,bg="", colormap="new")
		self.marqueeFrame.grid(row=3,column=0)
		self.marqueeList = []
		self.marqueeText = [""] * MARQUEE_SIZE
		for x in range(0, MARQUEE_SIZE):
			tempLabel = Label(self.marqueeFrame, text="",anchor="w")
			tempLabel.grid(row=x,column=0,columnspan=10)
			self.marqueeList.append(tempLabel)

		
	def marqueeAdd(self, textStringAdd):	
		for x in range(MARQUEE_SIZE-1,0,-1):
			
			self.marqueeText[x] = self.marqueeText[x-1]
			#self.marqueeText[x] = 'wow'
		self.marqueeText[0] = textStringAdd	
		
		for x in range(0,MARQUEE_SIZE):
			self.marqueeList[x].config(text=self.marqueeText[x])
		self.resetGui()
		
	def create_infoBox(self):
		self.infoFrame = Frame(self.frame,width=10,height=10,bg="", colormap="new")
		self.infoFrame.configure(background='white')
		self.infoFrame.grid(row=0,column=10,rowspan=2,padx=10,pady=5)
		self.infoBox = []
		self.nameText = StringVar()
		self.costText = StringVar()
		self.typeText = StringVar()
		self.infoText = StringVar()
		self.powerText = StringVar()
		self.toughText = StringVar()
		self.infoBox.append(Label(self.infoFrame, textvariable=self.nameText,anchor="w"))
		self.infoBox[0].grid(row=0,column=0,columnspan=2,padx=10,pady=10)
		
		self.infoBox.append(Label(self.infoFrame, textvariable=self.costText,anchor="w"))
		self.infoBox[1].grid(row=1,column=0,padx=1,pady=1)
		
		self.infoBox.append(Label(self.infoFrame, textvariable=self.typeText,anchor="w"))
		self.infoBox[2].grid(row=1,column=1,padx=1,pady=1)
		
		self.infoBox.append(Message(self.infoFrame, textvariable=self.infoText,anchor="w"))
		self.infoBox[3].grid(row=3,column=0,columnspan=2,padx=1,pady=1)
		
		self.infoBox.append(Label(self.infoFrame, textvariable=self.powerText,anchor="w"))
		self.infoBox[4].grid(row=2,column=0,padx=1,pady=1)
		
		self.infoBox.append(Label(self.infoFrame, textvariable=self.toughText,anchor="w"))
		self.infoBox[5].grid(row=2,column=1,padx=1,pady=1)
		self.actionButtons = []
		tempButton = Button(self.infoFrame, text="Play", fg="black", height=2,width=4,command= partial(self.infoAction0))
		tempButton.grid(row=4,column=1,columnspan=1)
		self.actionButtons.append(tempButton)
		
	def createSkillTarget(self):
		self.skillSelectFrame = Frame(self.frame,width=10,height=10,bg="", colormap="new")
		self.skillSelectFrame.configure(background='white')
		self.skillSelectFrame.grid(row=0,column=10,rowspan=2,padx=10,pady=5)

		for x in range(0, ENEMY_SIZE):
			tempButton = Button(self.skillSelectFrame, wraplength=45, text=x, fg="black", height=1,width=2,command= partial(self.getCharToUseSkill,PLAYER_SIZE+x,1))
			tempButton.grid(row=0,column=x)
			self.skillTargets.append(tempButton)
			
			
		for x in range(0, PLAYER_SIZE):
			tempButton = Button(self.skillSelectFrame, wraplength=45, text=x, fg="black", height=1,width=2,command= partial(self.getCharToUseSkill,x,0))
			tempButton.grid(row=1,column=x)
			self.skillTargets.append(tempButton)
			
	def createSkillInfoBox(self):
		self.skillInfoFrame = Frame(self.frame,width=10,height=10,bg="", colormap="new")
		self.skillInfoFrame.configure(background='white')
		self.skillInfoFrame.grid(row=3,column=1,columnspan=5, rowspan=1,padx=10,pady=5)
		
		self.skillNameText = StringVar()
		self.skillDescText = StringVar()
		self.skillInfoBox = []
		self.skillInfoBox.append(Label(self.skillInfoFrame, wraplength=100, height=2,width=8, textvariable=self.skillNameText,anchor="w"))
		self.skillInfoBox[0].grid(row=0,column=0,columnspan=1,padx=5,pady=5)
		self.skillInfoBox.append(Label(self.skillInfoFrame, wraplength=280, height=5,width=40, textvariable=self.skillDescText,anchor="w"))
		self.skillInfoBox[1].grid(row=1,column=0,columnspan=1,padx=5,pady=5)
		
	def createCharInfoBox(self):
		self.charInfoFrame = Frame(self.frame,width=10,height=10,bg="", colormap="new")
		self.charInfoFrame.configure(background='white')
		self.charInfoFrame.grid(row=4,column=1,columnspan=5, rowspan=1,padx=10,pady=50)
		
		self.charNameText = StringVar()
		self.charHealthText = StringVar()
		
		self.charInfoBox = []
		self.charInfoBox.append(Label(self.charInfoFrame, wraplength=100, height=2,width=8, textvariable=self.charNameText,anchor="w"))
		self.charInfoBox[0].grid(row=0,column=0,columnspan=1,padx=5,pady=5)
		self.charInfoBox.append(Label(self.charInfoFrame, wraplength=300, height=10,width=30, textvariable=self.charHealthText,anchor="w"))
		self.charInfoBox[1].grid(row=1,column=0,columnspan=1,padx=5,pady=5)
	
	def selectionTarget(self, x):
		print("Select")
		
	def infoAction0(self):
		if selectedStatus == 0:
			print("Play")
			
	def resetSkillTargetColor(self):

		for x in range(0, len(self.skillTargets)):
			self.skillTargets[x].config(fg="black")
		
	
	def getValidTargets(self,user,skill):
		allies = []
		enemies = []
		for x in range(0, len(self.globalPlayers)):
			if self.globalPlayers[x] == user:
				spotMine = x
		
	def colorTargets(self,user,skill):
		targetType = skill.TARGET[0].get("ATARGET", "")
		self.resetSkillTargetColor()

		self.resetGui()
		
	
	def create_frame(self):
		self.frame.grid(row=0,column=0)
		self.create_spots()
		#self.create_infoBox()
		self.createSkillTarget()
		self.createSkillInfoBox()
		self.createCharInfoBox()
		self.endButton = Button(self.frame, text="End", fg="black", height=2,width=4,command= partial(self.end_turn))
		self.endButton.grid(row=0,column=12)
		self.create_marquee()
		
	def draw(self):
		emptySpot = -1
		for x in range(0, len(self.gameField.handField)):
			if emptySpot == -1:
				if self.gameField.handField[x] == 0:
					emptySpot = x
		if emptySpot != -1:
			self.gameField.handField[emptySpot] = CardInBattle(("Mr.Man"+str(emptySpot), "Human", "Good"),(1,2,3))
			
		
	
	def getCurrentChar(self):
		for x in range(0, len(self.globalPlayers)):
			if self.globalPlayers[x].PLAYTURN ==1:
				return x
	
	def end_turn(self):
		for x in range(0, len(self.globalPlayers)):
			self.globalPlayers[x].endTurn()
			
		self.currentTurn = self.currentTurn + 1
		if self.currentTurn >= len(self.ORDER):
			self.currentTurn = 0
			self.calculateOrder()
			
		while self.ORDER[self.currentTurn].ALIVE == False:
			self.currentTurn = self.currentTurn + 1
			if self.currentTurn >= len(self.ORDER):
				self.currentTurn = 0
				self.calculateOrder()
			
		self.ORDER[self.currentTurn].startTurn()
		
		self.displayCharInfo(self.getCurrentChar())
		self.resetSkillInfo()
	
	def start_game(self):
		for x in range(0, PLAYER_SIZE):
			tempc = copy.deepcopy(globalChars[0])
			tempc.setFrame(self)
			tempc.teamSet(0)
			tempc.spotSet(x)
			self.globalPlayers.append(tempc)
			tempc.startGame()
			
		for x in range(0, ENEMY_SIZE):
			tempc = copy.deepcopy(globalChars[0])
			tempc.setFrame(self)
			tempc.teamSet(1)
			tempc.spotSet(PLAYER_SIZE+x)
			self.globalPlayers.append(tempc)
			tempc.startGame()
			
		self.calculateOrder()
		self.ORDER[self.currentTurn].startTurn()
		for x in range(0, len(self.globalPlayers)):
			if self.globalPlayers[x].PLAYTURN ==1:
				self.displayCharInfo(x)
		
		
	def spotToChar(self,spot):
		foundChar = -1

		for x in range(0, len(self.globalPlayers)):
			if self.globalPlayers[x].SPOT == spot:
				foundChar = self.globalPlayers[x]
		return foundChar
			
	def refreshCharInfo(self):
		self.display_hand_info(self.selectedPlayer)
		char = self.selectedPlayer
		self.charNameText.set(char.NAME)
		self.charHealthText.set(char.myDesc())
		self.display_hand_info(char)
			
	def displayCharInfo(self,spot):
		self.selectedPlayer = self.globalPlayers[spot]
		self.refreshCharInfo()
		

	
	def display_hand_info(self,char):
		
		for x in range(0, len(self.handBtn)):
			self.handBtn[x].config(text=x)
		
		for x in range(0, len(char.HAND.CARDS)):
			self.handBtn[x].config(text=char.HAND.CARDS[x])
		self.resetGui()
		
	def resetSkillInfo(self):
		self.selectedSkill = -1
		self.skillName = ''
		self.skillNameText.set('')
		self.skillDescText.set('')
			
	def display_skill_info(self, spot):
		if len(self.selectedPlayer.HAND.CARDS)>spot:
			self.skillName = self.selectedPlayer.HAND.CARDS[spot]
			actualSkill = getSkillFromName(self.skillName)
			if actualSkill != 'NotFound':
				self.skillNameText.set(globalSkills[actualSkill].id)
				self.skillDescText.set(globalSkills[actualSkill].info)
			else:
				print(self.skillName + ' did not load!')
		
	def display_info(self, spot, status):
		
		if status == 0:
			print ('spot') 
		elif status == 1:
			self.selectedPlayer = self.globalPlayers[spot]
			self.display_char_info(self.selectedPlayer)
			#self.display_hand_info(self.selectedPlayer)
			
		elif status == 2:
			print ('spot') 
		self.resetGui()
		
	def getCharToUseSkill(self,spot,team):
		self.selectedPlayer.useSkill(self.skillName,self.spotToChar(spot))
		self.refreshCharInfo()
		self.resetSkillInfo()
		
		
	def calculateOrder(self):
		tempSpeed = self.globalPlayers
		self.ORDER = []
		#Yea yea, I know, bubblesort is bad
		#But if speed is the same, add ACC to determine priority
		#Also theres only like 6 total players
		
		n = len(tempSpeed)
		# Traverse through all array elements
		for i in range(n):
			# Last i elements are already in place
			for j in range(0, n-i-1):
				compare0 = tempSpeed[j].SPEED
				compare1 = tempSpeed[j+1].SPEED
				# traverse the array from 0 to n-i-1
				# Swap if the element found is greater
				# than the next element
				if compare0 > compare1 :
					tempSpeed[j], tempSpeed[j+1] = tempSpeed[j+1], tempSpeed[j]
		self.ORDER = tempSpeed
		
		
		
		
class Card:
	def __init__(self,words,stats):
		self.name = words[0]
		self.type = words[1]
		self.cost = stats[0]
		self.power = stats[1]
		self.tough = stats[2]

	
class CardInBattle:
	def __init__(self,words,stats):
		self.name = words[0]
		self.type = words[1]
		self.info = words[2]
		self.cost = stats[0]
		self.power = stats[1]
		self.tough = stats[2]
		self.powerc = stats[1]
		self.toughc = stats[2]
		

class Field:
	def __init__(self):	
		self.handField = [0,0,0,0,0,0,0,0,0,0]
		self.allyField = [0,0,0,0,0,0,0,0,0,0]
		self.enemyField = [0,0,0,0,0,0,0,0,0,0]

class Skill:
	def __init__(self, v0,v1,v2,v3,v4,v5,v6,v7):
		self.id =  v0[0].get("NAME", "")
		self.SKILLNAME = v0
		self.TARGET = v1
		self.ACC = v2
		self.COST = v3
		costStr = v3[0].get("COSTSPLIT", "")
		if len(costStr) >0:
			costStr = costStr[1:-1].split(',')
		self.costArray = [int(i) for i in costStr]
		self.DAMAGE = v4
		self.DEBUFF = v5
		self.BUFF = v6
		self.DESC = v7
		self.info = v7[0].get("SKILLD", "")


class Deck:
	def __init__(self,deck):
		self.CARDS = deck
		
class Hand:
	def __init__(self,total):
	
		tempDeck = total
		newDeck = []
		for x in range(0, len(tempDeck)):
			if tempDeck[x].find("[") != -1:
				tempName = tempDeck[x][:tempDeck[x].find("[")]
				tempValue = tempDeck[x].strip()
				tempValue = int(tempValue[tempDeck[x].find("[")+1:tempDeck[x].find("]")])
				for x in range(0, tempValue):
					newDeck.append(tempName)
		self.TOTALDECK = newDeck
		self.INDECK = self.TOTALDECK
		self.SIZE = 3
		self.MAX = 10
		self.CARDS = []
		
	def draw(self,amt):
		for i in range(0,amt):
			if len(self.INDECK) > 0 and len(self.CARDS) < self.MAX:
				nextPick = randomInRange(0,len(self.INDECK)-1)
				self.CARDS.append(self.INDECK[nextPick])
				self.INDECK.pop(nextPick)
		
	def consumeSkill(self,name):
		notUsed = True
		for x in range(0, len(self.CARDS)):
			if self.CARDS[x] == name and notUsed:
				notUsed = False
				self.CARDS.pop(x)
				return True
		return False

class Buff:
	def __init__(self,attach):
		self.NAME = "Bleed"
		self.DESC = "Test"
		self.Duration = 3
		self.BUFFORDEBUFF = 0
		self.TYPE = "DAMAGE"
		self.STR = 10
		self.DAMAGETYPE = 'Physical'
		
class Character:
	def __init__(self,v0,v1,v2,v3):
		self.NAME = v0
		#self.MAXHEALTH = 100
		self.MAXHEALTH = int(v2[0].get("MAXHEALTH", ""))
		self.HEALTH = self.MAXHEALTH

		self.DAMAGE = 100
		self.SPEED = int(v2[0].get("SPEED", ""))
		self.DODGE = int(v2[0].get("DODGE", ""))
		self.ACC = int(v2[0].get("ACC", ""))
		self.TEAM = 0
		self.DECK = v3
		
		self.SPOT =-1
		self.ALIVE = 1
		self.CORPSE = 0
		self.DEBRIS = 0
		self.MANA = [0,0,0]
		#self.MANAGAIN = v2[0].get("MANAGAIN", "").split()
		costStr = v2[0].get("MANAGAIN", "")
		if len(costStr) >0:
			costStr = costStr[1:-1].split(',')
		self.MANAGAIN = [float(i) for i in costStr]
		
		costStr = v2[0].get("MANASTART", "")
		if len(costStr) >0:
			costStr = costStr[1:-1].split(',')
		self.MANASTART = [float(i) for i in costStr]
		#self.MANASTART = v2[0].get("MANASTART", "").split()
		
		#self.DAMAGESPLIT = v2[0].get("DAMAGESPLIT", "").split()
		costStr = v2[0].get("DAMAGESPLIT", "")
		if len(costStr) >0:
			costStr = costStr[1:-1].split(',')
		self.DAMAGESPLIT = [float(i) for i in costStr]
		
		self.CURRENTMANA = [0,0,0]
		self.CURRENTMAXMANA = self.MANASTART
		self.FRAME = 0
		#BRY
		self.DAMAGESPLIT = [10,10,10]
		self.TYPE = ['Beast','Carnivore']
		self.BUFFS = []
		self.DEBUFFS = []
		self.PLAYTURN = 0
		
	def setFrame(self,frame):
		self.FRAME = frame
		self.NAME = self.NAME + str(len(self.FRAME.globalPlayers))
		
	def teamSet(self,team):
		self.TEAM = team
		
	def spotSet(self,team):
		self.SPOT = team
		
	def takeDamage(self,damage,type,attacker):
		self.HEALTH = self.HEALTH - damage
		self.FRAME.marqueeAdd(self.NAME + " takes " + str(damage) + " damage!")
	def dealDamage(self,target,damage,type):
		target.takeDamage(damage,type,self)
		
	def triggerValidate(self,user,target,list):
		totalTrue = True
		for x in range(0, len(list)):
			if seperateTitle(list[x]) == 'LOWTARPER':
				per = (target.HEALTH/target.MAXHEALTH)*100
				if per > float(seperateValue(list[x])):
					totalTrue = False
				
			elif seperateTitle(list[x]) == 'HIGHTARPER':
				per = (target.HEALTH/target.MAXHEALTH)*100
				if per < float(seperateValue(list[x])):
					totalTrue = False
					
			elif seperateTitle(list[x]) == 'USERTYPE':
				canFind = False
				for i in range(0, len(user.TYPE)):
					if user.TYPE[i] == seperateValue(list[x]):
						canFind = True
				if canFind == False:
					totalTrue = False
					
			elif seperateTitle(list[x]) == 'TARTYPE':
				canFind = False
				for i in range(0, len(target.TYPE)):
					if target.TYPE[i] == seperateValue(list[x]):
						canFind = True
				if canFind == False:
					totalTrue = False
				
				
	
		return totalTrue
		
	def costCheck(self,cost):
		costMet = True
		for x in range(0, len(cost)):
			if self.CURRENTMANA[x] < cost[x]:
				costMet = False
		return costMet
		
	def costUse(self,cost):
		for x in range(0, len(cost)):
			self.CURRENTMANA[x] = self.CURRENTMANA[x] - cost[x]

	def consumeSkill(self,skillName):
		if self.HAND.consumeSkill(skillName):
			return True
		else:
			return False
		
	def useSkill(self,skill,target):
		if self.PLAYTURN == 1:
			if getSkillFromName(skill) != 'NotFound':
				skillGet = globalSkills[getSkillFromName(skill)]
				if self.costCheck(skillGet.costArray) and self.consumeSkill(skill):
				
					print("Cost met!")
					
					self.costUse(skillGet.costArray)
					skillBaseAcc = 0
					###############################ACC
					for x in range(0, len(skillGet.ACC)):
						tempStr = skillGet.ACC[x].get("BASE", "")
						skillBaseAcc = skillBaseAcc + int(tempStr)
					###############################DAMAGE
					for x in range(0, len(skillGet.DAMAGE)):
						skillTargets = []
						targetType = skillGet.DAMAGE[x].get("ATARGET", "")
						tempStr = skillGet.DAMAGE[x].get("STR", "")
						damageType = skillGet.DAMAGE[x].get("DAMAGETYPE", "")
						if targetType == 'TAR':
							skillTargets.append(target)
						elif targetType == 'SELF':
							skillTargets.append(self)
						elif targetType == 'ALLENEMY':
							skillTargets = self.getEnemies()
						elif targetType == 'ALLALLY':
							skillTargets = self.getAllies()
							
						for i in range(0, len(skillTargets)):
							if 'TRIGGER' in skillGet.DAMAGE[x]:
								tempTrig = skillGet.DAMAGE[x].get("TRIGGER","").split()

								if self.triggerValidate(self,skillTargets[i],tempTrig):
									self.dealDamage(skillTargets[i],int(tempStr),damageType)
							else:
								self.dealDamage(skillTargets[i],int(tempStr),damageType)
					##############################DEBUFF
					for x in range(0, len(skillGet.DEBUFF)):
						skillTargets = []
						targetType = skillGet.DEBUFF[x].get("ATARGET", "")
						
						if targetType == 'TAR':
							skillTargets.append(target)
						elif targetType == 'SELF':
							skillTargets.append(self)
						elif targetType == 'ALLENEMY':
							skillTargets = self.getEnemies()
						elif targetType == 'ALLALLY':
							skillTargets = self.getAllies()
					
						for i in range(0, len(skillTargets)):
							if 'TRIGGER' in skillGet.DEBUFF[x]:
								tempTrig = skillGet.DEBUFF[x].get("TRIGGER","").split()

								if self.triggerValidate(self,skillTargets[i],tempTrig):
									newDebuff = Buff(skillTargets[i])
									skillTargets[i].takeDebuff(newDebuff)
							else:
								newDebuff = Buff(skillTargets[i])
								skillTargets[i].takeDebuff(newDebuff)
					##########################################
						
				else:
					print("Cost not met!")
			
	

		
		
	def takeDebuff(self,buff):
		print(self.NAME + " got a debuff!")
		self.DEBUFFS.append(buff)
		
	def getEnemies(self):
		enes = []
		for x in range(0, len(self.FRAME.globalPlayers)):
			if self.FRAME.globalPlayers[x].TEAM != self.TEAM:
				enes.append(self.FRAME.globalPlayers[x])
		return enes
	
	def getAllies(self):
		enes = []
		for x in range(0, len(self.FRAME.globalPlayers)):
			if self.FRAME.globalPlayers[x].TEAM == self.TEAM:
				enes.append(self.FRAME.globalPlayers[x])
		return enes
	
	def manaScale(self):
		for x in range(0, len(self.CURRENTMAXMANA)):
			self.CURRENTMAXMANA[x] = self.CURRENTMAXMANA[x]+ self.MANAGAIN[x]
			self.CURRENTMAXMANA[x] = round(self.CURRENTMAXMANA[x], 2)
	
	def endTurn(self):
		if self.PLAYTURN == 1:
			self.manaScale()
		self.PLAYTURN = 0
		
	def draw(self,amt):
		self.HAND.draw(amt)
		
	def startGame(self):
		self.HAND = Hand(self.DECK)
		self.draw(3)
		
	def startTurn(self):
		self.PLAYTURN = 1
		self.FRAME.marqueeAdd(self.NAME + " turn")
		self.CURRENTMANA = self.CURRENTMAXMANA
		self.draw(1)
		
	def myDesc(self):
		infoString = ('Health: ' + str(self.HEALTH)+'/'+ str(self.MAXHEALTH) +'\n'
					  +'Speed: ' + str(self.SPEED) +' '
					  +'Acc: ' + str(self.ACC) +' '
					  +'Dodge: ' + str(self.DODGE) +'\n'
					  +'Current Mana:: ' + str(math.floor(self.CURRENTMANA[0])) +'B '
					  + str(math.floor(self.CURRENTMANA[1])) +'R '
					  + str(math.floor(self.CURRENTMANA[2])) +'Y'
					  )
		return infoString
	
#Probally inefficient
def getSkillFromName(name):
	for x in range(0, len(globalSkills)):
		if globalSkills[x].id == name:
			return x
	return 'NotFound'
		
	
def seperateInfo(given):
	if given.find("[") != -1:
		split = given[given.find("["):]
		if split.find('=') != -1:
			attList = ast.literal_eval(split)
			attPair = dict(s.split('=') for s in attList)
			return attPair
		else:
			return 0
	else:
		return 0
		
def seperateTitle(given):
	if given.find("[") != -1:
		return given[:given.find("[")]
	else:
		return 0
		
def seperateValue(given):
	if given.find("[") != -1:
		return given[given.find("[")+1:-1]
	else:
		return 0
		

def randomInRange(min,max):
	return random.randint(min,max)
		
		
def loadSkills():
	textSk = "texts/skl.txt"
	t0 = []
	t1 = []
	t2 = []
	t3 = []
	t4 = []
	t5 = []
	t6 = []
	t7 = []
	loadType = 0
	with open(textSk) as f:
	
		for line in f:
			if (line.rstrip()== "SKILLSTART[]"):
				t0 = []
				t1 = []
				t2 = []
				t3 = []
				t4 = []
				t5 = []
				t6 = []
				t7 = []
				loadType = 0
			elif (line.rstrip()== "SKILLEND[]"):
				newSk = Skill(t0,t1,t2,t3,t4,t5,t6,t7)
				globalSkills.append(newSk)
			elif (line.rstrip()== "CHARSTART[]"):
				t0 = []
				t1 = []
				t2 = []
				t3 = []
				t4 = []
				t5 = []
				t6 = []
				t7 = []
				loadType = 1
			elif (line.rstrip()== "CHAREND[]"):
			
				newCh = Character(t0[0].get("NAME", ""),t1,t2,t3)
				globalChars.append(newCh)
				
			else:
				if loadType == 0:
					category = seperateTitle(line)
					info = seperateInfo(line)
					
					if category == 'SKILLNAME':
						t0.append(info)
					elif category == 'TARGET':
						t1.append(info)
					elif category == 'ACC':
						t2.append(info)
					elif category == 'COST':
						t3.append(info)
					elif category == 'DAMAGE':
						t4.append(info)
					elif category == 'DEBUFF':
						t5.append(info)
					elif category == 'BUFF':
						t6.append(info)
					elif category == 'DESC':
						t7.append(info)
				elif loadType == 1:
					category = seperateTitle(line)
					info = seperateInfo(line)
					if category == 'CHARNAME':
						t0.append(info)
					elif category == 'DESC':
						t1.append(info)
					elif category == 'CHARSTATS':
						t2.append(info)
					elif category == 'CHARDECK':
						
						tempDeckStr = seperateValue(line.strip())
						tempDeckStr = tempDeckStr.replace("'","")

						t3 = tempDeckStr.split(',')
					elif category == 'DAMAGE':
						t4.append(info)
					elif category == 'DEBUFF':
						t5.append(info)
					elif category == 'BUFF':
						t6.append(info)
					elif category == 'DESC1':
						t7.append(info)

	
	
def main():	

	loadSkills()
	root = Tk()

	app = App(root)
	
	root.mainloop()
	root.destroy() # optional; see description below

	
if __name__ == "__main__":
    main()
