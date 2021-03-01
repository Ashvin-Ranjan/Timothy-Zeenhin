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

rates = {}

# Read msgpack file
with open("rates.msgpack", "rb") as f:
	byte_data = f.read()

rates = msgpack.unpackb(byte_data)

validated = {}

# Read msgpack file
with open("validated.msgpack", "rb") as f:
	byte_data = f.read()

validated = msgpack.unpackb(byte_data)

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
	global dictionary_inv, dictionary, rates, validated
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

	if message.content.split(" ")[0].strip().startswith("~set") and len(message.content.split(" ")) == 3:
		try:
			if(validated[str(message.author.id)]):
				rates[str(int(message.content.split(" ")[1].strip()))] = float(message.content.split(" ")[2].strip())
				with open("rates.msgpack", "wb") as f:
					packed = msgpack.packb(rates)
					f.write(packed)
				await message.add_reaction("✅")
			else:
				await message.add_reaction("❌")
		except:
			await message.add_reaction("❌")

		return

	if message.content.split(" ")[0].strip().startswith("~validate") and len(message.content.split(" ")) == 2 and message.author.id == 384499090865782785:
		try:
			validated[str(int(message.content.split(" ")[1].strip()))] = True
			with open("validated.msgpack", "wb") as f:
				packed = msgpack.packb(validated)
				f.write(packed)
			await message.add_reaction("✅")
		except Exception as e:
			print(e)
			await message.add_reaction("❌")

		return

	if message.content.split(" ")[0].strip().startswith("~devalidate") and len(message.content.split(" ")) == 2 and message.author.id == 384499090865782785:
		try:
			validated[str(int(message.content.split(" ")[1].strip()))] = False
			with open("validated.msgpack", "wb") as f:
				packed = msgpack.packb(validated)
				f.write(packed)
			await message.add_reaction("✅")
		except Exception as e:
			print(e)
			await message.add_reaction("❌")

		return

	#send message or reaction
	rate = 0.01
	try:
		rate = rates[str(message.channel.id)]
	except:
		pass
	if prob <= rate:
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