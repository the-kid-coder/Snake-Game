
import turtle
import random

WIDTH = 700
HEIGHT = 700
MOVE_DISTANCE = 22
GAME_SPEED = 120

BACKGROUND_COLOR = "#17212b"
LIGHT_SQUARE = "#1e2d3a"
GRID_COLOR = "#293743"
SNAKE_COLOR = "#39d98a"
FOOD_COLOR = "#ff5252"
TEXT_COLOR = "white"

screen = turtle.Screen()
screen.title("SNAKE - Arcade Edition")
screen.setup(WIDTH, HEIGHT)
screen.bgcolor(BACKGROUND_COLOR)
screen.tracer(0)

snake = []
food = None
score = 0
direction = "Right"
running = False
score_writer = None

def create_segment(x, y, color=SNAKE_COLOR):
    segment = turtle.Turtle()
    segment.shape("square")
    segment.color(color)
    segment.penup()
    segment.goto(x, y)
    segment.speed(0)
    return segment

def draw_grid():
    grid = turtle.Turtle()
    grid.hideturtle()
    grid.speed(0)
    grid.penup()
    grid.pensize(1)

    for row in range(31):
        for col in range(31):
            x = -330 + col * MOVE_DISTANCE
            y = -330 + row * MOVE_DISTANCE

            if (row + col) % 2 == 0:
                grid.color(LIGHT_SQUARE)
            else:
                grid.color(BACKGROUND_COLOR)

            grid.goto(x - 11, y - 11)
            grid.setheading(0)
            grid.pendown()
            grid.begin_fill()

            for _ in range(4):
                grid.forward(MOVE_DISTANCE)
                grid.left(90)

            grid.end_fill()
            grid.penup()

    grid.color(GRID_COLOR)

    for i in range(32):
        position = -341 + i * MOVE_DISTANCE

        grid.goto(position, -341)
        grid.pendown()
        grid.goto(position, 341)
        grid.penup()

        grid.goto(-341, position)
        grid.pendown()
        grid.goto(341, position)
        grid.penup()

def create_snake():
    global snake
    snake = [create_segment(0, 0)]

def create_food():
    global food

    if food:
        food.hideturtle()

    while True:
        x = random.randint(-15, 15) * MOVE_DISTANCE
        y = random.randint(-15, 15) * MOVE_DISTANCE

        if not any(segment.xcor() == x and segment.ycor() == y for segment in snake):
            break

    food = create_segment(x, y, FOOD_COLOR)
    food.shape("circle")

def update_score():
    score_writer.clear()
    score_writer.write(
        f"SCORE: {score}",
        align="center",
        font=("Arial", 20, "bold")
    )

def move():
    global snake, score

    head = snake[0]
    x = head.xcor()
    y = head.ycor()

    if direction == "Up":
        y += MOVE_DISTANCE
    elif direction == "Down":
        y -= MOVE_DISTANCE
    elif direction == "Left":
        x -= MOVE_DISTANCE
    elif direction == "Right":
        x += MOVE_DISTANCE

    new_head = create_segment(x, y)
    snake.insert(0, new_head)

    if new_head.distance(food) < 5:
        score += 10
        update_score()
        create_food()
    else:
        tail = snake.pop()
        tail.hideturtle()

def detect_collision():
    head = snake[0]

    if (
        head.xcor() >= WIDTH // 2 - 10
        or head.xcor() <= -WIDTH // 2 + 10
        or head.ycor() >= HEIGHT // 2 - 10
        or head.ycor() <= -HEIGHT // 2 + 10
    ):
        return True

    for segment in snake[1:]:
        if head.distance(segment) < 5:
            return True

    return False

def update():
    global running

    if not running:
        return

    move()

    if detect_collision():
        running = False
        game_over()
        return

    screen.update()
    screen.ontimer(update, GAME_SPEED)

def up():
    global direction
    if direction != "Down":
        direction = "Up"

def down():
    global direction
    if direction != "Up":
        direction = "Down"

def left():
    global direction
    if direction != "Right":
        direction = "Left"

def right():
    global direction
    if direction != "Left":
        direction = "Right"

def show_start_screen():
    writer = turtle.Turtle()
    writer.hideturtle()
    writer.color(TEXT_COLOR)
    writer.penup()

    writer.goto(0, 100)
    writer.write("SNAKE", align="center", font=("Arial", 48, "bold"))

    writer.goto(0, 30)
    writer.write("ARCADE EDITION", align="center", font=("Arial", 18, "normal"))

    writer.goto(0, -50)
    writer.write("Use the ARROW KEYS to move", align="center", font=("Arial", 16, "normal"))

    writer.goto(0, -100)
    writer.write("Press SPACE to start", align="center", font=("Arial", 18, "bold"))

def game_over():
    screen.clear()
    screen.bgcolor(BACKGROUND_COLOR)

    writer = turtle.Turtle()
    writer.hideturtle()
    writer.color(FOOD_COLOR)
    writer.penup()

    writer.goto(0, 70)
    writer.write("GAME OVER", align="center", font=("Arial", 38, "bold"))

    writer.color(TEXT_COLOR)

    writer.goto(0, 10)
    writer.write(f"FINAL SCORE: {score}", align="center", font=("Arial", 22, "normal"))

    writer.goto(0, -60)
    writer.write("Press SPACE to play again", align="center", font=("Arial", 16, "normal"))

    screen.update()
    setup_controls()

def start_game():
    global running, score, direction, snake, food, score_writer

    if running:
        return

    screen.clear()
    screen.bgcolor(BACKGROUND_COLOR)
    screen.tracer(0)

    score = 0
    direction = "Right"
    snake = []
    food = None

    draw_grid()
    create_snake()
    create_food()

    score_writer = turtle.Turtle()
    score_writer.hideturtle()
    score_writer.color(TEXT_COLOR)
    score_writer.penup()
    score_writer.goto(0, HEIGHT // 2 - 50)

    running = True

    setup_controls()
    update_score()
    screen.update()
    update()

def setup_controls():
    screen.listen()
    screen.onkey(up, "Up")
    screen.onkey(down, "Down")
    screen.onkey(left, "Left")
    screen.onkey(right, "Right")
    screen.onkey(start_game, "space")

setup_controls()
show_start_screen()
screen.update()

screen.mainloop()
