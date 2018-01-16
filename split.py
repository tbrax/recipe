import markovify
import re
import random
save0 = 'construct/title.txt'
save1 = 'construct/initial.txt'
save2 = 'construct/ability.txt'
save3 = 'construct/stats0.txt'
save4 = 'construct/stats1.txt'
save5 = 'construct/abilityname.txt'
save6 = 'construct/quote.txt'
textChamp = "texts/champ.txt"
textHero0 = "texts/hero0.txt"
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
			"Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vii",
			"Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", 
			"Xin Zhao", "Yasuo", "Yorick", "Zac", "Zed", "Ziggs", "Zilean", "Zoe", "Zyra",
			"Abaddon","Alchemist","Axxe","Beastmaster"]


output0 = open(save0, 'w')
output0.truncate()
output1 = open(save1, 'w')
output1.truncate()
output2 = open(save2, 'w')
output2.truncate()
output3 = open(save3, 'w')
output3.truncate()
output4 = open(save4, 'w')
output4.truncate()
output5 = open(save5, 'w')
output5.truncate()
output6 = open(save6, 'w')
output6.truncate()
abilityPlaceHolder = "ABILITYREPLACE"
def splitText(textGiven):
	lastString = ""
	case = 0
	lastCase = 0
	placeHolder = "INSERTNAMEHERE"
	with open(textGiven) as f:
		lines = f.readlines()
		last = lines[-1]
		#last = len(lines)-1
		#for line in f.readlines():
		recentAbilityName = ''
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
							recentAbilityName = line.rstrip()
							print(recentAbilityName,file=output5)
							lastText = lastString
							lastText = lastText.replace(recentAbilityName,abilityPlaceHolder)
							#print("Replace '"+recentAbilityName+"' in '"+lastText+"'")
							print(lastText,file=output1)
						if line.rstrip() == 'QUOTESTART':
							case = 3
						else:
							if case == 0:
								if i<len(lines)-1:
									#print("l "+ str(len(lines)-1))
									#print("l "+ str(last))
									#print(i)
									ii = 1
									while re.match(r'^\s*$', lines[i+ii]):
										if len(lines) >(i+ii-1):
											ii = ii + 1
									if line.find(lines[i+ii].rstrip()) == -1:
										lineText = line
										lineText = lineText.replace(recentAbilityName, abilityPlaceHolder)
										print(lineText,file=output2)
								else:
									print(line,file=output2)
					elif lastCase == 1:
						print(line,file=output0)
					elif lastCase == 2:
						print(line,file=output4)
					elif lastCase == 3:
						if line.rstrip() == 'QUOTEEND':
							case = 0
						else:
							case = 3
							if '"' in line:
								actQuoteLine = line
								actQuoteLine = actQuoteLine.replace('"', '');
								print(actQuoteLine,file=output6)
					#print("Compare "+ lastString+" and "+ line)
					
					lastCase = case
				lastString = line
			
splitText(textChamp)
splitText(textHero0)
print("File Split")


