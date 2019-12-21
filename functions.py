import re
from emoji import UNICODE_EMOJI

with open('chat.txt', 'r') as file:
	data = file.read()

class Item:
	def __init__(self, parent):
		self.nodes = []
		self.parent = parent
		self.has_nodes = False

	def add_node(self, node):
		self.nodes.append(node)

	def remove_nodes(self):
		del(self.nodes)

	def __repr__(self):
		try:
			return f"<Parent {self.parent}\n Messages: {self.nodes}>"
		except AttributeError:
			return f"<Parent {self.parent}"


stack = []

def containsDate(s):
	pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), '
	#pattern = '^([0-3][0-9]/[0-9][0-9]/[0-2]0[0-9][0-9], ([0-9]:[0-9][0-9]) [a-z][a-z] -'
	result = re.match(pattern, s)
	if result:
		return True
	return False


def containsAuthor(s):
	patterns = [
		'([\w]+):',                        # First Name
		'([\w]+[\s]+[\w]+):',              # First Name + Last Name
		'([\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
		'([+]\d{2} \d{5} \d{5}):',         # Mobile Number (India)
		'([+]\d{2} \d{3} \d{3} \d{4}):',   # Mobile Number (US)
		'([+]\d{2} \d{4} \d{7})'           # Mobile Number (Europe)
	]
	pattern = '^' + '|'.join(patterns)
	result = re.match(pattern, s)
	if result:
		return True
	return False

def containsEmoji(s):
	for i in s:
		if i in UNICODE_EMOJI:
			return True
	return False

def getDataPoint(line):
	# line = 18/06/17, 22:47 - Loki: Why do you have 2 numbers, Banner?

	splitLine = line.split(' - ') # splitLine = ['18/06/17, 22:47', 'Loki: Why do you have 2 numbers, Banner?']

	dateTime = splitLine[0] # dateTime = '18/06/17, 22:47'

	date, time = dateTime.split(', ') # date = '18/06/17'; time = '22:47'

	message = ' '.join(splitLine[1:]) # message = 'Loki: Why do you have 2 numbers, Banner?'
    
	if containsAuthor(message) or containsEmoji(message): # True
		splitMessage = message.split(': ') # splitMessage = ['Loki', 'Why do you have 2 numbers, Banner?']
		author = splitMessage[0] # author = 'Loki'
		message = ' '.join(splitMessage[1:]) # message = 'Why do you have 2 numbers, Banner?'
	else:
		author = None
	return date, time, author, message


for i in data.split('\n'):
	if containsDate(i):
		stack.append(Item(i))
	else:
		try:
			stack[-1].has_nodes = True
			stack[-1].add_node(i)
			
		except:
			pass

# for i in data.split('\n'):
# 	if containsAuthor(i):
# 		print()

for i in stack:
	if i.has_nodes:
		for j in i.nodes:
			if j == '':
				i.nodes.remove(j)
		if len(i.nodes) == 0:
			i.remove_nodes()

messages = []

for i in stack:
	if i.has_nodes:
		if not containsAuthor(i.parent.split('m - ')[-1]):
			pass
		if containsAuthor(i.parent) or containsEmoji(i.parent):
			messages.append(i)
	else:
		messages.append(i)


for i in messages:
	if i.has_nodes:
		print(getDataPoint(i.parent))

