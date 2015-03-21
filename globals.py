
def init():
	global XDIM
	global YDIM 
	global WINSIZE
	global START
	global lines
	global TERMINALVEL
	global goTo
	global goToVel 
	global keyChangeVal
	global goingTo
	global screen 
	global allBalls 
	global allClumps 
	global gravity
	global velRetainedOnCollision 
	global epsilon
	global numberOfBalls
	global collisionSpeedToClump
	global clumpEscapeSpeed
	global startRadius 
	global startXVel 
	global startYVel 
	global goToAcc
	global shootTheta
	global allCollisionlessParticles
	global maxRadius
	global startColor
	global allWalls
	global dirt
	XDIM = 640
	YDIM = int(480)
	WINSIZE = [XDIM, YDIM]
	START = (0, 0)
	lines = [((0, 0), (0, YDIM)), ((0, 0), (XDIM, 0)), ((XDIM-1, YDIM), (XDIM-1, 0)), ((XDIM, YDIM-1), (0, YDIM-1))]
	TERMINALVEL = 30.0
	goTo = (110, 110)
	goToVel = (0, 0)
	keyChangeVal = 6
	goingTo = False
	screen = None
	allBalls = []
	allClumps = []
	gravity = 0
	velRetainedOnCollision = 1
	epsilon = .000001
	numberOfBalls = 1
	collisionSpeedToClump = 3
	clumpEscapeSpeed = 10
	startRadius = 10
	startXVel = 5
	startYVel = 5
	goToAcc = 1
	shootTheta = 0
	allCollisionlessParticles = []
	maxRadius = 0
	allWalls = []
	startColor = (0, 255, 0)
	dirt = None


