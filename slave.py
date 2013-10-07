#! runners

from threading import Thread
from random import randint
from pygame import time
from pygame import sprite
from pygame import image
from pygame import Rect
from util import loggin,getValues

class SlaveDrawDesc():

	def __init__(self,initval = sprite.Sprite()):

		self.obj = initval

	def __get__(self):

		return self.obj

	def __set__(self,obj,val):

		if isinstance(sprite.Sprite,val):
			raise Exception('Not correct instace')

		self.obj = val

class SlaveDraw():
	def __init__(self,img):
		self.draw = SlaveDrawDesc()

		img = image.load(img)
		print img
		print type(img)
		self.draw.image = img
		print type(self.draw.image)
		self.draw.rect = self.draw.image.get_rect()

class Slave(Thread):

	def __init__(self,maze,target,config):
		Thread.__init__(self)

		self.config = config
		self.draw = SlaveDraw(config['img']).draw
		self.maze = maze
		self.target = target
		self.canFork = False
		self.item = self.config['maze']['item']

		self.x = 0
		self.y = 0

		self.alive = True

		self.clock = time.Clock()

		#prev path 
		self.path = []
		self.pos = {"x":0,"y":0}

		self.color = [ randint(0,255),randint(0,255),randint(0,255)]

		self.running = True
		self.direction = 0

		#directions key to ignore and actual
		self.ignore = "back"
		self.actual = "next"

		self.directions = {"x":["next","back"],"y":["up","down"]}

		self.keyContraint = {
			"up":{ "ignore": "down","direction":3},
			"down":{ "ignore": "up","direction":1},
			"next":{ "ignore": "back","direction":0},
			"back":{ "ignore": "next","direction":2}
		}

	def run(self):

		while self.running:
			self.clock.tick(40)

			if self.direction == 0:
				self.x = self.x + 1
			elif self.direction == 1:
				self.y = self.y + 1	
			elif self.direction == 2:
				self.x = self.x - 1
			elif self.direction == 3:
				self.y = self.y - 1

			self.move()

	#move on maze and append point to the slave path
	def moveOnMaze(self):
		if (self.x != 0 and self.x % self.item == 0)  or (self.y != 0 and self.y % self.item == 0 ):

			#scuare path
			pathWH = 8

			#to center the path scuare
			middleItem = ( self.item / 2 ) - ( pathWH / 2 )

			#position of the scuare path
			x = self.pos['x'] * self.item + middleItem 
			y = self.pos['y'] * self.item + middleItem 

			if self.x != 0 and self.x % self.config['maze']['item'] == 0 and self.direction % 2  == 0:

				self.path.append( Rect(x ,y ,pathWH,pathWH) )
				self.canFork = True

				if self.direction == 0:
					self.pos["x"] = self.pos["x"] + 1
				else:
					self.pos["x"] = self.pos["x"] - 1

			if self.y != 0 and self.y % self.config['maze']['item'] == 0 and self.direction % 2  != 0:

				self.path.append( Rect(x ,y ,pathWH,pathWH) )
				self.canFork = True

				if self.direction == 1:
					self.pos["y"] = self.pos["y"] + 1
				else:
					self.pos["y"] = self.pos["y"] - 1

	# hanfle all slave's movement
	def move(self):

		if self.pos['x'] == self.target[0] and self.pos['y'] == self.target[1]:
			print 'Finish'
			self.catch()
		
		# handle movent on maze ( not screen )
		self.moveOnMaze()


		# get all posible move
		next = self.maze.space[ self.pos["y"]][self.pos["x"] + 1]
		down = self.maze.space[ self.pos["y"] + 1 ][self.pos["x"]]
		up = self.maze.space[ self.pos["y"] - 1 ][self.pos["x"]]
		back = self.maze.space[ self.pos["y"]][self.pos["x"] - 1]

		#set to a group of values
		result = { "back": back , "next": next , "down": down , "up": up }
		#drop actual value ( don't care )
		result.pop(self.ignore)		

		# get posible movement on both axis
		yResult = getValues(result,self.directions['y'])
		xResult = getValues(result,self.directions['x'])


		# 1 on thres direction means block slave
		if yResult + xResult == 3:
			self.catch()


		# directions 0 | 2  ( x+, x- )
		if self.direction % 2  == 0:

			# if the actual direction will be bloked it change the direction
			if result[self.actual] == 1:
				if result['down'] == 0:
					self.ignore,self.actual = self.keyContraint['up']['ignore'],"up"
					self.direction = self.keyContraint[self.actual]['direction']

				if result['up'] == 0:
					self.ignore,self.actual = self.keyContraint['up']['ignore'],"down"
					self.direction = self.keyContraint[self.actual]['direction']

			#drop actual direction
			result.pop(self.actual)

			#verify if can fork 
			if getValues(result,self.directions['y']) < 2:
				self.wrapPreFork(result)
			
		#directions 1 | 3 ( y+, y- )		
		else:
			if result[self.actual] == 1:
				if result['next'] == 0:
					self.ignore,self.actual = self.keyContraint['next']['ignore'],'next'
					self.direction = self.keyContraint[self.actual]['direction']

				if result['back'] == 0:
					self.ignore,self.actual = self.keyContraint['back']['ignore'],'back'
					self.direction = self.keyContraint[self.actual]['direction']

			#drop actual direction
			result.pop(self.actual)

			if getValues(result,self.directions['x']) < 2:
				self.wrapPreFork(result)


	def wrapPreFork(self,result):

		# canForm ( new slave can fork many slave because od position )
		if self.canFork:

			self.canFork = False

			for key in result:

				#if the direction is equals to 0 can create a new slave
				if result[key] == 0:
					#get actual direction and ignore direction from posible new slave
					tmpIgnore,tmpActual =  self.keyContraint[key]['ignore'],key
					direction = self.keyContraint[key]['direction']

					self.fork(direction,tmpIgnore,tmpActual)
					self.tmpForm = { k:self.pos[k] for k in self.pos }

	def catch(self):
		self.running = False
		print self.name, " Stock"

	def fork(self,direction,ignore,actual):

		slave = self.__class__(self.maze,self.target,self.config)
		slave.direction = direction
		slave.x = self.x
		slave.y = self.y
		slave.pos = self.pos.copy()

		slave.ignore = ignore
		slave.actual = actual

		self.maze.slaves.append( slave )

		slave.start()


