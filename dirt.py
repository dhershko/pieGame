import globals as g
import pygame
import math
import Queue as Q
import game
import ball
import numpy as np

class Dirt():
	def __init__(self):
		brown = (205,133,63)
		self.dirtRad = 5
		self.color = brown
		matrix = np.zeros(shape=(g.YDIM,g.XDIM))
		self.dirtHexs = []
		dirtRows = g.YDIM/(self.dirtRad*2)
		dirtCols = g.XDIM/(self.dirtRad*2)
		for i in range(0, dirtCols):
			for j in range(0, dirtRows):
				toAdd = self.dirtRad
				if j % 2 == 0:
					toAdd = 0
				self.dirtHexs.append((i*self.dirtRad*2+toAdd, j*self.dirtRad*2 + self.dirtRad, self.dirtRad))
	def removeDirtAt(self, posn):
		for toRemove in self.getDirtHexFromXY(posn[0], posn[1]):	
			if toRemove in self.dirtHexs:
				self.dirtHexs.remove(toRemove)
	def getDirtHexFromXY(self, X, Y):
		dirtRows = g.YDIM/(self.dirtRad*2)
		dirtCols = g.XDIM/(self.dirtRad*2)

		xThRow = int(X /(self.dirtRad*2))
		yThRow = int(Y  /(self.dirtRad*2))
		toReturn1 = (xThRow*self.dirtRad*2+self.dirtRad, yThRow*self.dirtRad*2+self.dirtRad, self.dirtRad)
		xThRow = int(math.floor(X /(self.dirtRad*2)))
		yThRow = int(math.floor(Y /(self.dirtRad*2)))
		toReturn2 = (xThRow*self.dirtRad*2+self.dirtRad, yThRow*self.dirtRad*2+self.dirtRad, self.dirtRad)

		return (toReturn1, toReturn2)



	def render(self):
		for dHex in self.dirtHexs:
			dX, dY, dR = dHex
			dR -= 1
			points = []
			for i in range (0, 7):
				angle = i*math.pi/3
				points.append((dR*math.cos(angle) + dX, dY+ dR*math.sin(angle)))

			pygame.draw.polygon(g.screen, self.color, points, 0)