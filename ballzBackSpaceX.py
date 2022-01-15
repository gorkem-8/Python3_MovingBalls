#This code visualize random colorful balls colliding, which are moving with random speeds.

from tkinter import *
import time
import random

#Below code block forms the animation template.

gui = Tk()
width_val=800
height_val=550
gui.geometry(str(width_val)+"x"+str(height_val))
gui.title("BackSpaceX Ball Bouncing")
canvas = Canvas(gui, width=width_val,height=height_val,bg='black')
canvas.pack()

#Each ball has the properties of the below class. They are defined with 4 coordinates, 
#Which are top left point X,Y and bottomright point X,Y. They have 2 velocity vectors in 
#x and y directions. And lastly they have a color. 

class ball:

    def __init__(self):
        randomNumbers = [-4,-3,-2,-1,1,2,3,4] #for velocity choice, random number array.
        self.velocityX = random.choice(randomNumbers)  
        self.velocityY = random.choice(randomNumbers)           
        self.diameter = 30 
        self.topLeftX = random.randint(0,width_val-self.diameter)
        self.topLeftY = random.randint(0,height_val-self.diameter)
        self.bottomRightX =self.topLeftX+self.diameter #Diameter is set to 30 as defualt settings.
        self.bottomRightY = self.topLeftY+self.diameter
        self.color=['red','blue','green'][random.randint(0,2)] #Color array for random coloring.
        self.selfintopu=canvas.create_oval(self.topLeftX,self.topLeftY,self.bottomRightX,self.bottomRightY,fill=self.color) #This
        #line draws the ball in the canvas plate.
        self.pos=canvas.coords(self.selfintopu) # This coords command helps to save the actual positions of the 4 position data
        #of a ball.

    def Move(self): #This method is built for moving the balls.
        canvas.move(self.selfintopu,self.velocityX,self.velocityY)
        self.pos=canvas.coords(self.selfintopu) 
        if self.color=='blue': # This condition is built for letting the blue ball to pass through the walls.
            if self.pos[1] <= -(self.diameter-10): # Top Wall condition.
                canvas.moveto(self.selfintopu, self.pos[0]+self.diameter/2, height_val-self.diameter-10)    
            if self.pos[3] >= height_val+(self.diameter-10): # Bottom Wall condition.
                canvas.moveto(self.selfintopu, self.pos[0]+self.diameter/2, self.diameter)
            if self.pos[0] <= (self.diameter-10): #Left wall condition.
                canvas.moveto(self.selfintopu, width_val-self.diameter, self.pos[1]+self.diameter/2)
            if self.pos[2] >= width_val+(self.diameter-10): #Right wall condition.
                canvas.moveto(self.selfintopu, self.diameter-10 , self.pos[1]+self.diameter/2) 
        elif self.color == 'red' or self.color == 'green': #This condition helps the green and red balls
            #to bound from the walls.
            if self.pos[3] >= height_val or self.pos[1] <=0 :
                self.velocityY = -self.velocityY
            if self.pos[2] >= width_val or self.pos[0] <=0 :
                self.velocityX = -self.velocityX

    def check_collision(self,otherObject): #This method is comparing two balls for whether they are colliding
        #or not. If they are colliding, this method returns 1 when it is called in the main code.
        if self.pos[2]>=otherObject.pos[0] and self.pos[0] <= otherObject.pos[2]:
            if self.pos[3] >= otherObject.pos[1] and self.pos[1] <= otherObject.pos[3]:
                return 1 
        else:
            return 0

    def bug_move(self): 
        '''
        This method will be used when the balls are stuck in each other and can not escape from each other.
        It moves them from 5 unit away from the actual center point.
        '''
        canvas.moveto(self.selfintopu, self.pos[0]+5,self.pos[1]+5)
        
    def change_color_same(self, otherObject):
        '''
        This method changes the colors of the two same colored colliding balls to different colors. 
        '''
        color_list=['red','blue','green']
        color_list.remove(self.color)
        self.color=color_list[0]
        otherObject.color=color_list[1]
        canvas.itemconfig(self.selfintopu,fill=self.color)
        canvas.itemconfig(otherObject.selfintopu,fill=otherObject.color)

    def change_velocity(self, otherObject):
        '''
        This method changes the velocities of colliding balls to opposite directions.
        '''
        self.velocityX=-self.velocityX
        self.velocityY=-self.velocityY
        otherObject.velocityX=-otherObject.velocityX
        otherObject.velocityY=-otherObject.velocityY

    def destroy_ball(self):
        '''
        This method sends the ball to the far away than our canvas plate.It sends 
        too fast that, no ball can come back from that place...So visually, ball
        is destroyed :(
        '''
        self.color = 'black'
        canvas.itemconfig(self, fill = 'black')
        canvas.moveto(self,width_val+1000,height_val+1000) 
        self.velocityX = 4000 
        self.velocityY = 4000

    def bigger_ball(self):
        '''
        This method deletes the drawing first, and then creates the drawing as bigger ball when a ball collides,
        if the probability is satisfied in the main code.
        '''
        self.diameter = self.diameter+10
        self.selfintopu = canvas.delete(self.selfintopu)
        self.selfintopu = canvas.create_oval(self.pos[0],self.pos[1],self.pos[2]+10,self.pos[3]+10,fill=self.color)
        


    def change_color_different(self,otherObject):
        '''
        If both of the colliding balls have different colors, this method converts their color to the 
        remaining color.
        '''
        color_list=['red','blue','green']
        for i in color_list:
            if i!=self.color:
                if i!=otherObject.color:
                    self.color=i
                    otherObject.color=i
                    break
        canvas.itemconfig(self.selfintopu,fill=self.color)
        canvas.itemconfig(otherObject.selfintopu,fill=otherObject.color)

    def check_color(self,objList):
        '''
        This code checks whether the color of a ball is red or not. If there is a red ball found, the method
        adds it to the red list. This list will be used in forming the triangle in the main code.
        '''
        red_list=[]
        if self.color=='red':
            red_list.append(0)
        for index, obj in enumerate(objList):
            if obj.color=='red':
                red_list.append(index+1)
        return red_list

    def draw_triangle(self,obj1, obj2):
        '''
        This method draws a triangle by taking totally 6 data from 3 balls which are their X and Y values.
        '''
        c=[((self.pos[0]+self.pos[2])/2),((self.pos[1]+self.pos[3])/2),((obj1.pos[0]+obj1.pos[2])/2),((obj1.pos[1]+obj1.pos[3])/2),((obj2.pos[0]+obj2.pos[2])/2),((obj2.pos[1]+obj2.pos[3])/2)]
        triangle=canvas.create_polygon(c, outline='white',fill="")
        return triangle

    def move_triangle(self,obj1,obj2):
        '''
        This method defines the triangle's position  when it is called in each time step.
        '''
        center=[((self.pos[0]+self.pos[2])/2),((self.pos[1]+self.pos[3])/2),((obj1.pos[0]+obj1.pos[2])/2),((obj1.pos[1]+obj1.pos[3])/2),((obj2.pos[0]+obj2.pos[2])/2),((obj2.pos[1]+obj2.pos[3])/2)]
        return center

####### MAIN CODE ########
ball_number=random.randint(15,25) # Number of the balls is selected randomly in this line.
objects = [] # Ball objects are saved in this list.

for k in range(ball_number): # This loop saves each ball objects to the ball list.
    k=ball()
    objects.append(k)

try:
    red_list = objects[0].check_color(objects[1::]) # This line adds the red balls to the red list.
    if len(red_list)>=3: # If there are 3 balls, triangle will be created.
        triangle=objects[red_list[0]].draw_triangle(objects[red_list[1]],objects[red_list[2]])
        center=canvas.coords(triangle)
except:
    pass

while True: # Continious loop for plotting the balls in the canvas.
    for element in list(objects):
        element.Move()
    try:
        red_list=objects[0].check_color(objects[1::])
        if len(red_list)>=3: # This condition defines the triangle for the current positions.
            center=objects[red_list[0]].move_triangle(objects[red_list[1]],objects[red_list[2]])
            canvas.coords(triangle, center)
        else:
            canvas.moveto(triangle,-2000,-2000) # Triangle is moved to the far mountains if there are not enough red balls.
    except:
        pass

    for i in range(len(objects)): #This loop compares the objects with each other in the objects list.
        for j in range(i+1,len(objects)):
            if i is not j: #In order to not comparing the same object with itself. 
                if objects[i].check_collision(objects[j]): #Objects are checked whether they are colliding or not.
                    a=random.randint(1,3)
                    if a == 1: # by 33% probability, one of the colliding object is destroyed, and the size of the other one
                        #is increased.
                        objects[i].destroy_ball()
                        objects[j].bigger_ball() 
                        
                    else: # by 66% probability, the colliding balls are swapping the colors.
                    
                        objects[i].change_velocity(objects[j])
                        if objects[i].color==objects[j].color:
                            objects[i].change_color_same(objects[j])
                        else:
                            objects[i].change_color_different(objects[j])
    

    gui.update()
    time.sleep(.025)
        
gui.mainloop()
