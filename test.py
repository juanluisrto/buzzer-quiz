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

	def read_first(self):
		command, lifting = self.read(6), self.read(6)



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