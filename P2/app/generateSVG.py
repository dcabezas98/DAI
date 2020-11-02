# Generates random SVG figures

from SVG import *
from random import randint

def randSVG():
    n = randint(1,3) # Select figure

    if n == 1: # Triangle
        return draw_triangle()
    
    elif n == 2: # Ellipse
        return draw_ellipse()

    elif n == 3: # Rectangle
        return draw_rectangle()

def draw_triangle():
    scene = Scene("triangle")
    point1= (randint(10,490),randint(10,490))
    point2= (randint(10,490),randint(10,490))
    point3= (randint(10,490),randint(10,490))
    points=[point1,point2,point3]
    fill_color=(randint(0,255),randint(0,255),randint(0,255))
    line_color=(randint(0,255),randint(0,255),randint(0,255))
    line_width=randint(1,4)
    scene.add(Polygon(points,fill_color,line_color,line_width))
    return scene.strarray()

def draw_ellipse():
    scene = Scene("ellipse")
    center= (randint(200,400),randint(200,400))
    radius_x=randint(50,150)
    radius_y=randint(50,150)
    fill_color=(randint(0,255),randint(0,255),randint(0,255))
    line_color=(randint(0,255),randint(0,255),randint(0,255))
    line_width=randint(1,4)
    scene.add(Ellipse(center,radius_x,radius_y,fill_color,line_color,line_width))
    return scene.strarray()

def draw_rectangle():
    scene = Scene("rectangle")
    
    origin=(randint(50,200),randint(50,200))
    height=randint(50,200)
    width=randint(50,200)
    fill_color=(randint(0,255),randint(0,255),randint(0,255))
    line_color=(randint(0,255),randint(0,255),randint(0,255))
    line_width=randint(1,4)
    scene.add(Rectangle(origin,height,width,fill_color,line_color,line_width))
    return scene.strarray()

if __name__ == "__main__": randSVG()
    
