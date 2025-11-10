import turtle
import time

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("I Love You!!")

# Create the turtle for drawing
heart = turtle.Turtle()
heart.speed(0)
heart.hideturtle()

# Function to draw a heart
def draw_heart(x, y, size, color):
    heart.penup()
    heart.goto(x, y)
    heart.pendown()
    heart.color(color)
    heart.begin_fill()
    heart.left(140)
    heart.forward(size)
    for _ in range(200):
        heart.right(1)
        heart.forward(size * 0.01)
    heart.left(120)
    for _ in range(200):
        heart.right(1)
        heart.forward(size * 0.01)
    heart.forward(size)
    heart.end_fill()
    heart.setheading(0)

# Function to write text
def write_text(x, y, text, color, font_size):
    heart.penup()
    heart.goto(x, y)
    heart.color(color)
    heart.write(text, align="center", font=("Arial", font_size, "bold"))

# Animate the heart (pulsing effect)
size = 100
while True:
    # Clear previous drawing
    heart.clear()
    
    # Draw the heart
    draw_heart(0, -50, size, "red")
    
    # Write the text
    write_text(0, -150, "I Love You!!", "white", 24)
    
    # Update screen
    screen.update()
    
    # Pulse effect: increase and decrease size
    size += 5
    if size > 150:
        size = 100
    
    time.sleep(0.1)
