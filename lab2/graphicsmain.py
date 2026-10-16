from gamemodel import *
from graphics import *
import math 

class GameGraphics:
    def __init__(self, game:Game):
        self.game = game 
        # open the window
        self.win = GraphWin("Cannon game" , 640, 480, autoflush=False)
        self.win.setBackground(color_rgb(50,130,50))
        self.win.setCoords(-110, -10, 110, 155)
        
        # draw the terrain 
        self.line = Line(Point(-110,0),Point(110,0))
        self.line.setFill("black")
        self.line.draw(self.win)

        self.draw_cannons = [self.drawCannon(0), self.drawCannon(1)]
        self.draw_scores  = [self.drawScore(0), self.drawScore(1)]
        self.draw_projs   = [None, None]

        self.traceCircles = [] 
    
    def drawCannon(self, playerNr, angle=None):
        player = self.game.getPlayers()[playerNr]
        canon_size = self.game.getCannonSize()

        if angle is None:
            angle = player.getAim()[0]
 
        center_Xpos = player.getX()
        p1 = Point(center_Xpos - canon_size / 2, 0)
        p2 = Point(center_Xpos + canon_size / 2, canon_size)

        rect = Rectangle(p1, p2)
        rect.setFill(player.getColor())
        rect.setOutline(player.getColor())
        rect.draw(self.win)

        # adjusting angle for barrel based on isReversed
        if player.isReversed:
            angle = 180 - angle

        barrel_length = 10
        dx = math.cos(math.radians(angle)) * barrel_length
        dy = math.sin(math.radians(angle)) * barrel_length

        start = Point(center_Xpos, canon_size / 2)
        end = Point(start.x + dx, start.y + dy)

        barrel = Line(start, end)
        barrel.setFill("black")
        barrel.setWidth(10)
        barrel.draw(self.win)

        return rect, barrel

    
    def updateCannon(self, angle, playerNr=None):
        if playerNr is None:
            playerNr = self.game.getCurrentPlayerNumber()

        rect, old_barrel = self.draw_cannons[playerNr] 
        old_barrel.undraw() 

        player = self.game.getPlayers()[playerNr] 
        if player.isReversed:
            angle = 180 - angle

        barrel_length = 10
        dx = math.cos(math.radians(angle)) * barrel_length
        dy = math.sin(math.radians(angle)) * barrel_length

        start = Point(player.getX(), self.game.getCannonSize() / 2)
        end = Point(start.x + dx, start.y + dy)

        new_barrel = Line(start, end)
        new_barrel.setFill("black")
        new_barrel.setWidth(10)
        new_barrel.draw(self.win)

        self.draw_cannons[playerNr] = (rect, new_barrel)


    def drawScore(self,playerNr): 
        player = self.game.getPlayers()[playerNr]
        score = player.getScore() 
        center_Xpos = player.getX()   

        text = Text(Point(center_Xpos, -5), f"Score: {score}")
        text.setFill("black")
        text.draw(self.win)
        
        return text

    def fire(self, angle, vel):
        game = self.game
        player = self.game.getCurrentPlayer()
        proj = player.fire(angle, vel) 
        circle_X = proj.getX()
        circle_Y = proj.getY() 
        ball_Size = self.game.getBallSize() 

        circle:Circle = self.draw_projs[self.game.getCurrentPlayerNumber()]
        if circle:
           circle.undraw() 
        circle = Circle(Point(circle_X,circle_Y),ball_Size)

        # draw the projectile (ball/circle) 
        circle.setFill(player.getColor())
        circle.setOutline(player.getColor())
        circle.draw(self.win)
        
        while proj.isMoving(game.getOtherPlayer()):
            proj.update(1/50) 
            circle.move(proj.getX() - circle_X, proj.getY() - circle_Y)

            circle_X = proj.getX()
            circle_Y = proj.getY() 
            update(200)

        self.draw_projs[self.game.getCurrentPlayerNumber()] = circle
        return proj

    def updateScore(self,playerNr:int): 
        text:Text = self.draw_scores[playerNr]
        text.undraw()

        player = self.game.getPlayers()[playerNr]
        new_score = player.getScore() 
        text.setText(f"Score: {new_score}")
        text.draw(self.win)

    def play(self, prev_inp=None): 
        prev_inp = None
        while True:     
            player = self.game.getCurrentPlayer()
            oldAngle,oldVel = player.getAim()
            wind = self.game.getCurrentWind()
            inp = InputDialog(oldAngle,oldVel,wind, color_rgb(40,40,100)) if prev_inp is None else prev_inp  
 
            current_input = inp.interact()  
            if self.win.isClosed() or current_input == "Quit":
                exit() 

            elif current_input == "Trace":
                inp.close()
                prev_inp = None
                angle,vel = inp.getValues()
                self.removeTrace()
                self.updateCannon(angle)
                self.drawTrace(angle,vel)
                oldAngle,oldVel = angle,vel
                self.play(inp) 

            elif current_input == "Fire!":
                inp.close()
                prev_inp = None
                self.removeTrace()
                inp.close()
                angle, vel = inp.getValues()
                self.updateCannon(angle)
                player = self.game.getCurrentPlayer()
                other = self.game.getOtherPlayer()
                proj = self.fire(angle, vel)
                distance = other.projectileDistance(proj)
    
                if distance == 0.0:
                    self.draw_projs[self.game.getCurrentPlayerNumber()].undraw()
                    self.drawExplosion(player.getColor(), proj) 
                    player.increaseScore()
                    self.updateScore(self.game.getCurrentPlayerNumber())
                    self.game.newRound() 

                self.game.nextPlayer() 
            else: 
                prev_inp = inp 
 
    def drawTrace(self, angle, velocity, dots=5000, timestep=25):
        player = self.game.getCurrentPlayer()
        other_player = self.game.getOtherPlayer()
        trace = player.fire(angle,velocity)
        ball_Size = self.game.getBallSize() 
        for d in range(dots):
            trace_x = trace.getX()
            trace_y = trace.getY()
            circle = Circle(Point(trace_x,trace_y),ball_Size//3)

            if(d % 5 == 0):
                circle.setFill(player.getColor())
                circle.setOutline(player.getColor())
                circle.draw(self.win)  

            circle_X = trace.getX()
            circle_Y = trace.getY()

            if circle_Y == 0 or circle_X <= trace.xLower or circle_X >= trace.xUpper or other_player.collision(trace):
                if(other_player.collision(trace)):
                    circle.undraw()
                    rect = Text(Point(circle_X, circle_Y), "X")
                    rect.draw(self.win)
                    rect.setOutline("Green")
                    rect.setFill("Green")
                    self.traceCircles.append(rect)

                self.traceCircles.append(circle)
                break
             
            self.traceCircles.append(circle)

            circle.move(trace.getX() - circle_X, trace.getY() - circle_Y)

            trace.update(1/timestep)
            update(40*5)
            
    def removeTrace(self):
        for Circle in self.traceCircles:
            Circle.undraw()
            

    def drawExplosion(self, color, position: Projectile, granularity = 10): 
        ball_size = self.game.getBallSize()
        step = self.game.getCannonSize() / granularity
        for _ in range(granularity):
            circle = Circle(Point(position.getX(), position.getY()), ball_size )
            ball_size += step
            #circle.setFill(color)
            # circle.
            circle.setOutline(color)
            circle.draw(self.win)
            update(35)
            circle.undraw()
        
class InputDialog:
    def __init__ (self, angle, vel, wind, col):
        self.win = win = GraphWin("Fire", 200, 300)  
        self.win.setBackground(col)
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
        try:
            pt = self.win.getMouse()   
        except:
            exit()

        if self.quit.clicked(pt):
            return "Quit"
        elif self.fire.clicked(pt):
            return "Fire!"
        elif self.trace.clicked(pt):
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
