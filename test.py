'''
interface_number : -1
manufacturer_string : Namtai
path : USB_054c_1000_14200000
product_id : 4096
product_string : Buzz
release_number : 1
serial_number :
usage : 4
usage_page : 1
vendor_id : 1356
'''

import hid
import time
import random


class BuzzController():
	def __init__(self):
		self.d = hid.device(0x054c,0x1000)
		self.d.open(0x054c,0x1000)
		self.d.set_nonblocking(1)
		ON_state = 0xFF
		OFF_state = 0x00
		self.lamps = [OFF_state,OFF_state,OFF_state,OFF_state]

	def flush_leds(self):
		self.d.write([0x00,0x00,self.lamps[0],self.lamps[1],self.lamps[2],self.lamps[3],0x0,0x0])

	def turn_on(self, led_number):
		self.lamps[led_number] = ON_state
		self.flush_leds()

	def turn_off(self, led_number):
		self.lamps[led_number] = OFF_state
		self.flush_leds()

	def close_stream(self):
		self.d.close()

	def reset_stream(self):
		self.d.close()
		self.d.open(0x054c,0x1000)
		self.d.set_nonblocking(1)

	def blink_all(self,interval,totaltime):
		totaltime = totaltime / 2
		for _ in range( int( totaltime // interval) ):
			for i in range(4):
				self.lamps[i] = ON_state
			self.flush_leds()
			time.sleep(interval)
			for i in range(4):
				self.lamps[i] = OFF_state
			time.sleep(interval)

	def blink_player(self,player,interval,totaltime):
		totaltime = totaltime / 2
		for _ in range( int( totaltime // interval) ):
			self.lamps[player] = ON_state
			self.flush_leds()
			time.sleep(interval)
			self.lamps[player] = OFF_state
			time.sleep(interval)

	def blink_list(self,player_list,interval,totaltime):
		totaltime = totaltime / 2
		for _ in range( int( totaltime // interval) ):
			for i in player_list:
				self.lamps[i] = ON_state
			self.flush_leds()
			time.sleep(interval)
			for i in player_list:
				self.lamps[i] = OFF_state
			time.sleep(interval)


	def read_translate(self):
		data = self.d.read(6) 
		if data == []: 
			return None
		elif data[2] & 1:
			return (0,'red')
		elif data[2] & 2:
			return (0,'yellow')
		elif data[2] & 4:
			return (0,'green')
		elif data[2] & 8:
			return (0,'orange')
		elif data[2] & 16:
			return (0,'blue')
		elif data[2] & 32:
			return (1,'red')
		elif data[2] & 64:
			return (1,'yellow')
		elif data[2] & 128:
			return (1,'green')
		elif data[3] & 1:
			return (1,'orange')
		elif data[3] & 2:
			return (1,'blue')
		elif data[3] & 4 :
			return (2,'red')
		elif data[3] & 8 :
			return (2,'yellow')
		elif data[3] & 16:
			return (2,'green')
		elif data[3] & 32:
			return (2,'orange')
		elif data[3] & 64:
			return (2,'blue')
		elif data[3] & 128:
			return (3,'red')
		elif data[4] & 1:
			return (3,'yellow')
		elif data[4] & 2:
			return (3,'green')
		elif data[4] & 4:
			return (3,'orange')
		elif data[4] & 8:
			return (3,'blue')
		else:
			return None

def QuestionEngine():
	def __init__(self,inputfile):
		lines = open(inputfile).read().split('\n')
		question_list = []
		for l in lines:
			if '>' in l:
				question = l[1:]
				answers = []
				correct = 'None'
			elif '-' == l[0]:
				answers.append( l[1:] )
			elif '+' ==l[0]:
				answers.append( l[1:] )
				correct = l[1:]
			elif '=' ==l[0]:
				question_list.append([question,answers,correct])

		random.shuffle( question_list )

	def ask_question(self):
		question,answers,correct = question_list.pop()
		print question
		time.sleep(1)
		for a in answers:
			print a
			time.sleep(0.1)
		return answers, correct

def ScoreBoard():
	def __init__(self):
		self.scores = [0,0,0,0]

	def get_scores(self):
		return self.scores

	def give(self, player, points):
		self.scores[player] += points

	def winner(self):
		return self.scores.index(max(self.scores))




################     MAIN     ############


# Create instances of the main objects
bc = BuzzController()
qe = QuestionEngine('inputfile.txt')
sb = ScoreBoard()

# Print a nice looking Welcome Message TODO
print 'Welcome Mesage'
# Helper dictionary for the order of answers
dict_colors = {'blue':0,'orange':1,'green':2, 'yellow':3, 'red':None}

# Change this number to play more questions
NUMBER_OF_QUESTIONS = 30

# repeat the main game for every question
for _ in range(NUMBER_OF_QUESTIONS):

	# Asks and print the question and possibilities
	answers, correct = qe.ask_question()
	# initialize a list that keeps track of the player that have alreay answered
	already = []
	# The first who answers gets a penalty if he is wrong and a bonus if he is right so I keep this flag on until I check it
	firstplayer_flag = True
	# This flag turns on if the fastest player press red. If nobody answers correctly he takes 4 points otherwise loses 4
	challenge_flag = False
	#Wait a minimum time before allowing answering
	time.sleep(0.5)
	#Flush away bullshit pressed before it was allowed
	[bc.read_traslate() for _ in xrange(100)]
	# Be ready to answer, lights are on!!!
	for i in range(4):
		bc.turn_on(i)

	#Wait for the first player to answer (ccarefull this is potentially infinite loop)
	# notice that pressing the red button is accepted (so red button is considered a Challange....)
	while True:
		try:
			player, answer = bc.read_traslate()
			break
		except TypeError:
			pass

	# COUNTDOWN !!!!!
	# The player who answered keeps is light on, the others blink
	# They have 2 seconds to give an answer
	bc.turn_on(player)
	the_others = list(set(range(4))-set([player]))
	bc.blink_list(the_others,0.1,2)

	#Turn off all the lights
	print 'Time Elapsed'
	print 'The games are done'
	#After this point answers cannot be given and everything is saved in a record
	event_record = [bc.read_traslate() for _ in range(100)]
	# and the lights are turned off to make the point
	for i in range(4):
		bc.turn_off(i)
	

	# Search until you don't find the first that answer correctly
	while True:
		
		bc.blink_all(0.1,1) # Just to make this nicer and slower make a second of blinking per event considered until the first correct
		if (answers[ dict_colors[answer] ] == correct) and (player not in already):
			# if the answer of the currently considered player is correct 
			# AND this is his first observed attempt for that player
			bc.blink_player(player,0.1,3) # First to answer found and blinks for 3 sec
			print 'The fasters to answer correct is player %i' % (player +1)

			# Points are added 3 if it was the first player, 2 if it was the fastest player
			if firstplayer_flag:
				sb.give(player, 3)
			else:
				sb.give(player, 2)

			already.append(player)

			# explore the event record for other players who answered correct and give 1 point
			for E in event_record:
				try:
					player, answer = E
					if (answers[ dict_colors[answer] ] == correct) and (player not in already):
						sb.give(player, 1)
						already.append(player)
					else:
						already.append(player)
				except TypeError:
					#  this error raises for a release button event
					pass
				except ValueError:
					#  this error raises when an empty list is in the event_record
					pass

			# finaly break the while
			break
		else:
			# if the answer of the currently considered player is wrong 

			if firstplayer_flag:
				sb.give(player, -1)

			# This is set false for all the player but the first
			give_penalty_flag = False 

			already.append(player)

			try:
				# consider the next event
				player, answer = event_record.pop()
			except TypeError:
				#  this error raises for a release button event 
				pass
			except ValueError:
				#  this error raises when an empty list is in the event_record
				pass
			except IndexError:
				# pop returns this error when the element are finished
				print 'Nobody answered correctly'
				break

	bc.reset_stream()


print 'The game is finished'
print 'Scores are :' + ', '.get_scores(map(str, sb.scores()))
print 'The winner is player %i' % sb.winner()





'''
[bc.read_traslate() for i in range(100)]



d = hid.device(0x054c,0x1000)
time.sleep(0.3)


d.open(0x054c,0x1000)
time.sleep(0.3)

d.set_nonblocking(1)

#d.read(6)

ON_state = 0xFF
OFF_state = 0x00


lamps = [OFF_state,OFF_state,OFF_state,OFF_state]

def change_state(state):
	if state == ON_state:
		return OFF_state
	else:
		return ON_state



for i in range(100):
	time.sleep(0.1)
	random_ix = random.randint(0,3)
	lamps[random_ix] = change_state(lamps[random_ix])
	d.write([0x00,0x00,lamps[0],lamps[1],lamps[2],lamps[3],0x0,0x0])

d.close()
'''