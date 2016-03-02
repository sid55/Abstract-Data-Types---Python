
"""
Created on Tue Feb 23 16:59:04 2016

@author: Sidharth Gilela
"""

import math
import numpy as np
import numpy.random as rand
import numpy.linalg as linalg

from tkinter import Tk, Frame, Canvas

########### BEGIN CODE THAT NEEDS TO BE CHANGED ###############

#Priority Data Structure that you are to replace with more efficient implementation
import heapq
#This class uses Python's own heap implementation to maintain a priority
#queue. It can be interchangeably used the ArrayPQ class below.
class ArrayPQ:
    #-__init_ initializes the priority data structure
    def __init__(self, num_balls):
        self.pq = []
        self.index = 0
        return

    #-insert will insert a collision occurring at "value" which is a time stamp parameter
    # The auxilliary data structure maintained along with value is
    # (i, j, num_collisions_i, num_collisions_j)
    def insert(self, i, j, value, num_collisions_i, num_collisions_j):
        key = (i, j, num_collisions_i, num_collisions_j)
        combined = (value,key);
        self.pq.append(combined)
        #self.BuildMinHeap()
        self.index += 1
        return

    #delete will remove the top element from the priority queue
    def delete(self):
        self.ExtractMin()
        return 
    
    def ExtractMin(self):
        if self.index < 1:
            return
        min = self.pq[0]
        self.pq[0] = self.pq[self.index-1]
        self.index = self.index - 1
        self.MinHeapify(0)
        return min

    def MinHeapify(self, i):
        g = 2 * i +1
        r = 2 * i +2
        if g <= self.index-1 and self.pq[g][0] < self.pq[i][0]:
            smallest = g
        else:
            smallest = i
        if r <= self.index-1 and self.pq[r][0] < self.pq[smallest][0]:
            smallest = r
        if smallest != i:
            self.pq[i], self.pq[smallest] = self.pq[smallest], self.pq[i]
            self.MinHeapify(smallest)
    
    def BuildMinHeap(self):
        self.index = len(self.pq)
        for i in range(len(self.pq)//2-1, -1, -1):
            self.MinHeapify(i)
    #-get_next will return the next occurring collision across all possible 
    #collisions
    #get_next returns the time stamp of the collision as well asthe
    #auxillary data maintained along with the value namely
    # (i, j, num_collisions_i, num_collisions_j)
    #This function does not modify the priority queue
    def get_next(self):
        self.BuildMinHeap()
        value, key = self.pq[0]
        i = key[0]
        j = key[1]
        num_collisions_i = key[2]
        num_collisions_j = key[3]
        #self.delete()
        return i, j, value, num_collisions_i, num_collisions_j
########### END CODE THAT NEEDS TO BE CHANGED ###############

#Painter Class is defined in order to work with the tkinter module producing the graphic window
class Painter:
    #__init__ performs the construction of a Painter object
    def __init__(self, root, scale=500, border=5, refresh_speed=5, filename='balls.txt', min_radius=5, max_radius=10, num_balls=20):
        #width and height are used to set the simulation borders
        width = scale + border
        height = scale + border
        #Time is the time stamp for the simulation; it is set to 0 to indicate the beginning of the simulation
        self.time = 0
        #setup will set up the necessary graphics window and the ball list
        self.setup(root, width, height, border, refresh_speed)
        #Check the input parameter 'filename' to load predetermined simulation
        #otherwise set up the default simulation
        if filename is None:
            self.init_balls(max_radius, min_radius, num_balls)
            self.num_balls = num_balls
        else:
            self.num_balls = self.read_balls(scale, filename)
        #Create the priority data structure
        self.PQ = ArrayPQ(self.num_balls)
        #Initialize all possible collision times
        self.init_ball_collision_times()
        self.init_wall_collision_times()
        #draw will draw the graphics to the window
        self.draw()
        #refresh is a loop method intended to create animations
        self.refresh()
        #A blank return indicates the end of the function
        return

    #setup creates the window to display the graphics along with the red border
    #of the simulation
    def setup(self, root, width, height, border, refresh_speed):
        # Draw frame etc
        self.app_frame = Frame(root)
        self.app_frame.pack()
        self.canvas = Canvas(self.app_frame, width = width, height = height)
        self.canvas_size = (int(self.canvas.cget('width')), int(self.canvas.cget('height')))
        self.canvas.pack()
        self.refresh_speed = refresh_speed
        
        # Work area
        self.min_x = border
        self.max_x = width - border
        self.min_y = border
        self.max_y = height - border
        #create array to hold the n number of balls
        self.balls = []
        self.ball_handles = dict()        

        return

    #This function reads in predefined ball numbers and locations to implement predetermined simulations
    def read_balls(self, scale, filename):
        f = open(filename)
        num_balls = int(f.readline().strip())
        
        for l in f:
            ll = l.strip().split(" ")
            x = scale*float(ll[0])
            y = scale*float(ll[1])
            vx = scale*float(ll[2])
            vy = scale*float(ll[3])
            radius = scale*float(ll[4])
            mass = float(ll[5])
            r = int(ll[6])
            g = int(ll[7])
            b = int(ll[8])
            tk_rgb = "#%02x%02x%02x" % (r, g, b)            
            new_ball = Ball(radius, x, y, vx, vy, mass, tk_rgb)
            self.balls.append(new_ball)
        return num_balls
            
    #init_balls will create an array of size "num_balls" stored within self.balls
    def init_balls(self, max_radius, min_radius, num_balls):
        for i in np.arange(num_balls):
            while(True):
                radius = (max_radius - min_radius) * rand.random_sample() + min_radius

                ball_min_x = self.min_x + radius
                ball_max_x = self.max_x - radius
                x = (ball_max_x - ball_min_x)*rand.random_sample() + ball_min_x

                ball_min_y = self.min_y + radius
                ball_max_y = self.max_y - radius                
                y = (ball_max_y - ball_min_y)*rand.random_sample() + ball_min_y

                vx = rand.random_sample()
                vy = rand.random_sample()

                mass = 1.0 # rand.random_sample()
                new_ball = Ball(radius, x, y, vx, vy, mass)
                
                if not new_ball.check_overlap(self.balls):
                    self.balls.append(new_ball)
                    break

    #init_wall_collision_times will set all of the balls' minimum collision time
    #for both horizontal and vertical walls and store that time in their respective arrays
    def init_wall_collision_times(self):
        for i in np.arange(len(self.balls)):
            bi = self.balls[i]
            tix = bi.horizontal_wall_collision_time(self.min_x, self.max_x)
            tiy = bi.vertical_wall_collision_time(self.min_y, self.max_y)
            self.PQ.insert(i, -1, tix + self.time, self.balls[i].count, -1)
            self.PQ.insert(-1, i, tiy + self.time, -1, self.balls[i].count)
        return
    
    #init_ball_collision_times will set all of the balls' minimum collision time
    #with all other balls and store that time within the ith and jth index of
    #PQ.ball_collision_time
    def init_ball_collision_times(self):
        for i in np.arange(self.num_balls):
            bi = self.balls[i]
            for j in np.arange(i+1, self.num_balls):
                bj = self.balls[j]
                tij = bi.ball_collision_time(bj)
                self.PQ.insert(i, j, tij + self.time, self.balls[i].count, self.balls[j].count)
                # self.ball_collision_times[i][j] = tij
                # self.ball_collision_times[j][i] = tij
        return
    
    #update collision times is meant to update collision times of ball i with all
    #walls (horizontal and vertical) and all other balls within the PQ array
    def update_collision_times(self, i):
        bi = self.balls[i]
        tix = bi.horizontal_wall_collision_time(self.min_x, self.max_x)
        tiy = bi.vertical_wall_collision_time(self.min_y, self.max_y)
        self.PQ.insert(i, -1, tix + self.time,self.balls[i].count, -1)
        self.PQ.insert(-1, i, tiy + self.time, -1, self.balls[i].count)
        for j in np.arange(self.num_balls):
            bj = self.balls[j]
            tij = bi.ball_collision_time(bj) + self.time
            if i > j:
                self.PQ.insert(j, i, tij,self.balls[j].count,self.balls[i].count)
            else:
                self.PQ.insert(i, j, tij,self.balls[i].count, self.balls[j].count)
        return

    #draw will draw the borders and all balls within self.balls
    def draw(self):
        #Draw walls
        self.canvas.create_line((self.min_x, self.min_y), (self.min_x, self.max_y), fill = "red")
        self.canvas.create_line((self.min_x, self.min_y), (self.max_x, self.min_y), fill = "red")
        self.canvas.create_line((self.min_x, self.max_y), (self.max_x, self.max_y), fill = "red")
        self.canvas.create_line((self.max_x, self.min_y), (self.max_x, self.max_y), fill = "red")
        #Draw balls        
        for b in self.balls:
            obj = self.canvas.create_oval(b.x - b.radius, b.y - b.radius, b.x + b.radius, b.y + b.radius, outline=b.tk_rgb, fill=b.tk_rgb)
            self.ball_handles[b] = obj
        self.canvas.update()


    #refresh is called to update the state of the simulation
    #-each refresh call can be considered one iteration of the simulation
    #-all balls will be moved and if there is a collision then it will be computed
    def refresh(self):
        #get the next collision
        i, j, t, num_collisions_i, num_collision_j  = self.PQ.get_next()
        #gather the current collisions of the ith and jth ball
        current_collisions_i = self.balls[i].count
        current_collisions_j = self.balls[j].count
        
        #Check the difference in time between the predicted collision time and 
        #the current time stamp of the simulation
        delta = t - self.time
        #If the difference is greater than 1, then just move the balls
        if delta > 1.0:
            # cap delta to 1.0
            for bi in self.balls:
                bi.move()
                self.canvas.move(self.ball_handles[bi], bi.vx, bi.vy)
            self.time += 1.0
        #Otherwise a collision has occurred
        else:
            #Move all balls
            for bi in self.balls:
                bi.move(delta)
                self.canvas.move(self.ball_handles[bi], bi.vx*delta, bi.vy*delta)
            #increment the simulation time stamp
            self.time += delta
            #Delete the top element within the Priority Queue
            self.PQ.delete()
            #if i is -1 then this indicates a collision with a vertical wall
            #also this if statement checks if the number of collisions recorded 
            #when the collision returned by PQ.get_next() is equal to the 
            #number of collisions within the jth ball
            #this acts as a test to check if the collision is still valid
            if i == -1 and num_collision_j == current_collisions_j:
                #compute what happens from the vertical wall collision
                self.balls[j].collide_with_vertical_wall()
                #update collision times for the jth ball
                self.update_collision_times(j)
            #if j is -1 then this indicates a collision a horizontal wall
            #while also checking if the number of collisions match
            #to see if the collision is valid
            elif j == -1 and num_collisions_i == current_collisions_i:
                #compute what happens from the horizontal wall collision
                self.balls[i].collide_with_horizontal_wall()
                #update collision times for the ith ball
                self.update_collision_times(i)
            #Otherwise i and j are not equal to -1 indicating that the collision is between two balls
            #check if no collisions have occurred between both balls before the collision returned from PQ.get_next
            #if true then this means that the collision is still valid and must be executed
            elif num_collision_j == current_collisions_j and num_collisions_i == current_collisions_i:
                #Execute collision across the ith and jth ball                
                self.balls[i].collide_with_ball(self.balls[j])
                #update collision times for both the ith and jth ball
                self.update_collision_times(i)
                self.update_collision_times(j)
                
        #update the canvas to draw the new locations of each ball
        self.canvas.update()

        self.canvas.after(self.refresh_speed, self.refresh) #Calls the function again

#Class Ball defines the data and methods for the Ball object
class Ball:
    #__init__ defines the displacement, velocity, mass, and the color of the ball
    def __init__(self, radius, x, y, vx, vy,  mass, tk_rgb="#000000"):
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.tk_rgb = tk_rgb
        #count represents the number of collision for this instance of a ball object
        #since this ball was just initialized, it hasn't had any collisions yet
        self.count = 0
        return

    #move changes the displacement of the ball by the velocity
    def move(self, dt=1.0):
        self.x += self.vx*dt
        self.y += self.vy*dt
        return

    #check_overlap checks if this ball is overlapping with any other
    #ball, it is used to see if a collision has occurred
    def check_overlap(self, others):
        for b in others:
            min_dist = b.radius + self.radius
            center_dist = math.sqrt((b.x - self.x)*(b.x - self.x) + \
                                    (b.y - self.y)*(b.y - self.y))
            if center_dist < min_dist:
                return True
        return False
        
    #collide_with_ball computes collision, changing the Ball's velocity
    #as well as the other ball's velocity
    def collide_with_ball(self, other):
        dv_x = other.vx - self.vx
        dv_y = other.vy - self.vy

        dr_x = other.x - self.x
        dr_y = other.y - self.y

        sigma = self.radius + other.radius
        
        dv_dr = dv_x * dr_x + dv_y * dr_y

        J = 2.0 * self.mass * other.mass * dv_dr/((self.mass + other.mass)*sigma)
        Jx = J * dr_x/sigma
        Jy = J * dr_y/sigma

        self.vx += Jx/self.mass
        self.vy += Jy/self.mass

        other.vx -= Jx/other.mass
        other.vy -= Jy/other.mass
        #Increment the collision count for both balls
        self.count += 1
        other.count += 1
        return
    
    # Compute when an instance of Ball collides with the given Ball other
    # Return the timestamp that this will occur
    def ball_collision_time(self, other):
        
        dr_x = other.x - self.x
        dr_y = other.y - self.y

        if dr_x == 0 and dr_y == 0:
            return float('inf')
        
        dv_x = other.vx - self.vx
        dv_y = other.vy - self.vy

        dv_dr = dv_x * dr_x + dv_y * dr_y
        
        if dv_dr > 0:
            return float('inf')
        
        dv_dv = dv_x * dv_x + dv_y * dv_y
        dr_dr = dr_x * dr_x + dr_y * dr_y
        sigma = self.radius + other.radius

        d = dv_dr * dv_dr - dv_dv * (dr_dr - sigma * sigma) 
        
        # No solution 
        if d < 0 or dv_dv == 0:
            return float('inf')
        return - (dv_dr + np.sqrt(d))/dv_dv
    
    #collide_with_horizontal_wall executes the change in the Ball's
    #velocity when colliding with a horizontal wall
    def collide_with_horizontal_wall(self):
        self.vx = -self.vx
        self.count += 1
        return
    #collide_with_vertical_wall executes the change in the Ball's
    #velocity when colliding with a vertical wall
    def collide_with_vertical_wall(self):
        self.vy = -self.vy
        self.count += 1
        return

    # Compute when the instance of Ball collides with a horizontal wall
    # Return the time stamp that this will occur 
    # Inputs of min_x and max_x are the wall coordinates for both horizontal walls  
    def horizontal_wall_collision_time(self, min_x, max_x):
        if self.vx < 0:
            # x + delta_t * vx = min_x + radius
            return (min_x + self.radius - self.x)/(1.0*self.vx)
                
        if self.vx > 0:
            # x + delta_t * vx = max_x - radius
            return (max_x - self.radius - self.x)/(1.0*self.vx)
        
        return float('inf')

    # Compute when the instance of Ball collides with a vertical wall
    # Return the time stamp that this will occur 
    # Inputs of min_y and max_y 
    def vertical_wall_collision_time(self, min_y, max_y):
        if self.vy < 0:
            # y + delta_t * vy = min_y + radius
            return (min_y + self.radius - self.y)/(1.0*self.vy)
                
        if self.vy > 0:
            # y + delta_t * vy = max_y - radius
            return (max_y - self.radius - self.y)/(1.0*self.vy)
        
        return float('inf')

    #show_stats will print out the Ball's data
    #specifically the radius, position, velocity, mass, and color
    def show_stats(self):
        print("radius: %f"%self.radius)
        print("position: %f, %f"%(self.x, self.y))
        print("velocity: %f, %f"%(self.vx, self.vy))
        print("mass: %f"%self.mass)
        print("rgb: %s"%self.tk_rgb)
        return

#This link is to the discussion section assignment of the week
"https://users.soe.ucsc.edu/~rcompton/CMPS101/collision.txt" 

#Main script
if __name__ == "__main__":
    
    #Set the parameters for the graphics window and simulation
    scale = 800
    border = 5
    #Set radius range for all balls
    max_radius = 20
    min_radius = 5
    #set number of balls
    num_balls = 10
    #set refresh rate
    refresh_speed = 5
    #seed used to ensure consistent random values returned from using rand.random
    rand.seed(12394)
    #create the graphics object
    root = Tk()
    #Create the painter object
    p = Painter(root, scale, border, refresh_speed, None, min_radius, max_radius, num_balls)
    #If you have the commented out files in your directory then
    #uncomment them to see what they do
    #p = Painter(root, scale, border, refresh_speed, 'wallbouncing.txt')
    #p = Painter(root, scale, border, refresh_speed, 'p10.txt')
    #p = Painter(root, scale, border, refresh_speed, 'billiards4.txt')
    #p = Painter(root, scale, border, refresh_speed, 'squeeze.txt')
    
    #run the Painter main loop function (calls refresh many times)
    root.mainloop()
    


