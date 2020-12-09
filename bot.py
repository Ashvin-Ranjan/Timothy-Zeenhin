import discord
import discordhelp
import json
import emoji
import msgpack

learnnew = True

ratio = []

with open("ratio.txt", "r") as f:
	ratio = f.readlines()

for i in range(len(ratio)):
	ratio[i] = int(ratio[i])

dictionary = {}

# Read msgpack file
with open("dictionary.msgpack", "rb") as f:
	byte_data = f.read()

dictionary = msgpack.unpackb(byte_data)

client = discord.Client()

replacements = ['{', '|', '}', '~', '␡', '\x80', '\x81', '\x82', '\x83', '\x84', '\x85', '\x86', '\x87', '\x88', '\x89', '\x8a', '\x8b', '\x8c', '\x8d', '\x8e', '\x8f', '\x90', '\x91', '\x92', '\x93', '\x94', '\x95', '\x96', '\x97', '\x98', '\x99', '\x9a', '\x9b', '\x9c', '\x9d', '\x9e', '\x9f', '', '', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '\xad', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ', 'Ā']


serveremotes = []

@client.event
async def on_ready():
	customActivity = discord.Game("😳")
	await client.change_presence(status=discord.Status.online, activity=customActivity)

	print("The bot is ready")
	
@client.event
async def on_message(message):
	if len(serveremotes) != message.guild.emojis:
		for i in message.guild.emojis:
			if not i.animated:
				serveremotes.append('<:%s:%s>' % (i.name, i.id))

	print(message.content)
	if message.author == client.user:
		return

	if learnnew:

		processed = message.content

		for i in replacements:
			processed = processed.replace(i, "")

		for i in serveremotes:
			try:
				processed = processed.replace(i, dictionary[i])
			except:
				dictionary[i] = replacements[len(dictionary.keys())]
				processed = processed.replace(i, dictionary[i])
				# Write msgpack file
				with open("dictionary.msgpack", "wb") as f:
					packed = msgpack.packb(dictionary)
					f.write(packed)

		end = ""
		for char in processed:
			if(char in emoji.UNICODE_EMOJI or char in replacements or char == "\n"):
				end += char

		end = end.replace("\n", "n")
		if end.replace('n', "") != "":
			ratio[0] += 1
			end = ":" + end + ","
			with open('messages.txt', 'a') as f:
				f.write(end + "\n")
			print(end)
		else:
			ratio[1] += 1

		with open("ratio.txt", "w") as f:
			f.write(str(ratio[0]) + "\n" + str(ratio[1]))








client.run("Nzg2MjY5NTYxOTU1NTQ5Mjc0.X9D8lw.4Qa-vulXVuhOUE4Xor38Ru0PLbQ")