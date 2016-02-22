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
		self.buttons = [ {'red':0, 'yellow':0, 'green':0, 'orange':0, 'blue':0},\
		{'red':0, 'yellow':0, 'green':0, 'orange':0, 'blue':0},\
		{'red':0, 'yellow':0, 'green':0, 'orange':0, 'blue':0},\
		{'red':0, 'yellow':0, 'green':0, 'orange':0, 'blue':0}]

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

	def read_first(self):
		command, lifting = self.read(6), self.read(6)

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