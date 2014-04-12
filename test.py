import pygame, sys
from pygame.locals import *
pygame.init()
from GameObject import *
import time

screen = pygame.display.set_mode((400, 300))
screen.fill((255, 255, 255))

pygame.display.set_caption('Banheiro Unissex')

backgroundTexture = pygame.image.load('backGround.png')
testTex = pygame.image.load('penguin.png')
testTex2 = pygame.image.load('penguinFemale.png')
fpsClock = pygame.time.Clock()
group = pygame.sprite.Group()
group2 = pygame.sprite.Group()
import threading


empty = threading.Semaphore(1) #semaforo que indica se o banheiro esta ou nao vazio
maleMultiplex = threading.Semaphore(3) #Multiplex garantem que no maximo 3 pessoas fiquem simultaneamente no banheiro
femaleMultiplex = threading.Semaphore(3)


class lock():
    def __init__(self):
	self.status = 'False'
	self.lastIn =0
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
	test = GameObject((400, 100), (100, 100), testTex)
	test.changeDestination((self.threadID%5)*40+200,100)
	while maleLock.status == 'False':
		maleLock.changeStatus()
	while maleLock.lastIn + 1 != self.threadID:
		time.sleep(0)
	maleLock.lastIn = maleLock.lastIn + 1
	maleMultiplex.acquire()
	test.changeDestination(180,100)
	time.sleep(3-(self.threadID%3)/2)
	test.changeDestination((self.threadID%3)*40+150,20)
	print "Homem %d entrou no banheiro" %(self.threadID)
	time.sleep(5)
	print "Homem %d saiu do banheiro" %(self.threadID)
	test.changeDestination(180,400)
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
	test = GameObject((0, 100), (100, 100), testTex2)
	test.changeDestination((self.threadID%5)*40,100)
	while femaleLock.status == 'False':
		femaleLock.changeStatus()
	while femaleLock.lastIn + 1 != self.threadID:
		time.sleep(0)
	femaleLock.lastIn = femaleLock.lastIn + 1
	femaleMultiplex.acquire()
	print "Mulher %d entrou no banheiro" %(self.threadID)
	test.changeDestination(180,100)
	time.sleep(3-(self.threadID%3)/2)
	test.changeDestination((self.threadID%3)*40+150,20)
	time.sleep(5)
	print "Mulher %d saiu do banheiro" %(self.threadID)
	test.changeDestination(200,400)
	femaleLock.counter = femaleLock.counter-1
	if femaleLock.counter == 0:
		femaleLock.changeStatus()
	femaleMultiplex.release()

background = pygame.Surface((screen.get_width(), screen.get_height()))
background.fill((255, 255, 255))


Background.groups = group2
GameObject.groups = group	
maleCounter = 1
femaleCounter = 1

while True: # main game loop
    times = fpsClock.tick(60)
	
    for event in pygame.event.get():
	if event.type == QUIT:
		pygame.quit()
		sys.exit()
	if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_h):
		thread1 = threadMale(maleCounter, "Homem", 1, maleLock)
		maleCounter = maleCounter + 1
		thread1.start()
	if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_m):
		thread1 = threadFemale(femaleCounter, "Mulher", 1, maleLock)
		femaleCounter = femaleCounter + 1
		thread1.start()
	test = Background((200,150),(400, 300), backgroundTexture)

    group.clear(screen, background)
    group2.draw(screen)
    group.update(times/1000.0)
    group.draw(screen)
    pygame.display.update()
    
