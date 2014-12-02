#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, time
import threading
import qploop

class Worker(qploop.QPObject):
	"""docstring for Worker"""
	def __init__(self, *arg, **kwargs):
		super(Worker, self).__init__()
		self.s1 = qploop.Signal()
		self.s1.connect(self.funcB)
	
	def funcA(self, *args, **kwargs):
		print(threading.current_thread())
		print('funcA', args, kwargs)
		self.s1.emit(3, 4, b=5)

	def funcB(self, *args, **kwargs):
		print(threading.current_thread())
		print('funcB', args, kwargs)

	def funcC(self, *args, **kwargs):
		print(threading.current_thread())
		print('funcC', args, kwargs)
		self.funcA()
		self.s1.disconnect(self.funcB)

	def funcD(self, *args, **kwargs):
		print('funcD', args, kwargs)


def mainfuncA(*args, **kwargs):
	print(threading.current_thread())
	print('mainfuncA', args, kwargs)


if __name__ == '__main__':
	thread1 = qploop.EventThread()
	thread1.start()

	thread2 = qploop.EventThread()
	thread2.start()

	w1 = Worker()
	w1.moveToThread(thread1)
	
	w2 = Worker()
	w2.moveToThread(thread2)

	s1 = qploop.Signal()
	s1.connect(w1.funcA)

	s2 = qploop.Signal()
	s2.connect(w2.funcC)

	s2.emit(3, 4)
	time.sleep(2)
	s2.emit(1, 2)
	# while 1:
	# 	time.sleep(2)
	# 	s.emit(1, 2)
	# 	print('++++++++++++++++++')
