import globals as g
import math
import pygame
import math
import clump
import game

class Wall(pygame.sprite.Sprite):
	def __init__(self, xStart, yStart, xEnd, yEnd):
		self.xStart = xStart
		self.yStart = yStart
		self.xEnd = xEnd
		self.yEnd = yEnd
		self.speed = speed
		self.currX = xStart
		self.currY = yStart
	def update():
		pass
	def render():
		pygame.draw.line(g.screen, (255,255,255), (self.xStart, self.yStart), (self.xEnd, self.yEnd), 3)
