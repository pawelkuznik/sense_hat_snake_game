# ################# SNAKE GAME ##########################
Url: https://github.com/pawelkuznik/sense_hat_snake_game

import time, random
from sense_emu import SenseHat
#create instance of sensor
sense = SenseHat()
# define colors of objects
red = (255, 0, 0)
white = (255, 255, 255)
clear = (0, 0, 0)
 
# coordinates of snake body
snake_trail = [[3, 3]] # center by default
snake_direction = [1, 0] # right by default
snake_length = 1
 
food_position = [random.randint(0, 7), random.randint(0, 7)]
 
pixels = [clear] * 64
# 0 = up,
# 1 = right
# 2 = down
# 3 = left
def set_snake_direction(d):
    global snake_direction
 
    if d == 0:
        snake_direction = [0, -1]
    elif d == 1:
        snake_direction = [1, 0]
    elif d == 2:
        snake_direction = [0, 1]
    elif d == 3:
        snake_direction = [-1, 0]
# ################### GAME LOOP #################       
while True:
    pixels = [clear] * 64
# handle joystick press   
    for event in sense.stick.get_events():
        if event.action == "pressed":  
            if event.direction == "up":
                set_snake_direction(0)
            elif event.direction == "right":
                set_snake_direction(1)
            elif event.direction == "down":
                set_snake_direction(2)
            elif event.direction == "left":
                set_snake_direction(3)
# illusion of snake moving               
    snake_trail.insert(0, [snake_trail[0][0] + snake_direction[0], snake_trail[0][1] + snake_direction[1]])
# chck when snake meet wall - colision
    if snake_trail[0][0] < 0:
        snake_trail[0][0] = 7
    if snake_trail[0][1] < 0:
        snake_trail[0][1] = 7
    if snake_trail[0][0] > 7:
        snake_trail[0][0] = 0
    if snake_trail[0][1] > 7:
        snake_trail[0][1] = 0
 
# check colisons etc (first list element)    
    if snake_trail[0] == food_position:
        food_position = []
        while food_position == []:
            food_position = [random.randint(0, 7), random.randint(0,7)]
            if food_position in snake_trail:
                food_position = []
            snake_length += 1
    elif snake_trail[0] in snake_trail[1:]: # reset length if snke runs into itself
        snake_length = 1
    else:
        while len(snake_trail) > snake_length:
            snake_trail.pop()
 
    for snake_position in snake_trail:
        pixels[snake_position[1] * 8 + snake_position[0]] = white
 
    # convert two dimention to one dimmenssion
    # y * row_size
 
    pixels[food_position[1] * 8 + food_position[0]] = red
    sense.set_pixels(pixels)
 
    time.sleep(0.20)
