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
		self.s1.connect(self.funcA)
		self.s1.connect(self.funcB)
		self.s1.connect(self.funcD)
		self.s1.connect(self.funcC)
	
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
		self.s1.disconnect()

	def funcD(self, *args, **kwargs):
		print('funcD', args, kwargs)


def mainfuncA(*args, **kwargs):
	print(threading.current_thread())
	print('mainfuncA', args, kwargs)

def mainfuncB(*args, **kwargs):
	print(threading.current_thread())
	print('mainfuncB', args, kwargs)

def mainfuncC(*args, **kwargs):
	print(threading.current_thread())
	print('mainfuncC', args, kwargs)


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
	s1.connect(mainfuncA)
	s1.connect(mainfuncB)
	s1.connect(mainfuncC)
	s1.emit_now(1, 2)
	time.sleep(3)
	s1.disconnect()
	s1.emit(1, 2)

	s2 = qploop.Signal()
	s2.connect(w2.funcC)
	s2.connect(w2.funcC)

	s2.emit(3, 4)

	t = qploop.Timer(2)
	t.connect(mainfuncA)
	t.start()

	qploop.QPLoop.instance().start()
