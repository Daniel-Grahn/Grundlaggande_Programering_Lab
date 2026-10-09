from gamemodel import *
from graphics import *


class GameGraphics:
    def __init__(self, game:Game):
        self.game = game

        # open the window
        self.win = GraphWin("Cannon game" , 640, 480, autoflush=False)
        self.win.setCoords(-110, -10, 110, 155)
        
        # draw the terrain
        # TODO: Draw a line from (-110,0) to (110,0)
        self.line = Line(Point(-110,0),Point(110,0))
        self.line.setFill("black")
        self.line.draw(self.win)

        self.draw_cannons = [self.drawCanon(0), self.drawCanon(1)]
        self.draw_scores  = [self.drawScore(0), self.drawScore(1)]
        self.draw_projs   = [None, None]

        self.traceCircles = []

    def drawCanon(self,playerNr):
        # draw the cannon
        # TODO: draw a square with the size of the cannon with the color
        
        player = self.game.getPlayers()[playerNr]
        canon_size = self.game.getCannonSize()
        
        center_Xpos = player.getX()
        
        p1 = Point(center_Xpos - (canon_size//2), 0)
        p2 = Point(center_Xpos + (canon_size//2), canon_size)
        
        
        rect = Rectangle(p1,p2)
        rect.setFill(player.getColor())
        rect.setOutline(player.getColor())
        rect.draw(self.win)
        
        # and the position of the player with number playerNr.
        # After the drawing, return the rectangle object.
        return rect

    def drawScore(self,playerNr):
        # draw the score
        # TODO: draw the text "Score: X", where X is the number of points
        # for player number playerNr. The text should be placed under
        # the corresponding cannon. After the drawing,
        # return the text object.
        
        player = self.game.getPlayers()[playerNr]
        score = player.getScore()
        
        center_Xpos = player.getX()        
        
        text = Text(Point(center_Xpos, -5), f"Score: {score}")
        text.setFill("black")
        text.draw(self.win)
        
        return text

    def fire(self, angle, vel):
        player = self.game.getCurrentPlayer()
        proj = player.fire(angle, vel)

        circle_X = proj.getX()
        circle_Y = proj.getY()
        
        ball_Size = self.game.getBallSize()

        # TODO: If the circle for the projectile for the current player
        # is not None, undraw it!
        
        circle:Circle = self.draw_projs[self.game.getCurrentPlayerNumber()]
        if circle:
           circle.undraw()
       
        circle = Circle(Point(circle_X,circle_Y),ball_Size)

        # draw the projectile (ball/circle)
        # TODO: Create and draw a new circle with the coordinates of
        # the projectile.
        circle.setFill(player.getColor())
        circle.setOutline(player.getColor())
        circle.draw(self.win)
        
        while proj.isMoving():
            proj.update(1/50)

            # move is a function in graphics. It moves an object dx units in x direction and dy units in y direction
            circle.move(proj.getX() - circle_X, proj.getY() - circle_Y)

            circle_X = proj.getX()
            circle_Y = proj.getY()

            update(50)

        self.draw_projs[self.game.getCurrentPlayerNumber()] = circle
        return proj

    def updateScore(self,playerNr:int):
        # update the score on the screen
        # TODO: undraw the old text, create and draw a new text
        text:Text = self.draw_scores[playerNr]
        text.undraw()
        player = self.game.getPlayers()[playerNr]
        new_score = player.getScore()
        
        text.setText(f"Score: {new_score}")
        text.draw(self.win)

    def play(self, prev_inp=None):
        while True:
            player = self.game.getCurrentPlayer()
            oldAngle,oldVel = player.getAim()
            wind = self.game.getCurrentWind()

            # InputDialog(self, angle, vel, wind) is a class in gamegraphics
            inp = InputDialog(oldAngle,oldVel,wind) if prev_inp is None else prev_inp
            # interact(self) is a function inside InputDialog. It runs a loop until the user presses either the quit or fire button
            if inp.interact() == "Quit":
                exit()
            elif inp.interact() == "Trace":
                angle,vel = inp.getValues()
                self.removeTrace()
                self.drawTrace(angle,vel)
                oldAngle,oldVel = angle,vel
                self.play(inp)
            self.removeTrace()
            inp.close()
            angle, vel = inp.getValues()
            player = self.game.getCurrentPlayer()
            other = self.game.getOtherPlayer()
            proj = self.fire(angle, vel)
            distance = other.projectileDistance(proj)

            if distance == 0.0:
                player.increaseScore()
                self.updateScore(self.game.getCurrentPlayerNumber())
                self.game.newRound()

            self.game.nextPlayer()
            prev_inp = None

    def drawTrace(self, angle, velocity, dots=100, timestep=3):
        player = self.game.getCurrentPlayer()
        trace = player.fire(angle,velocity)
        ball_Size = self.game.getBallSize()

        for _ in range(dots):
            trace_x = trace.getX()
            trace_y = trace.getY()
            circle = Circle(Point(trace_x,trace_y),ball_Size//3)
            self.traceCircles.append(circle)

            circle.setFill(player.getColor())
            circle.setOutline(player.getColor())
            circle.draw(self.win)
            circle_X = trace.getX()
            circle_Y = trace.getY()

            if circle_Y == 0 or circle_X <= trace.xLower or circle_X >= trace.xUpper:
                break

            circle.move(trace.getX() - circle_X, trace.getY() - circle_Y)

            trace.update(1/timestep)
    def removeTrace(self):
        for Circle in self.traceCircles:
            Circle.undraw()

class InputDialog:
    def __init__ (self, angle, vel, wind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0,4.5,4,.5)
        Text(Point(1,1), "Angle").draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(angle))
        
        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(vel))
        
        Text(Point(1,3), "Wind").draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))
        
        self.fire = Button(win, Point(1,4), 0.9, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3,4), 0.9, .5, "Quit")
        self.quit.activate()
        self.trace = Button(win, Point(2,4), 0.9, .5, "Trace")
        self.trace.activate()

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"
            if self.trace.clicked(pt):
                return "Trace"

    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a,v

    def close(self):
        self.win.close()


class Button:

    def __init__(self, win, center, width, height, label):

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        return self.label.getText()

    def activate(self):
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0


GameGraphics(Game(11,3)).play()
