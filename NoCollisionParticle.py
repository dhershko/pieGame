import pygame
import globals as g


# allCollisionlessParticles = pyGameStuff.allCollisionlessParticles
# gravity = pyGameStuff.gravity
# XDIM = pyGameStuff.XDIM
# YDIM = pyGameStuff.YDIM

class NoCollisionParticle(pygame.sprite.Sprite):
	def __init__(self, x, y, xV, yV, xA, yA, color, radius):
		pygame.sprite.Sprite.__init__(self)	
		self.x = x
		self.y = y
		self.xVel = xV
		self.yVel = yV
		self.xAcc = xA
		self.yAcc = yA
		self.color = color
		self.radius = radius
		g.allCollisionlessParticles.append(self)
	def wallCheck(self):
		# Wall check
		if self.x < self.radius: 
			self.x = self.radius
			self.xVel = -self.xVel
		elif self.x > g.XDIM - self.radius:
			self.x = g.XDIM - self.radius
			self.xVel = -self.xVel
		if self.y < self.radius: 
			self.y = self.radius
			self.yVel = -self.yVel
		elif self.y > g.YDIM - self.radius:
			self.y = g.YDIM - self.radius
			self.yVel = -self.yVel


	def destroy(self):
		g.allCollisionlessParticles.remove(self)

	def update(self):
		# Update values
		self.x += self.xVel
		self.y += self.yVel

		self.xVel += self.xAcc
		self.yVel += self.yAcc + g.gravity

		# Wall check
		self.wallCheck()


		# Destruction check
		self.radius -= .8

		if self.radius <= 0:
			self.destroy()



	def render(self):
		pygame.draw.circle(g.screen, self.color, (int(self.x), int(self.y)), int(self.radius))

class Spark(NoCollisionParticle):
	def __init__(self, x, y, xV, yV, xA, yA, color):
		NoCollisionParticle.__init__(self, x, y, xV, yV, xA, yA, color, 5)
