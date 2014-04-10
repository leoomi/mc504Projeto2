#!/usr/bin/python

import threading
import time

empty = threading.Semaphore(1) #semaforo que indica se o banheiro esta ou nao vazio
maleMultiplex = threading.Semaphore(3) #Multiplex garantem que no maximo 3 pessoas fiquem simultaneamente no banheiro
femaleMultiplex = threading.Semaphore(3)


class lock():
    def __init__(self):
	self.status = 'False'
	self.counter = 0 #contador de pessoas que acessaram o lock
    def changeStatus(self):
	
	if self.status == 'False' and self.counter == 1:  #garante que so uma pessoa chame o metodo acquire de empty
		empty.acquire()
		print "Lock capturado"
		self.status = 'True'
	if self.status == 'True' and self.counter == 0: 
		print "Lock liberado"
		self.status = 'False'
		empty.release()

maleLock = lock()
femaleLock = lock()

class threadMale (threading.Thread):
    def __init__(self, threadID, name, counter, lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
	self.lock = lock
    def run(self):
	maleLock.counter = maleLock.counter+1
	while maleLock.status == 'False':
		maleLock.changeStatus()
	maleMultiplex.acquire()
	print "Homem %d entrou no banheiro" %(self.threadID)
	time.sleep(5)
	print "Homem %d saiu do banheiro" %(self.threadID)
	maleLock.counter = maleLock.counter-1
	if maleLock.counter == 0:
		maleLock.changeStatus()
	maleMultiplex.release()

class threadFemale (threading.Thread):
    def __init__(self, threadID, name, counter, lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
	self.lock = lock
    def run(self):
	femaleLock.counter = femaleLock.counter+1
	while femaleLock.status == 'False':
		femaleLock.changeStatus()
	femaleMultiplex.acquire()
	print "Mulher %d entrou no banheiro" %(self.threadID)
	time.sleep(5)
	print "Mulher %d saiu do banheiro" %(self.threadID)
	femaleLock.counter = femaleLock.counter-1
	if femaleLock.counter == 0:
		femaleLock.changeStatus()
	femaleMultiplex.release()
	


# Create new threads
numberOfThreads=1
while numberOfThreads<4:
        time.sleep(1)
        thread1 = threadMale(numberOfThreads, "Homem", 1, maleLock)
        thread1.start()
	thread2 = threadFemale(numberOfThreads, "Mulher", 1, maleLock)
        thread2.start()
	numberOfThreads+= 1

#time.sleep(10)
#thread2 = threadFemale(numberOfThreads, "Mulher", 1, maleLock)

#thread1 = threadMale(numberOfThreads, "Homem", 1, maleLock)
#thread1.start()
#thread2.start()
