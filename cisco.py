from turtle import *
turtle = Turtle()
screen = Screen()
screen.bgcolor(0, 0, 0)
turtle.speed(10)
Color = ["Red", "Purple", "Blue", "Green", "Yellow", "Orange"]
for i in range (360): 
    turtle.color(Color[i%6])
    turtle.width(i/100+1)
    turtle.forward(i)
    turtle.left(59)
