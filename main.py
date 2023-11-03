import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import ml
import re
import time

GRID_SIZE = 11
CELL_SIZE = 60
INP_PATTERN  = r'^\d+,\d+$'
GRID = ml.get_grid()
path = []
invalid_start_flag = False

def get_final_coordinates():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if GRID[row][col] == 2:
                return(row,col)
    return (0,0)

final_coordinates = get_final_coordinates()

def get_colors(row, col):
    color, line = " ", " "
    if (GRID[row][col]) == 0:   #path
        color = "white"
        line = "black"
    elif (GRID[row][col]) == 2: #goal
        color = "green"  
        line = "white"
    elif (GRID[row][col]) == 3: #current walking path
        color = "red"
        line = "white"
    else:                       #shelf
        color = "black"
        line = "white"

    return line, color


def input_validator(text):
    try:
        value = int(text)
        if 1 <= value <= GRID_SIZE:
            return True
        else:
            print("Only In Range 1 to 11 Inclusive")
            return False
    except (ValueError or TypeError):
        print("Only Integers")
        return False
    
def reset_grid():
    global path, GRID
    path = []
    GRID = [[0 if cell == 3 else cell for cell in row] for row in GRID]
    final_row, final_col = final_coordinates
    GRID[final_row][final_col] = 2

def input_handler(start_coordinates):
    reset_grid()    
    global path, invalid_start_flag, INP_PATTERN
    
    if re.match(INP_PATTERN, start_coordinates):
        pass
    else:
        print("ERROR : Invalid input format")
        return
    
    
    start_row, start_col = start_coordinates.split(",")

    if input_validator(start_row) and input_validator(start_col):
        start_row = int(start_row)
        start_col = int(start_col)
        if GRID[start_row-1][start_col-1]!=1:
            invalid_start_flag = False
            path_or_not  = ml.get_path(start_row-1, start_col-1)
            if path_or_not=="BOUNDED":
                invalid_start_flag = True
            else:
                path = path_or_not
                del path[-1]
        else:
            invalid_start_flag = True
    else:
        print("Invalid input. Please enter numbers between 1 and 11.")


def update_grid():

    if not path:
        return
    else:
        row, col = path[0]
        GRID[row][col] = 3  # Set cell color to red
        time.sleep(0.3)
        GRID[row][col] = 0  # Set cell color to red
        del path[0]

        
def draw_handler(canvas):
    global invalid_start_flag
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x0 = col * CELL_SIZE
            y0 = row * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE

            line, color = get_colors(row, col)

            if color=="black":
                canvas.draw_image(shelf, (shelf_w/2, shelf_h/2), (shelf_w, shelf_h), (x0+30, y0+30), (60, 60))
            elif color=="red":
                canvas.draw_image(robot, (robot_w/2, robot_h/2), (robot_w, robot_h), (x0+30, y0+30), (60, 60))
            elif color=="green":
                canvas.draw_image(goal, (goal_w/2, goal_h/2), (goal_w, goal_h), (x0+30, y0+30), (60, 60))
            else:
                canvas.draw_polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 1, line, color)
                canvas.draw_text(f"{(row+1)} {(col+1)}", (x0+30,y0+30), 15, "black")
    if(invalid_start_flag):
        frame.add_label('Invalid State')
        invalid_start_flag = False
                

ml.train()

timer_interval = 500
timer = simplegui.create_timer(timer_interval, update_grid)

frame = simplegui.create_frame("Warehouse Robot", GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
frame.add_input("Starting Location (a,b) : ", input_handler, 100)

shelf = simplegui._load_local_image('./shelf.png')
robot = simplegui._load_local_image('./robot.jpg')
goal = simplegui._load_local_image('./delivery.png')
shelf_w, shelf_h = shelf.get_width(), shelf.get_height()
robot_w, robot_h = robot.get_width(), robot.get_height()
goal_w, goal_h = goal.get_width(), goal.get_height()

frame.set_draw_handler(draw_handler)

timer.start()
frame.start()
