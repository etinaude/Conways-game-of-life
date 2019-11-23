from tkinter import *
import time
import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~User options~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
x=100                       #number of cells across                     ~
y=50                        #number of cells down                       ~
iterations=1000             #number of iterations before pausing        ~
speed=0.1                   #delay between iterations in milliseconds   ~
alive_color = "Blue"        #color of living cells                      ~
dead_color = "white"        #color of dead cells                        ~
chance = 0.5                #chance a cell will start out alive         ~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''' 
Conway's game of life rules:

- Any live cell with fewer than two live neighbours dies, as if caused by underpopulation
- Any live cell with two or three live neighbours lives on to the next generation
- Any live cell with more than three live neighbours dies, as if by overpopulation
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
'''
#classes
class node:
    #each cell is an object of type cell
    global alive_color,dead_color
    count = 0
    def __init__(self):
        #initilize
        self.alive = False
    def murder(self):
        #kill cell (rip it away from it's wife and family)
        self.alive = False
    def ITS_ALIVE(self):
        #revive the cell, (playing god)
        self.alive = True
    def poke(self):
        #prod the cell with a stick to test if it's alive
        return self.alive
    def __str__(self):
        #returns a formatted string with it's state and count of living neighbors
        if self.alive==True:
            return "T"+str(self.count)+"    "
        else:
            return "F"+str(self.count)+"    "
    def color(self):
        #returns a color base on weather its alive 
        if self.alive==True:
            return alive_color
        else:
            return dead_color
class grid:
    #the grid is an object holding nodes 
    global x,y,chance
    def __init__(self):
        #initalizes the grid
        self.data = [[]]
        self.width =x
        self.height =y
        for i in range(self.height):
            for j in range(self.width):
                self.data[i].append(node())
            self.data.append([])
    def set(self,other):
        #sets the grid to the values in another grid
        self.data = other.data
    def __str__(self):
        #returns a formatted string of all the cells in it
        sss =""
        count = 0
        for i in self.data:
            sss += "\n"
            for j in i:
                sss += j.__str__()
                count += j.count
        sss += "\ntotal = " +str(count)
        return sss
    def generate(self):
        #generates random cell patern
        for i in range(0, self.height):
            for j in range(0, self.width):
                rand = random.random()
                if rand > (1-chance):
                    self.data[i][j].ITS_ALIVE()
        return self
#helper functions
def iter(g):
    #performs an interation of the game of life
    nu = grid()
    for h in range(g.height):
        #loops through rows
        if h == 0:
            rows = [g.height-1,h,h+1]
        elif h == g.height-1:
            rows = [h-1,h,0]
        else:
            rows = [h-1,h,h+1]
        for w in range(g.width):
            #loops through collumns
            if w == 0:
                collumns = [g.width-1,w,w+1]
            elif w == g.width-1:
                collumns = [w-1,w,0]
            else:
                collumns = [w-1,w,w+1]
            
            #count living neighbours
            count=0
            for i in rows:
                for j in collumns:
                    if g.data[int(i)][int(j)].poke():
                        count+=1
            if g.data[h][w].poke():
                count -=1

            #applies the rules
            if count<2:
                nu.data[h][w].murder()
            elif count == 3:
                nu.data[h][w].ITS_ALIVE()
            elif count==2:
                if g.data[h][w].poke() == True:
                   nu.data[h][w].ITS_ALIVE()
            elif count > 3:
                nu.data[h][w].murder()
    #sets the grid to teh new values
    g.set(nu)
def display(g):
    #displays the grid on a GUI
    global c
    #makes all cells squares based on the smallest space
    w = (c.winfo_width()//g.width)
    h = (c.winfo_height()//g.height)
    w=h=min([w,h])
    w_offset =0
    h_offset =0
    color = "error"
    #loops through rows and collumn setiing rectangle colors
    for i in range(g.height):
        for j in range(g.width):
            color = g.data[i][j].color()
            c.create_rectangle(w_offset, h_offset, w+w_offset, h+h_offset, fill=color,outline ="light grey")
            w_offset+=w
        h_offset+=h
        w_offset=0

#application set up and running
t = Tk()
t.title("Conways game of life")
t.resizable(False,False)
c = Canvas(t, width=1200, height=600)
c.pack()

#creates start grid
g = grid()
g.generate()
for i in range(iterations):
    #iterates and updates grid and graphics
    c.delete("all")
    display(g)
    c.update_idletasks()
    c.update()
    iter(g)
    time.sleep(speed)

mainloop()