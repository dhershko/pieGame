import pygame
from pygame.locals import *
import math
import random
from scipy.stats import norm as gaussian
import numpy as np
import NoCollisionParticle as NCP 
import clump
import globals as g
import ball as b
import dirt

def makeSparksAt(n, x, y, speed, color):
	for i in range (0, n):
		randomTheta = random.uniform(0, 2*math.pi)
		randomXVel = speed*math.cos(randomTheta)
		randomYVel = speed*math.sin(randomTheta)
		NCP.Spark(x,y, randomXVel, randomYVel, 0, 0, color)

def randomInsert(lst, item):
    lst.insert(random.randrange(len(lst)+1), item)

# Returns number of out of bounds balls corrected
def correctForWallOverlap():
	numberOfWallCollisions = 0
	# Correct for walls
	for ball in g.allBalls:
		if ball.x < ball.radius:
			ball.x = ball.radius
			numberOfWallCollisions += 1
		elif ball.x > g.XDIM - ball.radius:
			ball.x = g.XDIM - ball.radius
			numberOfWallCollisions += 1
		if ball.y < ball.radius:
			ball.y = ball.radius
			numberOfWallCollisions += 1
		elif ball.y > g.YDIM - ball.radius:
			ball.y = g.YDIM - ball.radius
			numberOfWallCollisions += 1
	return numberOfWallCollisions
def correctForBallOverlap():
	overLapsFound = 0
	spaceBuffer = .1
	for ball in g.allBalls:


		for otherBall in g.allBalls:
			if not otherBall == ball:

				amountOfOverlap = ball.overLappingBy(otherBall)
				if amountOfOverlap > 0:
					overLapsFound += 1
					
					xDif = otherBall.x- ball.x
					yDif = otherBall.y- ball.y
					collisionAngle = math.atan2(yDif, xDif)

					velocityAngleBall = math.atan2(ball.yVel, ball.xVel)
					ballSpeed = math.sqrt(pow(ball.yVel, 2) + pow(ball.xVel, 2))

					velocityAngleOther = math.atan2(otherBall.yVel, otherBall.xVel)
					otherBallSpeed = math.sqrt(pow(otherBall.yVel, 2) + pow(otherBall.xVel, 2))

					ballAngle = collisionAngle #+  np.random.normal(0, .1)
					ballScalar = amountOfOverlap/2.0 + spaceBuffer

					otherBallAngle = collisionAngle #+ np.random.normal(0, .1)

					otherBallScalar = amountOfOverlap/2.0 + spaceBuffer


					xChangeBall = (ballScalar)*math.cos(ballAngle) 
					yChangeBall = (ballScalar )*math.sin(ballAngle)

					xChangeOther = (otherBallScalar )*math.cos(otherBallAngle)
					yChangeOther = (otherBallScalar )*math.sin(otherBallAngle)

					coinFlip = random.uniform(0, 1) > .5

					ballInBounds = inBounds(ball.x -xChangeBall, ball.y - yChangeBall, ball)
					otherBallInBounds = inBounds(otherBall.x + xChangeOther, otherBall.y + yChangeOther, otherBall)

					if ballInBounds and otherBallInBounds:
						otherBall.x += xChangeOther
						otherBall.y += yChangeOther
						ball.x -= xChangeBall
						ball.y -= yChangeBall
					elif ballInBounds:
						ballScalar = amountOfOverlap + spaceBuffer*2
						xChangeBall = (ballScalar)*math.cos(ballAngle) 
						yChangeBall = (ballScalar )*math.sin(ballAngle)
						ball.x -= xChangeBall
						ball.y -= yChangeBall

					elif otherBallInBounds:
						otherBallScalar = amountOfOverlap + spaceBuffer*2
						xChangeOther = (otherBallScalar )*math.cos(otherBallAngle)
						yChangeOther = (otherBallScalar )*math.sin(otherBallAngle)
						otherBall.x += xChangeBall
						ball.y -= yChangeBall
						otherBall.x += xChangeOther
						otherBall.y += yChangeOther
					# If moving directly causes out of bounds, then add noise until it woks 
					else:
						ball.x += np.random.normal(0, 2)
						ball.y += np.random.normal(0, 2)
						otherBall.x += np.random.normal(0, 2)
						otherBall.y += np.random.normal(0, 2)

					break
	return overLapsFound
def correctForBallOverlapAndWallCollision():
	wallCollisions = 1
	overLapsFound = 1
	while not wallCollisions == 0 or not overLapsFound == 0:
		wallCollisions = correctForWallOverlap()
		overLapsFound = correctForBallOverlap()

	

def scrammbleBallOrder():
	allBallsScrammbled = []
	for ball in g.allBalls:
		randomInsert(allBallsScrammbled, ball)
	g.allBalls = allBallsScrammbled

def inBounds(x, y, ball):
	return x > ball.radius and x < g.XDIM - ball.radius and y > ball.radius and y < g.YDIM - ball.radius


def swap(ind1, ind2):
	temp = g.allBalls[ind1]
	g.allBalls[ind1] = g.allBalls[ind2]
	g.allBalls[ind2] = temp

def bubbleSortAllBalls():
	performedSwap = True
	while performedSwap:
		performedSwap = False
		for index in range(0, len(g.allBalls)-1):
			ball1 = g.allBalls[index]
			ball2 = g.allBalls[index+1]
			if ball1.x > ball2.x:
				swap(index, index+1)
				performedSwap = True
	for i in range(0, len(g.allBalls)):
		g.allBalls[i].XIndex = i

def renderAll():

	background = pygame.Surface(g.screen.get_size())
	background = background.convert()


	g.screen.blit(background, (0, 0))

	# Draw dirt
	# g.dirt.render()
	# Draw collisionless particles
	for particle in g.allCollisionlessParticles:
		particle.render()

	# Draw balls
	for clump in g.allClumps:
		clump.render()
	# Draw agent
	pygame.draw.circle(g.screen, (0, 0, 255), g.goTo, 10)
	pygame.draw.line(g.screen, (255,0,0), g.goTo, (int(g.goTo[0]+math.cos(g.shootTheta)*20), int(g.goTo[1]+math.sin(g.shootTheta)*20)), 3)



	# Update screen
	pygame.display.flip()

def checkUserInput():
	for event in pygame.event.get():
		# Key down
		if event.type == KEYDOWN:
			# Movement and other controls
			if event.key == K_s:
				g.goToVel = (g.goToVel[0], g.goToVel[1] + g.keyChangeVal)
			elif event.key == K_w:
				g.goToVel = (g.goToVel[0], g.goToVel[1] - g.keyChangeVal)
			elif event.key == K_a:
				g.goToVel = (g.goToVel[0] - g.keyChangeVal, g.goToVel[1])
			elif event.key == K_d:
				g.goToVel = (g.goToVel[0] + g.keyChangeVal, g.goToVel[1])
			elif event.key == K_LEFT:
				g.shootTheta -= math.pi/4
			elif event.key == K_RIGHT:
				g.shootTheta += math.pi/4
			# Specials
			elif event.key == K_LSHIFT:
				g.goingTo = not g.goingTo
				for ball in g.allBalls:
					ball.color = (255, 0, 0)


			elif event.key == K_f:
				for ball in g.allBalls:
					speed = math.sqrt(math.pow(ball.xVel, 2) + math.pow(ball.yVel, 2))
					ball.xVel = speed*math.cos(g.shootTheta)
					ball.yVel = speed*math.sin(g.shootTheta)

			elif event.key == K_SPACE:
				toAppend = b.Ball(g.goTo[0], g.goTo[1], 0, 0, 0, 0, g.startRadius, g.startColor)
				toAppend.xVel = math.fabs(g.startXVel)*math.cos(g.shootTheta)
				toAppend.yVel = math.fabs(g.startYVel)*math.sin(g.shootTheta)


			elif event.key == K_LCTRL:
				if len(g.allBalls) > 0:
					g.allBalls[-1].deleteSelf()

			elif event.key == K_g:
				for ball in g.allBalls:
					ball.startNewClump()
			elif event.key == K_y:
				for ball in g.allBalls:
					ball.red= 255
					ball.green = 0
					renderAll()
					print ball.XIndex
					raw_input()
					ball.red = 0 
					ball.green = 255


		# Key up
		elif event.type == KEYUP:
			if event.key == K_s:
				g.goToVel = (g.goToVel[0], g.goToVel[1] - g.keyChangeVal)
			elif event.key == K_w:
				g.goToVel = (g.goToVel[0], g.goToVel[1] + g.keyChangeVal)
			elif event.key == K_a:
				g.goToVel = (g.goToVel[0] + g.keyChangeVal, g.goToVel[1])
			elif event.key == K_d:
				g.goToVel = (g.goToVel[0] - g.keyChangeVal, g.goToVel[1])

			elif event.key == K_LSHIFT:
				g.goingTo = not g.goingTo
				for ball in g.allBalls:
					ball.color = (math.fabs(ball.color[0]-255), math.fabs(ball.color[1]-255), 0)



def main():
	g.init()
	pygame.init()
	g.screen = pygame.display.set_mode(g.WINSIZE)
	pygame.display.set_caption('WOWEE')



	# Adding balls
	startY = 0
	startX = 0



	red = 0
	blue = 0
	green = 255
	black = 20, 20, 40

	# g.dirt = dirt.Dirt()
	# Make dirt:
	# dirtRad = 10
	# dirtRows = g.YDIM/(dirtRad*2)
	# dirtCols = g.XDIM/(dirtRad*2)
	# for i in range(0, dirtCols):
	# 	for j in range(0, dirtRows):
	# 		dirt.Dirt(i*dirtRad*2+dirtRad, j*dirtRad*2 + dirtRad, dirtRad)
			# renderAll()
	correctForBallOverlapAndWallCollision()	
	
	while True:
		# Update goto
		newX = max(min(g.goTo[0]+ g.goToVel[0], g.XDIM), 0)
		newY = max(min(g.goTo[1] + g.goToVel[1], g.YDIM), 0)
		g.goTo = (newX, newY)

		# update all ball positions
		for clump in g.allClumps:
			clump.update()

		# Sort balls
		bubbleSortAllBalls()
		# Check collisions to update velocities
		# for ball in g.allBalls:
		# 	ball.wallCheck()
		# for ball in g.allBalls:
		# 	ball.ballCheck()
		for ball in g.allBalls:
			ball.wasHit = False
		# Correct for latent overlap
		# if random.uniform(0,1) > 1- .5:
		correctForBallOverlapAndWallCollision()


		# Update nocollision particles
		for particle in g.allCollisionlessParticles:
			particle.update()
		# radialDivisions = 20
		# for angleMult in range(0, radialDivisions):
		# 	angle = (math.pi*2/radialDivisions)*angleMult
		# 	xToRemoveAt = math.cos(angle)*10 + g.goTo[0]
		# 	yToRemoveAt = math.sin(angle)*10 + g.goTo[1]
		# 	g.dirt.removeDirtAt((xToRemoveAt, yToRemoveAt))



		# Visual updates
		renderAll()




		# User input
		checkUserInput()




		



if __name__ == '__main__':
    main()
"""
 To do:
	 split up files
	 rotational stuff
	 optimal collision detection
	 better clump breaking up
	 generalized walls
	 clumps pulling together
	 clumps separating when joining piece lost
	 other particles (mostly for visuals)
	 implement changeVelCheck as a part of update(for clumps and particles)
	 implement a generalized agent for the world




"""





