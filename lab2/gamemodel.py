from math import sin,cos,radians
import random

#TODO: Deal with all TODOs in this file and also remove the TODO and HINT comments.

""" This is the model of the game"""
class Game:
    """ Create a game with a given size of cannon (length of sides) and projectiles (radius) """
    def __init__(self, cannonSize, ballSize):
        self.cannonSize = cannonSize
        self.ballSize = ballSize

        self.Players = [
            Player(self, False, -90, "blue"),
            Player(self, True, 90, "red")
        ]
        self.currentPlayer = 0
        self.wind = 0

    """ A list containing both players """
    def getPlayers(self):
        return self.Players

    """ The height/width of the cannon """
    def getCannonSize(self):
        return self.cannonSize

    """ The radius of cannon balls """
    def getBallSize(self):
        return self.ballSize

    """ The current player, i.e. the player whose turn it is """
    def getCurrentPlayer(self):
        return self.Players[self.currentPlayer]

    """ The opponent of the current player """
    def getOtherPlayer(self):
        return self.Players[not self.currentPlayer]
    
    """ The number (0 or 1) of the current player. This should be the position of the current player in getPlayers(). """
    def getCurrentPlayerNumber(self):
        return self.currentPlayer
    
    """ Switch active player """
    def nextPlayer(self):
        self.currentPlayer = (self.currentPlayer+1)%2

    """ Set the current wind speed, only used for testing """
    def setCurrentWind(self, wind):
        self.wind = wind

    def getCurrentWind(self):
        return self.wind

    """ Start a new round with a random wind value (-10 to +10) """
    def newRound(self):
        self.setCurrentWind(random.random()*20 - 10)
        self.nextPlayer()

""" Models a player """
class Player:
    def __init__(self, game, isReversed, x, color):
        self.game = game
        self.isReversed = isReversed
        self.x = x
        self.color = color

        self.score = 0 
        self.angle = 45
        self.velocity = 42
    
    """ Create and return a projectile starting at the centre of this players cannon. Replaces any previous projectile for this player. """
    def fire(self, angle, velocity):
        self.angle = angle
        self.velocity = velocity

        if self.isReversed:
            projectileAngle = 180 - angle
        else:
            projectileAngle = angle

        return Projectile(
            projectileAngle,
            velocity,
            self.game.getCurrentWind(),
            self.x,
            self.game.getCannonSize()/2,
            -110,
            110
        )

    """ Gives the x-distance from this players cannon to a projectile. If the cannon and the projectile touch (assuming the projectile is on the ground and factoring in both cannon and projectile size) this method should return 0"""
    def projectileDistance(self, proj):
        distance = abs(self.x - proj.getX())
        distanceY = abs(0 - proj.getY()) 
        #touchingDistance använder skillnaden på 'radien' på både kanonen och bollen. 
        #Anledningen till att vi inte också dividerar getBallSize() med två, är för att getBallSize() returnerar en radie, inte diameter.
        touchingDistance = (self.game.getCannonSize() / 2 + self.game.getBallSize())

        return not (distance <= touchingDistance and distanceY <= touchingDistance) 

    def collision(self, proj):
        dist_x = abs(self.x - proj.getX())
        dist_y = abs(0 - proj.getY())
        touchingDistance = (self.game.getCannonSize() / 2 + self.game.getBallSize())
        
        return dist_x <= touchingDistance and dist_y <= touchingDistance


    """ The current score of this player """
    def getScore(self):
        return self.score

    """ Increase the score of this player by 1."""
    def increaseScore(self):
        self.score += 1

    """ Returns the color of this player (a string)"""
    def getColor(self):
        return self.color

    """ The x-position of the centre of this players cannon """
    def getX(self):
        return self.x

    """ The angle and velocity of the last projectile this player fired, initially (45, 40) """
    def getAim(self):
        return self.angle, self.velocity



""" Models a projectile (a cannonball, but could be used more generally) """
class Projectile: 
    def __init__(self, angle, velocity, wind, xPos, yPos, xLower, xUpper):
        self.yPos = yPos
        self.xPos = xPos
        self.xLower = xLower
        self.xUpper = xUpper
        theta = radians(angle)
        self.xvel = velocity*cos(theta)
        self.yvel = velocity*sin(theta)
        self.wind = wind 
        
    def update(self, time):
        # Compute new velocity based on acceleration from gravity/wind
        yvel1 = self.yvel - 9.8*time
        xvel1 = self.xvel + self.wind*time
        
        # Move based on the average velocity in the time period 
        self.xPos = self.xPos + time * (self.xvel + xvel1) / 2.0
        self.yPos = self.yPos + time * (self.yvel + yvel1) / 2.0
        
        # make sure yPos >= 0
        self.yPos = max(self.yPos, 0)
        
        # Make sure xLower <= xPos <= mUpper   
        self.xPos = max(self.xPos, self.xLower)
        self.xPos = min(self.xPos, self.xUpper)
        
        # Update velocities
        self.yvel = yvel1
        self.xvel = xvel1
        
    """ A projectile is moving as long as it has not hit the ground or moved outside the xLower and xUpper limits """
    def isMoving(self, player:Player=None):
        test_check = 0 < self.getY() and \
               self.xLower < self.getX() < self.xUpper

        if player == None:
            return test_check 
        else:
            return test_check and not player.collision(self)   
        
    def getX(self):
        return self.xPos

    """ The current y-position (height) of the projectile". Should never be below 0. """
    def getY(self):
        return max(self.yPos, 0)