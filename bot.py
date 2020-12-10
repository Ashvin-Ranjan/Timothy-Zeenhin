import discord
import discordhelp
import json
import emoji
import msgpack
import brain
import random


ignore = []

learnnew = True

specialcases = ["🦭", "🫁"]

def generateInterval():
	return random.randint(70, 100)

client = discord.Client()

replacements = ['{', '|', '}', '~', '␡', '\x80', '\x81', '\x82', '\x83', '\x84', '\x85', '\x86', '\x87', '\x88', '\x89', '\x8a', '\x8b', '\x8c', '\x8d', '\x8e', '\x8f', '\x90', '\x91', '\x92', '\x93', '\x94', '\x95', '\x96', '\x97', '\x98', '\x99', '\x9a', '\x9b', '\x9c', '\x9d', '\x9e', '\x9f', '', '', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '\xad', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ', 'Ā']

registered = False

serveremotes = []

message_timer = generateInterval()

dictionary = {}

# Read msgpack file
with open("dictionary.msgpack", "rb") as f:
	byte_data = f.read()

dictionary = msgpack.unpackb(byte_data)

print(message_timer)


@client.event
async def on_ready():
	customActivity = discord.Game("😳")
	await client.change_presence(status=discord.Status.online, activity=customActivity)

	print("The bot is ready")
	


@client.event
async def on_message(message):
	global registered, message_timer
	if not registered:
		registered = True
		for i in message.guild.emojis:
			if not i.animated:
				serveremotes.append('<:%s:%s>' % (i.name, i.id))


	if f'<@!{client.user.id}>' in message.content:
		try:
			await message.channel.send(brain.createMessage())
		except:
			ignore.append(message.channel)

	if message.author == client.user or message.author.bot or message.channel in ignore or str(message.author) == "MysticalApple#0085":
		return


	message_timer -= 1
	print(message_timer)

	if message_timer <= 0:
		message_timer = generateInterval()
		m = brain.createMessage()
		p = m
		for i in serveremotes:
			p = p.replace(i, dictionary[i])

		e = ""
		for char in p:
			if(char in emoji.UNICODE_EMOJI or char in replacements or char == "\n" or char in specialcases):
				e += char
		prob = random.random()
		if len(e) < 3 and len(set(e)) == len(e) and prob < .75 and not "\n" in e:
			dictionary_inv = {v: k for k, v in dictionary.items()}
			for em in e:
				try:
					await message.add_reaction(dictionary_inv[em])
				except:
					try:	
						await message.add_reaction(dictionary_inv[e])
					except:
						ignore.append(message.channel)
						message_timer = 1
						print(message_timer)			
		else:
			try:	
				await message.channel.send(m)
			except:
				ignore.append(message.channel)
				message_timer = 1
				print(message_timer)

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
			if(char in emoji.UNICODE_EMOJI or char in replacements or char == "\n" or char in specialcases):
				end += char

		end = end.replace("\n", "n")
		if end.replace('n', "") != "":
			end = ":" + end + ","
			with open('messages.txt', 'a') as f:
				f.write(end + "\n")
			print(message.content)
			print(end)








client.run("")
