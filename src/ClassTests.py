# -*- coding:utf-8 -*-
"""
Created on Apr 18, 2013

@author: Filip
"""
class ProcessHandler:
	def __init__(self, attrSlot):
		self.attrSlot = attrSlot
		
	def handleEvent(self):
		data = 0.0
		self.attrSlot(data)
		
class ClientClass:
	def __init__(self):
		handler = ProcessHandler(self.slot)
		
		handler.handleEvent()
		
	def slot(self, data):
		print 'Hej!', data
		
if __name__ == '__main__':
	cc = ClientClass()