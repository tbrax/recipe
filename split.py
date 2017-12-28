import markovify
import re
import random
save0 = 'title.txt'
save1 = 'initial.txt'
save2 = 'ability.txt'
save3 = 'stats0.txt'
save4 = 'stats1.txt'
textChamp = "texts/champ.txt"
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
placeHolder = "INSERTNAMEHERE"
lastString = ""
case = 0
lastCase = 0
output0 = open(save0, 'w')
output1 = open(save1, 'w')
output2 = open(save2, 'w')
output3 = open(save3, 'w')
output4 = open(save4, 'w')
with open(textChamp) as f:
	lines = f.readlines()
	last = lines[-1]
	#for line in f.readlines():
	for i in range(0, len(lines)):
		line = lines[i]
		if line:
			if not re.match(r'^\s*$', line):
				case = 0
				if lastCase == 0:
					for x in namelist:
						if line.rstrip() == x.upper():
							case = 1
							print(line,file=output0)
					if (line.rstrip())[-1] == ':':
						case = 2
						print(line,file=output3)
					if lastString.find(line.rstrip()) != -1:	
						print(lastString,file=output1)
					else:
						if case == 0:
							if line is not last:
								ii = 1
								while re.match(r'^\s*$', lines[i+ii]):
									ii = ii + 1
								if line.find(lines[i+ii].rstrip()) == -1:
									
									print(line,file=output2)
							else:
								print(line,file=output2)
				elif lastCase == 1:
					print(line,file=output0)
				elif lastCase == 2:
					print(line,file=output4)
				#print("Compare "+ lastString+" and "+ line)
				
				lastCase = case
			lastString = line
	


