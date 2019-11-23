from tkinter import *
import time
import random

t = Tk()
t.title("Conways game of life")
t.resizable(False,False)
c = Canvas(t, width=1200, height=600)
c.pack()

class node:
    count = 0
    def __init__(self):
        self.alive = False
    def __str__(self):
        self.alive
    def kill(self):
        self.alive = False
    def ITS_ALIVE(self):
        self.alive = True
    def poke(self):
        return self.alive
    def __str__(self):
        if self.alive==True:
            return "T"+str(self.count)+"    "
        else:
            return "F"+str(self.count)+"    "
    def __eq__(self, value):
        return self.alive == value
    def color(self):
        if self.alive==True:
            return "Blue"
        else:
            return "White"
class grid:
    def get(self,x,y):
        return self.data[x,y]
    def __init__(self,width =100, height=50):
        self.data = [[],[]]
        self.width =width
        self.height =height
        for i in range(self.height):
            for j in range(self.width):
                self.data[i].append(node())
            self.data.append([])
    def set(self,other):
        self.data = other.data
    def __str__(self):
        sss =""
        for i in self.data:
            sss += "\n"
            for j in i:
                sss += j.__str__()
        return sss
    def surviving(self):
        ret =[]
        c1 =0
        for i in self.data:
            c2=0
            for j in i:
                if j.alive == True:
                    ret.append([c1,c2])
                c2+=1
            c1+=1
        return ret

def iter(g):
    nu = grid()
    checked =[]
    for i in g.surviving():
        #print(i[0])
        h = i[0]
        w = i[1]
        if h == 0:
            rows = [g.height-1,h,h+1]
        elif h == g.height-1:
            rows = [h-1,h,0]
        else:
            rows = [h-1,h,h+1]

        if w == 0:
            collumns = [g.width-1,w,w+1]
        elif w == g.width-1:
            collumns = [w-1,w,0]
        else:
            collumns = [w-1,w,w+1]
        for i in rows:
            for j in collumns:
                if [i,j] in checked:
                    continue
                checked.append([i,j])
                if i == 0:
                    t_rows = [g.height-1,i,i+1]
                elif i == g.height-1:
                    t_rows = [i-1,i,0]
                else:
                    t_rows = [i-1,i,i+1]
                if j == 0:
                    t_collumns = [g.width-1,j,j+1]
                elif j == g.width-1:
                    t_collumns = [j-1,j,0]
                else:
                    t_collumns = [j-1,j,j+1]
                check(nu,g,t_rows,t_collumns)

    g.set(nu)
def check(nu,g,rows,collumns):
    count=0
    h = rows[1]
    w = collumns[1]
    for i in rows:
        for j in collumns:
            if count >=4:
                pass
            if g.data[int(i)][int(j)].__eq__(True):
                count+=1
    if g.data[h][w].alive:
        count -=1
    g.data[h][w].count = count
    if count<2:
        nu.data[h][w].kill()
    elif count == 3:
        nu.data[h][w].ITS_ALIVE()
    elif count==2:
        if g.data[h][w].alive == True:
           nu.data[h][w].ITS_ALIVE()
    elif count > 3:
        nu.data[h][w].kill()

def display(g):
    global c
    w = (c.winfo_width()//g.width)
    h = (c.winfo_height()//g.height)
    w=h=min([w,h])
    w_offset =0
    h_offset =0
    color = "Blue"
    for i in range(g.height):
        for j in range(g.width):
            color = g.data[i][j].color()
            c.create_rectangle(w_offset, h_offset, w+w_offset, h+h_offset, fill=color,outline ="light grey")
            w_offset+=w
        h_offset+=h
        w_offset=0
def generate(g):
    g = grid()
    for i in range(0, g.height):
        for j in range(0, g.width):
            rand = random.random()
            if rand > 0.5:
                g.data[i][j].ITS_ALIVE()
    return g

g =generate(grid())
display(g)
for i in range(1000):
    c.delete("all")
    display(g)
    c.update_idletasks()
    c.update()
    iter(g)
    time.sleep(.02)




mainloop()



'''
- Any live cell with fewer than two live neighbours dies, as if caused by underpopulation
- Any live cell with two or three live neighbours lives on to the next generation
- Any live cell with more than three live neighbours dies, as if by overpopulation
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
'''