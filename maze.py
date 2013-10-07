#! maze 

import pygame
from slave import Slave

class Maze():
	
	def __init__(self,config):
		pygame.init()

		self.config = config

		self.width = config['maze']['width']
		self.height = config['maze']['height']

		self.screen = pygame.display.set_mode((self.width,self.height),0,16)

		self.xLines = [ pygame.Rect(i,0,1,self.height) for i in range(0,self.width,self.config['maze']['item']) ]
		self.yLines = [ pygame.Rect(0,i,self.width,2) for i in range(0,self.height,self.config['maze']['item']) ]

		self.reloj = pygame.time.Clock()

		self.bg_color = (51,153,255)

		self.main_slave = None
		self.slaves = []

		scuare = self.config['maze']['item']

		self.space,self.target = self.config['maze']['space']

		# for row in self.space:
		# 	print row

		# exit()

		self.spaces = [ [ None if space != 1 else self.space_factory(x * scuare,y * scuare,scuare) for x,space in enumerate(row)] for y,row in enumerate(self.space) ]


	def factory_slave(self):
		slave = Slave(self,[12,34],self.config)
		return slave

	def space_factory(self,x,y,scuare):
		
		space = pygame.Rect(x,y,scuare,scuare)

		return space

	def play(self):

		run = True

		self.slaves.append( self.factory_slave() )

		start = True

		while run:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					print 'termino'
					run = False
			
			self.reloj.tick(10)	

			self.screen.fill(self.bg_color)


			#draw ground
			for rowSpace in self.spaces:
				for space in rowSpace:
					if space != None:
						pygame.draw.rect(self.screen,[84,54,28],space)


			for line in self.xLines:
				pygame.draw.rect(self.screen,[123,56,200],line)				

			for line in self.yLines:
				pygame.draw.rect(self.screen,[180,12,200],line)

			#draw a slave and his path
			for slave in self.slaves:
				self.screen.blit(slave.draw.image,slave.draw.rect.move(slave.x,slave.y) )

				for point in slave.path:
					pygame.draw.rect(self.screen,slave.color,point)

			if start:

				for slave in self.slaves:
					
					slave.start()

				start = False


			pygame.display.update()


class Space(pygame.sprite.Sprite):
	def __init__(self,config):
		
		pygame.sprite.Sprite.__init__(self)

		self.rect = (config['maze']['item'],config['maze']['item'])
		self.color = [84,54,28]


