# Generates random SVG figures

from random import randint

colors=['green', 'red', 'yellow', 'blue', 'orange', 'brown', 'pink', 'purple', 'black']
ncolors=len(colors)
   
def randSVG():
    n = randint(1,2) # Select figure
    if n == 1: # Ellipse
        return [1]+ ellipse()

    elif n == 2: # Rectangle
        return [2]+ rectangle()

def ellipse():
    cx = randint(225,350)
    cy = randint(175,300)
    rx = randint(50,200)
    ry = randint(50,150)
    fill = colors[randint(0,ncolors-1)]
    return list(map(str,[cx, cy, rx, ry, fill]))

def rectangle():    
    x=randint(25,300)
    y=randint(25,250)
    width=randint(50,250)
    height=randint(50,200)
    fill = colors[randint(0,ncolors-1)]
    return list(map(str,[x, y, width, height, fill]))

