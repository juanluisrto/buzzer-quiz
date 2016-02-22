import pygame
import usb.core
import usb.util
import usb.backend
import traceback, sys, os
import time
import buzzdisp
#pygame.init()
#screen = pygame.display.set_mode((1024, 768),0,0)

device = usb.core.find(idVendor=0x054c, idProduct=0x1000)
cfg = device.get_active_configuration()
endpoint = cfg[(0,0)][0]

device.ctrl_transfer(0x21, 0x09,0x0200,0,[0xFF,0xFF,0xFF,0xFF,0x0,0x0]) #doesnt work




while True:
	print device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, timeout=3000)




