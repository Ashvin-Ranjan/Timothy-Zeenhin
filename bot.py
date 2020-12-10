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

client = discord.Client()

replacements = ['{', '|', '}', '~', '␡', '\x80', '\x81', '\x82', '\x83', '\x84', '\x85', '\x86', '\x87', '\x88', '\x89', '\x8a', '\x8b', '\x8c', '\x8d', '\x8e', '\x8f', '\x90', '\x91', '\x92', '\x93', '\x94', '\x95', '\x96', '\x97', '\x98', '\x99', '\x9a', '\x9b', '\x9c', '\x9d', '\x9e', '\x9f', '', '', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '\xad', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ', 'Ā']

registered = False

serveremotes = []


dictionary = {}

# Read msgpack file
with open("dictionary.msgpack", "rb") as f:
	byte_data = f.read()

dictionary = msgpack.unpackb(byte_data)

dictionary_inv = {v: k for k, v in dictionary.items()}



@client.event
async def on_ready():
	customActivity = discord.Game("😳")
	await client.change_presence(status=discord.Status.online, activity=customActivity)

	print("The bot is ready")
	


@client.event
async def on_message(message):
	global registered
	if not registered:
		registered = True
		for i in message.guild.emojis:
			if not i.animated:
				serveremotes.append('<:%s:%s>' % (i.name, i.id))

	if message.author == client.user:
		return

	if f'<@!{client.user.id}>' in message.content or f'<@{client.user.id}>' in message.content:
		try:
			await message.channel.send(brain.createMessage())
		except:
			ignore.append(message.channel)

	if message.author == client.user or message.author.bot or message.channel in ignore:
		return

	if "timothy" in message.content:
		m = brain.createMessage()
		p = m
		for i in serveremotes:
			p = p.replace(i, dictionary[i])

		e = ""
		for char in p:
			if(char in emoji.UNICODE_EMOJI or char in replacements or char == "\n" or char in specialcases ):
				e += char

		e.replace("\n", "n")
		prob = random.random()
		if len(e) <= 5 and len(set(e)) == len(e) and not "\n" in m:
			for em in e:
				try:
					await message.add_reaction(dictionary_inv[em])
				except:
					await message.add_reaction(em)
		else:
			e = e.replace("n", "")
			e = "".join(set(e))
			if len(e) <= 5:
				for em in e:
					try:
						await message.add_reaction(dictionary_inv[em])
					except:
						await message.add_reaction(em)
			else:
				for em in e[0:5]:
					try:
						await message.add_reaction(dictionary_inv[em])
					except:
						await message.add_reaction(em)

	prob = random.random()
	print(prob)

	if (message.channel.id == 711793617529995297 and prob < .25) or prob < 0.05:
		m = brain.createMessage()
		p = m
		for i in serveremotes:
			p = p.replace(i, dictionary[i])

		e = ""
		for char in p:
			if(char in emoji.UNICODE_EMOJI or char in replacements or char == "\n" or char in specialcases ):
				e += char
		prob = random.random()
		if len(e) <= 5 and len(set(e)) == len(e) and prob < .75 and not "\n" in e:
			for em in e:
				try:
					await message.add_reaction(dictionary_inv[em])
				except:
					try:	
						await message.add_reaction(em)
					except:
						ignore.append(message.channel)		
		else:
			try:	
				await message.channel.send(m)
			except:
				ignore.append(message.channel)

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
		if end.replace('n', "") != "" and str(message.author) != "MysticalApple#0085":
			end = ":" + end + ","
			with open('messages.txt', 'a') as f:
				f.write(end + "\n")
			print(message.content)
			print(end)








client.run("")