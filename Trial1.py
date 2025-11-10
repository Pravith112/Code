import turtle
import math
import random

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("I Love You!!")
screen.setup(width=800, height=700)
screen.tracer(0)  # turn off automatic animation

# Create the turtle for drawing the heart
heart = turtle.Turtle()
heart.hideturtle()
heart.speed(0)
heart.pensize(2)

# Separate turtle for writing text
writer = turtle.Turtle()
writer.hideturtle()
writer.speed(0)
writer.penup()

# Create a few twinkle stars in the background (draw once)
stars = []
for _ in range(40):
    sx = random.randint(-380, 380)
    sy = random.randint(-320, 320)
    size = random.uniform(1.0, 3.0)
    stars.append((sx, sy, size))

def draw_stars():
    star_t = turtle.Turtle()
    star_t.hideturtle()
    star_t.speed(0)
    star_t.penup()
    for (sx, sy, s) in stars:
        star_t.goto(sx, sy)
        # small flicker by randomizing short-lived brightness when drawn
        star_t.dot(int(s * 2 + random.choice([0, 1, 2])), "white")

# Heart drawing function (scales cleanly)
def draw_heart(x, y, size, color):
    heart.penup()
    heart.goto(x, y)
    heart.setheading(0)
    heart.pendown()
    heart.color(color)
    heart.begin_fill()

    # Classic heart made from two circular arcs and straight edges
    heart.left(140)
    heart.forward(size * 1.0)

    # The radius is proportional to size. Negative radius to make arcs curve inward.
    heart.circle(-size * 0.6, 200)
    heart.left(120)
    heart.circle(-size * 0.6, 200)
    heart.forward(size * 1.0)
    heart.end_fill()
    heart.setheading(0)
    heart.penup()

def write_text(x, y, text, color, font_size):
    writer.clear()
    writer.goto(x, y)
    writer.color(color)
    writer.write(text, align="center", font=("Arial", font_size, "bold"))

# Animation state
size = 70            # nominal heart "radius" scale
min_size = 70
max_size = 140
growing = True
hue_index = 0        # used to change color over time

def tween_color(i):
    # simple smooth color change between red -> hotpink -> red
    # returns an HTML-style color string that turtle accepts (tk color names or hex)
    # We'll interpolate between two RGB colors:
    r1, g1, b1 = (255, 30, 60)   # red-ish
    r2, g2, b2 = (255, 90, 140)  # pink-ish
    t = (math.sin(i * 0.06) + 1) / 2  # oscillates 0..1 smoothly
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    retur
