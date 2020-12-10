import msgpack
import random

dictionary = {}
ratio = []



with open("ratio.txt", "r") as f:
	ratio = f.readlines()

for i in range(len(ratio)):
	ratio[i] = int(ratio[i])

# Read msgpack file
with open("dictionary.msgpack", "rb") as f:
	byte_data = f.read()

dictionary = msgpack.unpackb(byte_data)

dictionary_inv = {v: k for k, v in dictionary.items()}


def generateChainDict(l):
	out = {}
	for message in l:
		for i,char in enumerate(message):
			if not char in out:
				out[char] = {}
			if char == ",":
				pass
			else:
				try:
					out[char][message[i+1]] += 1
				except:
					out[char][message[i+1]] = 1


	return out

def createMessage():
	messages = []
	with open("messages.txt", "r", encoding="utf-8") as f:
		messages = f.readlines()

	clean = []
	for i in messages:
		if i != "":
			clean.append(i.strip())

	messages = clean[:]

	message_data = generateChainDict(messages)

	cont = True

	out = ":"

	while cont:
		s = 0
		for i in message_data[out[len(out) -1]].keys():
			s += message_data[out[len(out) -1]][i]

		rand = random.randint(0, s)

		for i in message_data[out[len(out) -1]].keys():
			rand -= message_data[out[len(out) -1]][i]
			if rand <= 0:
				out += i
				if i == ",":
					cont = False
				break



	return decode(out)




def decode(s):
	out = ""
	for char in s[1: len(s) -1]:
		if char == "n":
			out += "\n"
		else:
			try:
				out += dictionary_inv[char]
			except:
				out += char

	return out

print(createMessage())