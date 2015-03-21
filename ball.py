import globals as g
import math
import pygame
import math
import clump
import game

class Ball(pygame.sprite.Sprite):
	print "blah"

	def __init__(self, xLoc, yLoc, xVel, yVel, xAcc, yAcc, radius, color):
		pygame.sprite.Sprite.__init__(self)
		g.maxRadius = max(g.maxRadius, radius)
		self.x = xLoc
		self.y = yLoc
		self.wasHit = False
		self.xVel = xVel
		self.yVel = yVel

		self.xAcc = xAcc
		self.yAcc = yAcc

		self.oldXVel = g.startXVel
		self.oldYVel = g.startYVel

		self.XIndex = 0

		self.density = .5

		self.color = color


		self.radius = radius

		self.myClump = clump.Clump(self)
		g.allBalls.append(self)
		self.ballCollides = True
		self.wallCollides = True

	def possibleCollisionCandidates(self):
		possibleCandidates = []
		index = self.XIndex-1

		# Look to left
		while index >= 0:
			candidate = g.allBalls[index]
			# Candidate
			if self.x - candidate.x < g.maxRadius*2:
				possibleCandidates.append(candidate)
			# Too far -- break
			else:
				break
			index -= 1

		# Look to right
		index = self.XIndex+1
		while index < len(g.allBalls):
			candidate = g.allBalls[index]
			# Candidate
			if candidate.x - self.x < g.maxRadius*2:
				possibleCandidates.append(candidate)
			# Too far -- break
			else:
				break
			index += 1


		return possibleCandidates

	def newClumpCheck(self, newXVel, newYVel):
		velocityChange = math.sqrt(pow(self.xVel-newXVel, 2) + pow(self.yVel-newYVel, 2))
		if velocityChange > g.clumpEscapeSpeed and len(self.myClump.ballsInClump) > 1:
			self.startNewClump()
			game.makeSparksAt(8, self.x, self.y, velocityChange, (255,255,255))

	def startNewClump(self):
		
		self.myClump.removeBallFromClump(self)
		self.myClump = clump.Clump(self)

	def deleteSelf(self):
		g.allBalls.remove(self)
		self.myClump.removeBallFromClump(self)

	def distanceToXY(self, x, y):
		xDif = self.x- x
		yDif = self.y- y

		collisionAngle = math.atan2(yDif,xDif)
		xDifSq = pow(xDif, 2)
		yDifSq = pow(yDif, 2)
		totalDif = math.sqrt(xDifSq + yDifSq)
		return totalDif

	def joinWithClump(self, otherBall):
		game.renderAll()

		if not self.myClump == otherBall.myClump:
			self.myClump.removeBallFromClump(self)
			otherBall.myClump.addBallToClump(self)


	def getSpeed():
		return math.sqrt(math.pow(self.xVel, 2) + math.pow(self.yVel, 2))

	def update(self):
		# Update position
		self.x = round(self.x+ self.xVel,2)
		self.y = round(self.y+self.yVel,2)

		# g.dirt.removeDirtAt((self.x, self.y))

		# Update velocity
		self.xVel += self.xAcc
		self.yVel += self.yAcc + g.gravity



		# Go To stuff:
		goToX = g.goTo[0]
		goToY = g.goTo[1]
		xDif = goToX - self.x
		yDif = goToY - self.y
		theta = math.atan2(yDif, xDif)
		# Go to goTo
		if g.goingTo:#counter < 100:
			self.xAcc = math.cos(theta)*g.goToAcc
			self.yAcc = math.sin(theta)*g.goToAcc
			# self.radius  += 1
		# Random Walk
		else:
			self.xAcc =0#random.randint(-1, 1)
			self.yAcc = 0#random.randint(-1, 1)
			# self.radius  = max (1, self.radius -1)
		# self.radius = random.randint(5, 20)
		if self.ballCollides:
			self.ballCheck()
		if self.wallCollides:
			self.wallCheck()
	def closestBallInClump(self):
		candidate = None
		bestCandidateVal = 999999999
		for otherBall in self.myClump.ballsInClump:
			if not otherBall == self:
				xDif = self.x- otherBall.x
				yDif = self.y- otherBall.y
				collisionAngle = math.atan2(yDif,xDif)
				xDifSq = pow(xDif, 2)
				yDifSq = pow(yDif, 2)
				totalDif = math.sqrt(xDifSq + yDifSq)
				if totalDif < bestCandidateVal:
					bestCandidateVal = totalDif
					candidate = otherBall
		return candidate


	def xWallCheck(self):
		toReturn = False
		# Wall check
		if self.x < self.radius: 
			# self.xVel = -self.xVel
			self.x = self.radius
			self.myClump.hitXWall()
			toReturn = True
		elif self.x > XDIM - self.radius:
			# self.xVel = -self.xVel
			self.x = XDIM - self.radius
			self.myClump.hitXWall()
			toReturn = True
		return toReturn
	def yWallCheck(self):
		toReturn = False
		if self.y < self.radius:
			# self.yVel = -self.yVel
			self.y = self.radius
			self.myClump.hitYWall()
			toReturn = True
		elif self.y > YDIM - self.radius:
			# self.yVel = -self.yVel
			self.y = YDIM - self.radius
			self.myClump.hitYWall()
			toReturn = True
		return toReturn

	def wallCheck(self):
		# Wall check

		if self.x < self.radius: 
			self.myClump.hitXWall()
			self.newClumpCheck(-self.xVel, self.yVel)
		elif self.x > g.XDIM - self.radius:
			self.myClump.hitXWall()
			self.newClumpCheck(-self.xVel, self.yVel)
		if self.y < self.radius: 
			self.myClump.hitYWall()
			self.newClumpCheck(self.xVel, -self.yVel)
		elif self.y > g.YDIM - self.radius:
			self.myClump.hitYWall()
			self.newClumpCheck(self.xVel, -self.yVel)

	def ballCheck(self):

		# Other balls check
		possibleCandidates = self.possibleCollisionCandidates()
		for otherBall in possibleCandidates:
			if otherBall not in self.myClump.ballsInClump:
				amountOfOverlap = self.overLappingBy(otherBall) 
				if amountOfOverlap > 0:

					speed = math.sqrt(pow(self.xVel, 2) + pow(self.yVel, 2))
					# Clump if speed high enough
					if speed > g.collisionSpeedToClump:
						self.joinWithClump(otherBall)
					else: #if not otherBall in self.myClump.ballsInClump:
					# Update velocities otherwise if in different clumps
						self.collidedWith(otherBall)
						# if self.radius > otherBall.radius:
						# 	otherBall.myClump.removeBallFromClump(otherBall)
						# 	self.radius += otherBall.radius
						# 	g.maxRadius = max(g.maxRadius, self.radius)
						# else:
						# 	self.myClump.removeBallFromClump(self)
						# 	otherBall.radius += otherBall.radius
						# 	g.maxRadius = max(g.maxRadius, otherBall.radius)

	def overLappingBy(self, otherBall):
		if not self.ballCollides or not otherBall.ballCollides:
			return 0
		else:
			xDif = self.x - otherBall.x
			yDif = self.y - otherBall.y
			xDifSq = pow(xDif, 2)
			yDifSq = pow(yDif, 2)
			totalDistance = math.sqrt(xDifSq + yDifSq)
			return  self.radius + otherBall.radius - totalDistance


	def findAnAngleOfXComponent(self, xComponent, yComponent):
		deltaY = yComponent
		deltaX = xComponent
		collisionAngle = math.atan2(deltaY,deltaX)

		# if deltaX < 0:
		# 	if deltaY > 0:
		# 		collisionAngle = collisionAngle + math.pi
		# 	else:
		# 		collisionAngle = collisionAngle - math.pi
		return collisionAngle
	def collidedWith(self, otherBall):
		if not self.wasHit:

			deltaX =   otherBall.x - self.x
			deltaY =  otherBall.y - self.y
			# if deltaX == 0:
			# 	self.myClump.hitYWall()
			# 	otherBall.myClump.hitYWall()
			# elif deltaY == 0:
			# 	self.myClump.hitXWall()
			# 	otherBall.myClump.hitXWall()

			collisionAngle = math.atan2(deltaY,deltaX)
			# if deltaX < 0:
			# 	if deltaY > 0:
			# 		collisionAngle = collisionAngle + math.pi
			# 	else:
			# 		collisionAngle = collisionAngle - math.pi
			v1i = math.sqrt(pow(self.xVel, 2) + pow(self.yVel, 2))
			v2i = math.sqrt(pow(otherBall.xVel, 2) + pow(otherBall.yVel, 2))
			ang1 = self.findAnAngleOfXComponent(self.xVel, self.yVel)
			ang2 = self.findAnAngleOfXComponent(otherBall.xVel, otherBall.yVel)
			v1xr = v1i*math.cos(ang1-collisionAngle)
			v1yr = v1i*math.sin(ang1-collisionAngle)
			v2xr = v2i*math.cos(ang2-collisionAngle)
			v2yr = v2i*math.sin(ang2-collisionAngle)

			m1 = self.myClump.getTotalMass()
			m2 = otherBall.myClump.getTotalMass()

			v1fxr = ((m1 - m2)*v1xr + (m2*2)*v2xr)/(m1 + m2)
			v2fxr = ((m1*2)*v1xr+(m2-m1)*v2xr)/(m1 + m2)
			v1fyr = v1yr
			v2fyr = v2yr

			if (v1xr-v2xr < 0):
				return
			v1fx = math.cos(collisionAngle)*v1fxr+math.cos(collisionAngle + math.pi/2)*v1fyr
			v1fy = math.sin(collisionAngle)*v1fxr+math.sin(collisionAngle + math.pi/2)*v1fyr
			v2fx = math.cos(collisionAngle)*v2fxr+math.cos(collisionAngle + math.pi/2)*v2fyr
			v2fy = math.sin(collisionAngle)*v2fxr+math.sin(collisionAngle + math.pi/2)*v2fyr

			# Finally update velocities...
			oldSpeed1 = self.getSpeed()
			self.newClumpCheck(v1fx, v1fy)
			self.setClumpVel(v1fx, v1fy)
			newSpeed1 = self.getSpeed()
			# otherBall.xVel = v2fx
			# otherBall.yVel = v2fy
			otherBall.wasHit = True
			oldSpeed2 = otherBall.getSpeed()
			otherBall.newClumpCheck(v2fx, v2fy)
			otherBall.setClumpVel(v2fx, v2fy)
			newSpeed2 = otherBall.getSpeed()

			# Spark stuff
			xPointOfContact = self.x + self.radius*math.cos(collisionAngle)
			yPointOfContact = self.y + self.radius*math.sin(collisionAngle)
			speedDif1 = math.fabs(oldSpeed1-newSpeed1)
			speedDif2 = math.fabs(oldSpeed2-newSpeed2)
			if speedDif1 + speedDif2 > 5:
				game.makeSparksAt(self.radius, xPointOfContact, yPointOfContact, speedDif1 + speedDif2, self.color)


	def setClumpVel(self, xVel, yVel):
		speed = math.sqrt(math.pow(xVel,2) + math.pow(yVel,2)) * g.velRetainedOnCollision
		velAngle = math.atan2(yVel, xVel)
		for ball in self.myClump.ballsInClump:
			ball.xVel = speed*math.cos(velAngle)
			ball.yVel = speed*math.sin(velAngle)

	def getSpeed(self):
		return math.sqrt(math.pow(self.xVel,2) + math.pow(self.yVel, 2))

	def draw(self, screen):
		pass
	def render(self):
		color = self.color
		ballLoc = (int(round(self.x,0)), int(round(self.y,0)))
		pygame.draw.circle(g.screen, color, ballLoc, int(self.radius))
		pygame.draw.circle(g.screen, (0,0,0), ballLoc, int(self.radius-2))
			