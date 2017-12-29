import markovify
import re
import random
#book = input('Enter text name: ')
#str1 = "texts/"
#str2 = str1+book
#str3 = str2+".txt"
save0 = 'out.txt'

textAbility = "texts/ability.txt"
textChamp = "texts/champ.txt"
textInitial = "texts/initial.txt"
textStats0 = "texts/stats0.txt"
textStats1 = "texts/stats1.txt"
# Get raw text as string.
replaceName = True
namelist = ["Aatrox", "Ahri", "Akali", "Alistar","Amumu","Anivia",
			"Annie", "Ashe", "Aurelion Sol", "Azir", "Bard", "Blitzcrank",
			"Brand", "Braum", "Caitlyn", "Camille", "Cassiopeia",
			"Cho'Gath","Corki","Darius","Diana","Dr. Mundo","Draven",
			"Ekko","Elise", "Evelynn","Ezreal","Fiddlesticks","Fiora",
			"Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas",
			"Graves", "Hecarim", "Heimerdinger", "Illaoi",
			"Irelia", "Ivern", "Janna", "Jarvan IV", "Jax", "Jayce",
			"Jhin", "Jinx", "Kalista", "Karma", "Karthus", "Kassadin",
			"Katarina", "Kayle", "Kayn", "Kennen", "Kha'Zix", "Kindred", 
			"Kled", "Kog'Maw", "LeBlanc", "Lee Sin", "Leona", "Lissandra",
			"Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai",
			"Master Yi", "Miss Fortune", "Mordekaiser", "Morgana",
			"Nami", "Nasus", "Nautilus", "Nidalee", "Nocturne",
			"Nunu","Olaf", "Orianna", "Ornn", "Pantheon", "Poppy",
			"Quinn", "Rakan", "Rammus", "Rek'Sai", "Renekton", "Rengar",
			"Riven", "Rumble", "Ryze", "Sejuani", "Shaco", "Shen", 
			"Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka",
			"Swain", "Syndra", "Tahm Kench", "Taliyah", "Talon", "Taric", "Teemo",
			"Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate", "Twitch",
			"Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vi ",
			"Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", 
			"Xin Zhao", "Yasuo", "Yorick", "Zac", "Zed", "Ziggs", "Zilean", "Zoe", "Zyra"]
			
			
totalNamelist = ["Aatrox", "Ahri", "Akali", "Alistar","Amumu","Anivia",
			"Annie", "Ashe", "Aurelion Sol", "Azir", "Bard", "Blitzcrank",
			"Brand", "Braum", "Caitlyn", "Camille", "Cassiopeia",
			"Cho'Gath","Corki","Darius","Diana","Dr. Mundo","Draven",
			"Ekko","Elise", "Evelynn","Ezreal","Fiddlesticks","Fiora",
			"Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas",
			"Graves", "Hecarim", "Heimerdinger", "Illaoi",
			"Irelia", "Ivern", "Janna", "Jarvan IV", "Jax", "Jayce",
			"Jhin", "Jinx", "Kalista", "Karma", "Karthus", "Kassadin",
			"Katarina", "Kayle", "Kayn", "Kennen", "Kha'Zix", "Kindred", 
			"Kled", "Kog'Maw", "LeBlanc", "Lee Sin", "Leona", "Lissandra",
			"Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai",
			"Master Yi", "Miss Fortune", "Mordekaiser", "Morgana",
			"Nami", "Nasus", "Nautilus", "Nidalee", "Nocturne",
			"Nunu","Olaf", "Orianna", "Ornn", "Pantheon", "Poppy",
			"Quinn", "Rakan", "Rammus", "Rek'Sai", "Renekton", "Rengar",
			"Riven", "Rumble", "Ryze", "Sejuani", "Shaco", "Shen", 
			"Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka",
			"Swain", "Syndra", "Tahm Kench", "Taliyah", "Talon", "Taric", "Teemo",
			"Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate", "Twitch",
			"Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vi ",
			"Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", 
			"Xin Zhao", "Yasuo", "Yorick", "Zac", "Zed", "Ziggs", "Zilean", "Zoe", "Zyra", "Vi's",
			"Wolf", "Lamb", "Tibbers"]
placeHolder = "INSERTNAMEHERE"

#def remove_non_ascii_1(text):
	#new_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', text)
	#print(new_str)
	#return new_str
	#string = open(str3).read()
	#new_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', string)
	#open(str3, 'w').write(new_str)
	
#with open(str3,encoding="utf8") as f:
#with open(str3) as f:



###############
def addAbilityDesc(t0,output,thisChoice):
	abilityLine = t0.make_short_sentence(200)
	abilityLineReplace = abilityLine.replace(placeHolder, thisChoice)
	print(abilityLineReplace,file=output)
	
#########################
def addAbilityDetails(t2,t3,output):
	statLevel = t2.make_short_sentence(150)
	while statLevel is None:
		statLevel = t2.make_short_sentence(150)	
	if statLevel.find("PER") != -1:
		if random.randint(0,5) > 0:
			statLevel = statLevel[:statLevel.find("PER")-1]
			
	if random.randint(0,7) > 0:
		statLevel = statLevel.replace('TORNADO ', '')
	
	if statLevel[-1] != ':':
			statLevel = statLevel + ':'
	
	print(statLevel,file=output)
	statNumbers = t3.make_short_sentence(150)
	lastStatType = 0
	a = ['current', 'maximum', 'mana', 'bonus', 'AD', 'AP']
	if statNumbers.find("%") != -1 and lastStatType == 0:
		if not any(x in statNumbers for x in a):
			statNumbers = re.sub('[%]', '', statNumbers)
	#else:
		#if any(x in statNumbers for x in a):
			#statNumbers = statNumbers + '%'
			


			
	print(statNumbers,file=output)
	print("",file=output)
	


def createChamp(t0,t1,t2,t3,output):
	thisChoice = random.choice(namelist)
	print(thisChoice,file=output)
	print("",file=output)
	for i in range(4):
		print(t1.make_short_sentence(200),file=output)
		addAbilityDesc(t0,output,thisChoice)
		addAbilityDesc(t0,output,thisChoice)
		
		print("",file=output)
		addAbilityDetails(t2,t3,output)
		addAbilityDetails(t2,t3,output)

		
def main():	
	with open(textInitial) as f1:
		text1 = f1.read()
	with open(textStats0) as f2:
		text2 = f2.read()
	with open(textStats1) as f3:
		text3 = f3.read()
	
	with open(textAbility) as f0:
		text = f0.read()
		if replaceName == True:
			for x in totalNamelist:
				if x != " Vi ":
					text = text.replace(x, placeHolder)
				else:
					text = text.replace(x, ""+placeHolder+" ")		
#text_model = markovify.Text(text)
	text_model = markovify.NewlineText(text)
	text_model1 = markovify.NewlineText(text1)
	text_model2 = markovify.NewlineText(text2)
	text_model3 = markovify.NewlineText(text3)
	output = open(save0, 'w')
	for i in range(50):
		createChamp(text_model,text_model1,text_model2,text_model3,output)
	
	#text_model.make_short_sentence(140)
	#print(text_model.make_sentence(tries=20),file=output)
	print('Saved to '+save0)
	
if __name__ == "__main__":
    main()
# Python 3.x
# Print three randomly-generated sentences of no more than 140 characters
#for i in range(3):
   #text_model.make_sentence()
#print(text_model.make_short_sentence(140))