import turtle
import time
import colorsys
import keyboard as ky
import sys

colors = ()

grid_size=(4,5)  #x,y

# prebacit u cpp
def is_empty(position, xcheck, ycheck, max_x_size, max_y_size):
    empty = True
    for y in range(max((ycheck-max_y_size+1,0)), ycheck+1): #for y in range(max((ycheck-max_y_size+1,0)), ycheck+1):
        for x in range(max((xcheck-max_x_size, 0)), xcheck+1):
            for i in range(len(position[1])):
                if position[1][i] == y and position[0][i] == x:
                    if position[1][i]+size[1][i]-1 >= ycheck and position[0][i]+size[0][i]-1 >= xcheck:
                        empty = False
    return empty
def all_possible_moves(position, max_x_size, max_y_size):
    moves=[]
    for shape in range(len(position[0])):
        if position[1][shape]+size[1][shape] != grid_size[1]:
            is_move_possible = True
            for i in range(size[0][shape]):
                if not is_empty(position, position[0][shape]+i, position[1][shape]+size[1][shape], max_x_size, max_y_size):
                    is_move_possible = False
            if is_move_possible:
                moves.append((
                    position[0],
                    position[1][:shape]+(position[1][shape]+1,)+position[1][shape+1:]
                ))
        if position[0][shape]+size[0][shape] != grid_size[0]:    
            is_move_possible = True
            for i in range(size[1][shape]):
                if not is_empty(position, position[0][shape]+size[0][shape], position[1][shape]+i, max_x_size, max_y_size):
                    is_move_possible = False
            if is_move_possible:
                moves.append((
                    position[0][:shape]+(position[0][shape]+1,)+position[0][shape+1:],
                    position[1]
                ))
        if position[1][shape] != 0:
            is_move_possible = True
            for i in range(size[0][shape]):
                if not is_empty(position, position[0][shape]+i, position[1][shape]-1, max_x_size, max_y_size):
                    is_move_possible = False
            if is_move_possible:
                moves.append((
                    position[0],
                    position[1][:shape]+(position[1][shape]-1,)+position[1][shape+1:]
                ))
        if position[0][shape] != 0:
            is_move_possible = True
            for i in range(size[1][shape]):
                if not is_empty(position, position[0][shape]-1, position[1][shape]+i, max_x_size, max_y_size):
                    is_move_possible = False
            if is_move_possible:
                moves.append((
                    position[0][:shape]+(position[0][shape]-1,)+position[0][shape+1:],
                    position[1]
                ))
    return tuple(moves)

# ostaje
def paintBIG(pixels, step=0, num_steps=0, pic_size=50, space_size=5, border=5):
    turtle.reset()
    # col = rainbow_colors(len(pixels[0]))
    col = [(234, 210, 162)]*len(pixels[0])
    col[key_peace] = (255, 0, 0)
    screen = turtle.Screen()
    screen.tracer(0)
    turtle.colormode(255)

    turtle.pu()
    turtle.ht()

    for i in range(len(pixels[0])):
        x = pixels[0][i] * pic_size
        y = pixels[1][i] * pic_size

        fx = size[0][i] * pic_size
        fy = size[1][i] * pic_size

        turtle.goto(x, y)
        turtle.setheading(0)

        turtle.color(*col[i])
        turtle.pd()
        turtle.begin_fill()

        for _ in range(2):
            turtle.fd(fx-space_size)
            turtle.lt(90)
            turtle.fd(fy-space_size)
            turtle.lt(90)

        turtle.end_fill()
        turtle.pu()
    if num_steps != 0:
        turtle.goto(0, -40)
        turtle.write(f"{step+1}/{num_steps}", font=('Arial', 20, 'normal'))
        turtle.st()
        turtle.goto(-pic_size/2, 0)
        turtle.pd()
        turtle.width(5)
        turtle.goto(-pic_size/2, grid_size[1]*pic_size)
        turtle.pu()
        turtle.color("red")
        turtle.shape("circle")
        turtle.goto(-pic_size/2, grid_size[1]*pic_size*(step+1)/num_steps)
    screen.update()
def rainbow_colors(n):
    if n <= 0:
        return []

    colors = []
    for i in range(n):
        h = i / n              # hue ravnomjerno od 0 do 1
        s = 1.0                # puna zasićenost
        v = 1.0                # puna svjetlina
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        colors.append((
            int(r * 255),
            int(g * 255),
            int(b * 255)
        ))

    return colors
def start_paint():
    turtle.bgcolor("black")
    turtle.speed(1)
    turtle.rt(360)

# prebacit
def is_new(layers,k):
    is_new = True
    for l in layers:
        if k in l.keys():
            is_new = False
    return is_new
def is_solution(k, key_peace, key_location):
    return (k[0][key_peace],k[1][key_peace]) == key_location
def find_sequence(solution, layers):
    sequence=[solution]
    for i in range(len(layers)-1):
        level = len(layers)-i-2
        done = False
        for j in layers[level]:
            if sequence[i] in layers[level][j] and done==False:
                sequence.append(j)
                done = True
    return sequence
def paint_list(pic_list):
    start_paint()
    stop = "a"
    while stop == "a":
        for i in range(len(pic_list)):
            paintBIG(pic_list[len(pic_list)-i-1], i, len(pic_list))
            input("next")
        stop = input("stop/again/change level(s,a, c)")
        while not stop in ["a", "s", "c"]:
            print("Wrong input, options(a, s, c)")
            stop = input("stop/again/chose level(s, a, c)")
    return stop
def purge(layers):
    layers2 = []
    for i in list(range(len(layers)-1, -1, -1)):
        a = {}
        for j in layers[i]:
            if len(layers[i][j]) > 0:
                a[j] = layers[i][j]
        layers2.append(a)
    return layers2
def solve_layers(pos, key_peace, key_location):
    max_x_size = max(size[0])
    max_y_size = max(size[1])
    layers=[{pos:all_possible_moves(pos, max_x_size, max_y_size)}] #layers: sve, list
    counter=0
    is_done=False
    layer = 0
    while is_done==False: #i: sloj, dict
        layer+=1
        # print("try append")
        layers.append({}) # dodaje idući sloj
        # print("all good")
        
        for j in layers[counter].values(): #j: toupl veza
            for k in j:
                if is_new(layers, k): 
                    layers[counter+1].update({k:all_possible_moves(k, max_x_size, max_y_size)})
                    if is_solution(k, key_peace, key_location):
                        is_done=True
                        solution = k
                        break
        # for i in layers:
        #     print(len(i), end=", ")
        # if layer%3==0:
        #     layers = purge(layers)
        #     print(sys.getsizeof(layers), layer)
        #     li = []
        #     for i in layers:
        #         li.append(sys.getsizeof(i))
        #     print(li, layer)
        counter+=1

    sequence=find_sequence(solution, layers)
    return sequence
def choose_level():
    global size, position
    level = input("What level(1-4)")
    good = False
    while good==False:
        if level=='1':
            size =     ((1,1,1,1,2,1,2,1,1,1), (2,2,2,2,1,1,2,1,1,1)) # lv 10
            position = ((1,2,0,3,1,0,1,3,0,3), (0,0,1,1,2,3,3,3,4,4))
            good = True
        elif level=='2':
            size =     ((1,1,2,1,1,2,2,1,1,1,2,1), (1,1,1,1,1,1,1,1,1,1,2,1)) # lv 14
            position = ((0,1,2,0,1,2,0,2,3,0,1,3), (0,0,0,1,1,1,2,2,2,3,3,3))
            good = True
        elif level=='3':
            size =     ((2,1,1,1,1,1,1,2,1,1), (1,2,1,2,2,1,2,2,1,1)) # lv 15
            position = ((2,0,1,2,3,1,0,1,3,3), (0,1,1,1,1,2,3,3,3,4))
            good = True
        elif level=='4':
            size =     ((1,1,1,1,1,1,2,1,2,1), (2,1,1,2,1,1,1,2,2,2)) # og lv 30
            position = ((0,1,2,3,1,2,1,0,1,3), (0,0,0,0,1,1,2,3,3,3))
            good = True
        else:
            print("Wrong input, options(1, 2, 3, 4)")

key_peace = 3 # og je  8
stop = "c"
while stop == "c":
    choose_level()
    stop = paint_list(solve_layers(position, key_peace, (0,0)))

