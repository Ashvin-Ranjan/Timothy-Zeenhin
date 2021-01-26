import discord
import discordhelp
import json
import emoji
import msgpack
import brain
import random
import asyncio

key = ""

with open("key.txt", "r") as f:
	key = f.read().strip()

ignore = [713649228412616714]

learnnew = True

specialcases = ["🦭", "🫁"]

client = discord.Client()

registered = False

bots_allowed = [723063395280224257, 766064505079726140]

dictionary = {}

# Read msgpack file
with open("dictionary.msgpack", "rb") as f:
	byte_data = f.read()

dictionary = msgpack.unpackb(byte_data)

dictionary_inv = {v: k for k, v in dictionary.items()}

dictionary = {v: k for k, v in dictionary_inv.items()}

with open("dictionary.msgpack", "wb") as f:
	packed = msgpack.packb(dictionary)
	f.write(packed)

#print(dictionary)

def update_emotes():
	global dictionary_inv, dictionary
	serveremotes = []
	for guild in client.guilds:
		for i in guild.emojis:
			serveremotes.append('<:%s:%s>' % (i.name, i.id))

	for emote in serveremotes:
		if emote not in dictionary:
			#if something is not in the dictionary add it
			indexkey = 200
			newkey = chr(indexkey)
			while newkey in dictionary_inv:
				indexkey += 1
				newkey = chr(indexkey)
			dictionary[emote] = newkey
			dictionary_inv = {v: k for k, v in dictionary.items()}
			print("adding " + emote + " as " + newkey)
			# Write msgpack file
			with open("dictionary.msgpack", "wb") as f:
				packed = msgpack.packb(dictionary)
				f.write(packed)

	remove = []
	for key in dictionary.keys():
		if key not in serveremotes:
			remove.append(key)

	for rem in remove:
		print("removing", rem)
		dictionary.pop(rem)

	dictionary_inv = {v: k for k, v in dictionary.items()}

	with open("dictionary.msgpack", "wb") as f:
		packed = msgpack.packb(dictionary)
		f.write(packed)

@client.event
async def on_ready():
	customActivity = discord.Game("😳")
	await client.change_presence(status=discord.Status.online, activity=customActivity)
	
	update_emotes()

	print("The bot is ready")
	

@client.event
async def on_message(message):
	global dictionary_inv, dictionary
	#register all server emotes
	update_emotes()

	#send message if @ ed
	if f'<@!{client.user.id}>' in message.content or f'<@{client.user.id}>' in message.content:
		try:
			async with message.channel.typing():
				await asyncio.sleep(random.random()/4)
				await message.channel.send(brain.createMessage())
		except:
			pass

	if message.author == client.user or message.channel in ignore:
		return


	prob = random.random()
	
	#send message or reaction
	if (message.channel.id == 711793617529995297 and (prob < .1 or message.author.id == 723063395280224257)) or prob <= 0.01:
		m = brain.createMessage()
		p = m
		for i in dictionary.keys():
			p = p.replace(i, dictionary[i])

		e = ""
		for char in p:
			if(char in emoji.UNICODE_EMOJI or char in dictionary.keys() or char == "\n" or char in specialcases ):
				e += char
		prob = random.random()
		
		
		try:
			async with message.channel.typing():
				await asyncio.sleep(random.random())
				await message.channel.send(m)
		except:
			ignore.append(message.channel)

	#learning
	if learnnew:
		processed = message.content

		for i in dictionary_inv.keys():
			processed = processed.replace(i, "")

		for i in dictionary.keys():
			processed = processed.replace(i, dictionary[i])
			
		end = ""
		for char in processed:
			if(char in emoji.UNICODE_EMOJI or char in dictionary_inv.keys() or char == "\n" or char in specialcases):
				end += char

		#learning and writing, and maybe reacting
		end = end.replace("\n", "n")
		if end.replace('n', "") != "" and (not message.author.bot or message.author.id in bots_allowed):
			end = ':%s,' % (end.strip("n"))
			with open('messages.txt', 'a', encoding="utf-8") as f:
				f.write(end + "\n")
			print(message.content)
			print(end)








client.run(key)