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

registered = []

serveremotes = []


dictionary = {}

def sendReaction(message, l):
	m = brain.createMessage()
	p = m
	for i in serveremotes:
		p = p.replace(i, dictionary[i])

	e = ""
	for char in p:
		if(char in emoji.UNICODE_EMOJI or char in dictionary.keys() or char == "\n" or char in specialcases ):
			e += char

	e.replace("\n", "n")
	prob = random.random()
	if len(e) <= l and len(set(e)) == len(e) and not "\n" in m:
		return e
	else:
		e = e.replace("n", "")
		e = e.replace("\n", "")
		e = "".join(set(e))
		if len(e) <= l:
			return e
		else:
			return e[0:l]

# Read msgpack file
with open("dictionary.msgpack", "rb") as f:
	byte_data = f.read()

dictionary = msgpack.unpackb(byte_data)

dictionary_inv = {v: k for k, v in dictionary.items()}

print(dictionary)

@client.event
async def on_ready():
	customActivity = discord.Game("😳")
	await client.change_presence(status=discord.Status.online, activity=customActivity)

	print("The bot is ready")
	


@client.event
async def on_message(message):
	global registered
	#register all server emotes
	if not message.guild.id in registered:
		registered.append(message.guild.id)
		for i in message.guild.emojis:
			if not i.animated:
				serveremotes.append('<:%s:%s>' % (i.name, i.id))
		registered.append(message.guild.id)


	#send reaction if timothy is in name
	if "timothy" in message.content.lower():
		e = sendReaction(message, 1)
		for em in e:
			try:
				await message.add_reaction(dictionary_inv[em])
			except:
				try:
					await message.add_reaction(em)
				except:
					pass

	#send reaction if timothy is in name
	if "flushedtaco" in message.content.lower().replace(" ", ""):
		try:
			await message.add_reaction("<:flushedtaco:786270715187167242>")
		except:
			pass

	#send message if @ ed
	if f'<@!{client.user.id}>' in message.content or f'<@{client.user.id}>' in message.content:
		try:
			await message.channel.send(brain.createMessage())
		except:
			ignore.append(message.channel)
		return

	if message.author == client.user or message.channel in ignore:
		return


	prob = random.random()
	print(round(prob * 1000)/1000.0)
	
	#send message or reaction
	if (message.channel.id == 711793617529995297 and prob < .25) or prob <= 0.01:
		m = brain.createMessage()
		p = m
		for i in serveremotes:
			p = p.replace(i, dictionary[i])

		e = ""
		for char in p:
			if(char in emoji.UNICODE_EMOJI or char in dictionary.keys() or char == "\n" or char in specialcases ):
				e += char
		prob = random.random()
		if len(e) <= 1 and len(set(e)) == len(e) and prob < .25 and not "\n" in e:
			for em in e:
				try:
					await message.add_reaction(dictionary_inv[em])
				except:
					try:	
						await message.add_reaction(em)
					except:
						pass
		else:
			try:	
				await message.channel.send(m)
			except:
				ignore.append(message.channel)

	#learning
	if learnnew and not message.author.bot:
		processed = message.content

		for i in dictionary_inv.keys():
			processed = processed.replace(i, "")

		for i in serveremotes:
			try:
				processed = processed.replace(i, dictionary[i])
			except:
				print("adding " + i)
				#if something is not in the dictionary add it
				dictionary[i] = chr(len(dictionary.keys()) + 200)
				processed = processed.replace(i, dictionary[i])
				# Write msgpack file
				with open("dictionary.msgpack", "wb") as f:
					packed = msgpack.packb(dictionary)
					f.write(packed)
		end = ""
		for char in processed:
			if(char in emoji.UNICODE_EMOJI or char in dictionary_inv.keys() or char == "\n" or char in specialcases):
				end += char

		#learning and writing, and maybe reacting
		end = end.replace("\n", "n")
		if end.replace('n', "") != "" and str(message.author) != "MysticalApple#0085":
			end = ':%s,' % (end.strip("n"))
			with open('messages.txt', 'a') as f:
				f.write(end + "\n")
			print(message.content)
			print(end)

			if random.random() < .25:
				e = sendReaction(message, 1)
				for em in e:
					try:
						await message.add_reaction(dictionary_inv[em])
					except:
						try:
							await message.add_reaction(em)
						except:
							pass








client.run("")
