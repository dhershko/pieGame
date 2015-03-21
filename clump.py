import globals as g
import pygame
import math
import Queue as Q
import game

class Clump(pygame.sprite.Sprite):
	def __init__(self, initialBall):
		pygame.sprite.Sprite.__init__(self)
		self.ballsInClump = [initialBall]
		g.allClumps.append(self)

	def removeBallFromClump(self, ball):
		self.ballsInClump.remove(ball)

		ball.myClump = None

		if len(self.ballsInClump) > 1:
			self.solidifyClump()
		elif len(self.ballsInClump) == 0:
			g.allClumps.remove(self)
	def addBallToClump(self, ball):
		ball.myClump = self
		self.ballsInClump.append(ball)

		if len(self.ballsInClump) > 1:
			self.solidifyClump()
	def getTotalMass(self):
		mass = 0
		for ball in self.ballsInClump:
			mass += pow(ball.radius, 2)*math.pi
		return mass

	def ballIsOverlappingInClump(self, ball):
		for otherBall in self.allBallsInClump:
			if not ball == otherBall:
				if ball.overLappingBy(otherBall) > g.epsilon:
					return True
		return False


	def sortBallsOnClosenessToCenter(self, clumpX, clumpY):
		PQ = Q.PriorityQueue()
		for ball in self.ballsInClump:
			distanceToCenter = ball.distanceToXY(clumpX, clumpY)
			PQ.put(ball, distanceToCenter)
		newList = []
		while not PQ.empty():
			newList.append(PQ.get())
		self.allBallsInClump = newList

	def solidifyClump(self):
		clumpX, clumpY = self.getLocOfClump()
		self.sortBallsOnClosenessToCenter(clumpX, clumpY)
		numberOfOverlaps = 0

		# while numberOfOverlaps < len(self.ballsInClump) - 1:
		# 	numberOfOverlaps = 0
		# 	for ball in self.allBallsInClump:
		# 		angleToCenter = math.atan2(ball.y-clumpY, ball.x-clumpX)
		# 		xChange = math.cos(angleToCenter)*quicknessOfSolidify
		# 		yChange = math.sin(angleToCenter)*quicknessOfSolidify
		# 		ball.x -= xChange
		# 		ball.y -= yChange
		# 		if self.ballIsOverlappingInClump(ball):
		# 			ball.x += xChange
		# 			ball.y += yChange
		# 			numberOfOverlaps += 1
		# for ball in self.ballsInClump:
		# 	angleToCenter = math.atan2(ball.y-clumpY, ball.x-clumpX)
		# 	xChange = math.cos(angleToCenter)*ball.radius
		# 	yChange = math.sin(angleToCenter)*ball.radius
		# 	ball.x = clumpX + xChange
		# 	ball.y = clumpY + yChange
		# 	game.correctForBallOverlapAndWallCollision()


	def update(self):

		# self.solidifyClump()
		# Update for group behavour
		totalXVel = 0
		totalYVel = 0
		for ball in self.ballsInClump:
			totalXVel += ball.xVel
			totalYVel += ball.yVel
		totalBalls = len(self.ballsInClump)
		avgXVel = totalXVel/totalBalls
		avgYVel = totalYVel/totalBalls
		for ball in self.ballsInClump:
			ball.xVel = avgXVel
			ball.yVel = avgYVel

		# Update balls individually
		for ball in self.ballsInClump:
			ball.update()

		# Clump together


	def getLocOfClump(self):
		totalX = 0
		totalY = 0
		for ball in self.ballsInClump:
			totalX += ball.x
			totalY += ball.y
		totalBalls = len(self.ballsInClump)
		return (int(totalX/totalBalls), int(totalY/totalBalls))

	def getVolOfClump(self):
		totalVolume = 0
		for ball in self.ballsInClump:
			totalVolume += pow(ball.radius, 2)*math.pi
	def hitYWall(self):
		xVel = self.ballsInClump[0].xVel
		yVel = self.ballsInClump[0].yVel
		velAngle = math.atan2(yVel, xVel)
		speed = math.sqrt(math.pow(xVel,2)+math.pow(yVel,2))*g.velRetainedOnCollision

		for ball in self.ballsInClump:
			ball.xVel = speed*math.cos(velAngle)
			ball.yVel = -speed*math.sin(velAngle)
	def hitXWall(self):
		xVel = self.ballsInClump[0].xVel
		yVel = self.ballsInClump[0].yVel
		velAngle = math.atan2(yVel, xVel)
		speed = math.sqrt(math.pow(xVel,2)+math.pow(yVel,2))*g.velRetainedOnCollision

		for ball in self.ballsInClump:
			ball.xVel = -speed*math.cos(velAngle)
			ball.yVel = speed*math.sin(velAngle)

	def render(self):
		g.screen
		g.allBalls
		pointList = []
		

		# Draw lines
		for ball in self.ballsInClump:
			color = (255,255,255)
			ballLoc = (int (ball.x), int(ball.y))
			for otherBall in self.ballsInClump:
				if not ball == otherBall:
					pygame.draw.line(g.screen, color, ballLoc, (int(otherBall.x), int(otherBall.y)), int(otherBall.radius/3))


		# Draw circles
		for ball in self.ballsInClump:
			ball.render()

