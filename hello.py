import markovify
import re
book = input('Enter text name: ')
str1 = "texts/"
str2 = str1+book
str3 = str2+".txt"
save0 = 'out.txt'
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
			"Katarina"]
placeHolder = "INSERTNAMEHERE"

def remove_non_ascii_1(text):
	new_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', text)
	print(new_str)
	return new_str
	string = open(str3).read()
	new_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', string)
	open(str3, 'w').write(new_str)
	
#with open(str3,encoding="utf8") as f:
with open(str3) as f:
#with open(str3) as f:
	text = f.read()
	if replaceName == True:
		for x in namelist:
			text = text.replace(x, placeHolder)

# Build the model.
#text_model = markovify.Text(text)
text_model = markovify.NewlineText(text)

# Print five randomly-generated sentences
output = open(save0, 'w')
for i in range(200):
	#text_model.make_short_sentence(140)
	#print(text_model.make_sentence(tries=20),file=output)
	print(text_model.make_short_sentence(200),file=output)
	
print('Saved to '+save0)
# Python 3.x
# Print three randomly-generated sentences of no more than 140 characters
#for i in range(3):
   #text_model.make_sentence()
#print(text_model.make_short_sentence(140))