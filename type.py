import markovify
import re
import random
import time
import ast
from tkinter import *
from functools import partial

UPDATE_RATE = 1000
MARQUEE_SIZE = 10
testnum = 0
ENEMY_SIZE = 3
PLAYER_SIZE = 3
globalSkills = []
combatDecks = []
combatHands = []

class App:
	
	def __init__(self, master):
		self.frame = Frame(master,width=10,height=10,bg="", colormap="new")
		self.topBtn= [0]*3
		self.botBtn= [0]*3
		self.handBtn= [0]*10
		self.gameField = Field()
		self.create_frame()
		self.selectedSpot = -1
		self.selectedStatus = -1
		self.globalPlayers = []
		self.start_game()
		

	def resetGui(self):
		self.frame.configure(background='white')
	def create_spots(self):
		for x in range(0, 3):
			tempButton = Button(self.frame, text=x, fg="black", height=2,width=4,command= partial(self.display_info,x,2))
			tempButton.grid(row=0,column=x)
			self.topBtn[x] = tempButton
		
		for x in range(0, 3):
			tempButton = Button(self.frame, text=x, fg="black", height=2,width=4,command= partial(self.display_info,x,1))
			tempButton.grid(row=1,column=x)
			self.botBtn[x] = tempButton
			
		for x in range(0, 10):
			tempButton = Button(self.frame, text=x, fg="black", height=2,width=8,command= partial(self.display_info,x,0))
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

		
	def marquee_add(self, textStringAdd):	
		for x in range(MARQUEE_SIZE-1,0,-1):
			print ("This is "+str(x)+" taking from " + str(x-1))
			self.marqueeText[x] = self.marqueeText[x-1]
			#self.marqueeText[x] = 'wow'
		self.marqueeText[0] = textStringAdd	
		print(self.marqueeText)
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
	
	def infoAction0(self):
		if selectedStatus == 0:
			print("Play")
		
	def create_frame(self):
		self.frame.grid(row=0,column=0)
		self.create_spots()
		self.create_infoBox()
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
			#print("Card added to "+ str(emptySpot))
		
	def end_turn(self):
		global testnum
		self.marquee_add("End Turn" + str(testnum))
		testnum = testnum + 1
		self.draw()
		self.update_colors()
		loadSkills()
	
	def start_game(self):
		for x in range(0, PLAYER_SIZE):
			tempc = Character("Name"+ str(x))
			self.globalPlayers.append(tempc)

			
	def display_char_info(self,char):
		self.nameText.set(char.NAME)
	def display_hand_info(self,char):
		for x in range(0, len(self.gameField.handField)):
			self.handBtn[x].config(text=char.HAND.CARDS[x])
		self.resetGui()
	def display_info(self, spot, status):
		print(len(self.globalPlayers))
		if status == 0:
			print (spot) 
		elif status == 1:
			self.display_char_info(self.globalPlayers[spot])
			self.display_hand_info(self.globalPlayers[spot])
		elif status == 2:
			print (spot) 
		self.resetGui()
		#self.topBtn[info].destroy()

		
		# 0=cost, 1=power, 2=tough
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
		self.id = v0[0][NAME]
		self.SKILLNAME = v0
		self.TARGET = v1
		self.ACC = v2
		self.COST = v3
		self.DAMAGE = v4
		self.DEBUFF = v5
		self.BUFF = v6
		self.DESC = v7
		


class Deck:
	def __init__(self):
		self.CARDS = ['Letting Swipe','Letting Swipe','Pounce']
class Hand:
	def __init__(self):
		self.SIZE = 3
		self.MAX = 10
		self.CARDS = ['Letting Swipe','Letting Swipe','Pounce',0,0,0,0,0,0,0]

class Character:
	def __init__(self,v0):
		self.NAME = v0
		self.HEALTH = 100
		self.DAMAGE = 10
		self.SPEED = 10
		self.DODGE = 10
		self.ACC = 10
		self.TEAM = 0
		self.DECK = Deck()
		self.HAND = Hand()
	
	
#Probally inefficient
def getSkillFromName(name):
	for x in range(0, len(globalSkills)):
		if globalSkills[x].id == name:
			return x	
	return -1
		
	
	
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
			elif (line.rstrip()== "SKILLEND[]"):
				newSk = Skill(t0,t1,t2,t3,t4,t5,t6,t7)
				globalSkills.append(newSk)
			else:
				category = seperateTitle(line)
				info = seperateInfo(line)
				#print(info)
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
				

	
	
def main():	

	
	root = Tk()

	app = App(root)

	root.mainloop()
	root.destroy() # optional; see description below

	
if __name__ == "__main__":
    main()
