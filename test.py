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
		self.ON_state = 0xFF
		self.OFF_state = 0x00
		self.lamps = [self.OFF_state,self.OFF_state,self.OFF_state,self.OFF_state]

	def flush_leds(self):
		self.d.write([0x00,0x00,self.lamps[0],self.lamps[1],self.lamps[2],self.lamps[3],0x0,0x0])

	def turn_on(self, led_number):
		self.lamps[led_number] = self.ON_state
		self.flush_leds()

	def turn_off(self, led_number):
		self.lamps[led_number] = self.OFF_state
		self.flush_leds()

	def close_stream(self):
		self.d.close()

	def reset_stream(self):
		self.d.close()
		self.d.open(0x054c,0x1000)
		self.d.set_nonblocking(1)

	def blink_all(self,interval,times):
		#totaltime = totaltime / 2
		for _ in range( times):
			for i in range(4):
				self.lamps[i] = self.ON_state
			self.flush_leds()
			time.sleep(interval)
			for i in range(4):
				self.lamps[i] = self.OFF_state
			self.flush_leds()
			time.sleep(interval)

	def blink_player(self,player,interval,times):
		#totaltime = totaltime / 2
		for _ in range( times):
			self.lamps[player] = self.ON_state
			self.flush_leds()
			time.sleep(interval)
			self.lamps[player] = self.OFF_state
			time.sleep(interval)
			self.flush_leds()

	def blink_list(self,player_list,interval,times):
		#totaltime = totaltime / 2
		for _ in range( times):
			for i in player_list:
				self.lamps[i] = self.ON_state
			self.flush_leds()
			time.sleep(interval)
			for i in player_list:
				self.lamps[i] = self.OFF_state
			self.flush_leds()
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

class QuestionEngine():
	def __init__(self,inputfile):
		lines = open(inputfile).read().split('\n')
		self.question_list = []
		#answers = []
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
				if len(answers) != 4:
					for z in range(4 - len(answers)):
						answers.append('')
				self.question_list.append([question,answers,correct])

		random.shuffle( self.question_list )

	def ask_question(self):
		question,answers,correct = self.question_list.pop()
		print question + '\n'
		time.sleep(2.5)
		for a in answers:
			print ' - ' + a + '\n'
			time.sleep(0.3)
		return answers, correct

class ScoreBoard():
	def __init__(self):
		self.scores = [0,0,0,0]

	def get_scores(self):
		return tuple( self.scores )

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
print '\n\n\nWelcome To the game for Chema!!!\n\n authored by Giole and Juan Luis\n and yes we are the best\n'
# Helper dictionary for the order of answers
dict_colors = {'blue':0,'orange':1,'green':2, 'yellow':3, 'red':None}

# Change this number to play more questions
NUMBER_OF_QUESTIONS = 26

# repeat the main game for every question
for _ in range(NUMBER_OF_QUESTIONS):

	
	# initialize a list that keeps track of the player that have alreay answered
	already = []
	# The first who answers gets a penalty if he is wrong and a bonus if he is right so I keep this flag on until I check it
	firstplayer_flag = True
	# This flag turns on if the fastest player press red. If nobody answers correctly he takes 4 points otherwise loses 4
	challenge_flag = False
	#Wait a minimum time before allowing answering
	time.sleep(0.5)
	#Flush away bullshit pressed before it was allowed
	[bc.read_translate() for _ in xrange(100)]

	for i in range(4):
		bc.turn_off(i)
	print '\nGet ready press the red button. Now!\n'
	ready = [False,False,False,False]
	while not (ready[0] and ready[1] and ready[2] and ready[3]):
		try:
			player, answer = bc.read_translate()
			if answer == 'red':
				ready[player] = True
				bc.turn_on(player)
		except TypeError:
			pass

	[bc.read_translate() for _ in xrange(100)]
	# Be ready to answer, lights are on!!!
	
	# Asks and print the question and possibilities
	answers, correct = qe.ask_question()	

	#Wait for the first player to answer (ccarefull this is potentially infinite loop)
	# notice that pressing the red button is accepted (so red button is considered a Challange....)
	while True:
		try:
			player, answer = bc.read_translate()
			break
		except TypeError:
			pass

	# COUNTDOWN !!!!!
	# The player who answered keeps is light on, the others blink
	# They have 2 seconds to give an answer
	bc.turn_on(player)
	the_others = list(set(range(4))-set([player]))
	bc.blink_list(the_others,0.1,20)

	#Turn off all the lights
	print 'Time Elapsed!!!!!!!\n'
	print 'The games are done!!! Stop pressing is uselless!!\n'
	#After this point answers cannot be given and everything is saved in a record
	event_record = [bc.read_translate() for _ in range(30)]
	# and the lights are turned off to make the point
	for i in range(4):
		bc.turn_off(i)
	time.sleep(3)
	

	# Search until you don't find the first that answer correctly
	while True:
		
		bc.blink_all(0.03,2) # Just to make this nicer and slower make a second of blinking per event considered until the first correct
		if (answers[ dict_colors[answer] ] == correct) and (player not in already):
			# if the answer of the currently considered player is correct 
			# AND this is his first observed attempt for that player
			bc.blink_player(player,0.1,10) # First to answer found and blinks for 3 sec
			print 'The correct answer was:'
			print '%s\n' % correct
			print 'The faster to answer correct is player %i\n' % (player +1)
			bc.turn_on(player)
			# Points are added 3 if it was the first player, 2 if it was the fastest player
			if firstplayer_flag:
				sb.give(player, 3)
				print 'Player %i wins 3 points' %  (player +1)
			else:
				sb.give(player, 2)
				print 'Player %i wins 2 points' %  (player +1)

			already.append(player)

			# explore the event record for other players who answered correct and give 1 point
			for E in event_record:
				try:
					player, answer = E
					if (answers[ dict_colors[answer] ] == correct) and (player not in already):
						sb.give(player, 1)
						print 'But also the slow player %i get it right! 1 point' %  (player +1)
						bc.blink_player(player,0.1,10)
						bc.turn_on(player)
						already.append(player)
					else:
						already.append(player)
				except TypeError:
					#  this error raises for a release button event
					pass
				except ValueError:
					#  this error raises when an empty list is in the event_record
					pass
			print 'The score is Player1: %i   Player2: %i   Player3: %i   Player4: %i\n' % sb.get_scores()
			# finaly break the while
			time.sleep(3)
			break
		else:
			# if the answer of the currently considered player is wrong 

			if firstplayer_flag and (player not in already):
				sb.give(player, -1)

			# This is set false for all the player but the first
			firstplayer_flag = False 

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
				print '\nNobody answered correctly!!!!!!!! Looosers!!!!!\n'
				break

	bc.reset_stream()


print 'The game is finished. Stop crying for more!!!!\n\n'
time.sleep(2)
print 'The score is Player1: %i   Player2: %i   Player3: %i   Player4: %i' % sb.get_scores()
print 'The winner is player %i' % (sb.winner() +1)





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