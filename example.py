#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, time
import threading
import qploop

class Worker(qploop.QPObject):
    """docstring for Worker"""
    def __init__(self, *arg, **kwargs):
        super(Worker, self).__init__()
        self.workera = WorkerA()
    
    def funcA(self, *args, **kwargs):
        print(threading.current_thread())
        print('Worker', 'funcA', args, kwargs)

    def funcB(self, *args, **kwargs):
        print(threading.current_thread())
        print('Worker', 'funcB', args, kwargs)

    def funcC(self, *args, **kwargs):
        print(threading.current_thread())
        print('Worker', 'funcC', args, kwargs)

    def funcD(self, *args, **kwargs):
        print('funcD', args, kwargs)


class WorkerA(qploop.QPObject):

    def __init__(self, *arg, **kwargs):
        super(WorkerA, self).__init__()
        self.s = qploop.Signal()
        self.s.connect(mainfuncA)

    def funcA(self, *args, **kwargs):
        print(threading.current_thread())
        print('WorkerA', 'funcD', args, kwargs)
        self.s.emit("4144444")


def mainfuncA(*args, **kwargs):
    print(threading.current_thread())
    print('mainfuncA', args, kwargs, '++++++++++++++')

if __name__ == '__main__':
    thread1 = qploop.EventThread()

    w1 = Worker()
    print(w1.thread)
    w1.moveToThread(thread1)
    print (w1.thread)
    print ("====================")
    s2 = qploop.Signal()
    s2.connect(w1.funcA)
    s2.connect(w1.funcB)
    s2.connect(w1.funcC)
    s2.connect(w1.workera.funcA)
    s2.emit(1, 2)
    qploop.globalLoop.start()
