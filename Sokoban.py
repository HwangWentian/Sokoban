from pynput import keyboard as kb
from os import system
from time import sleep
from re import split


def read_map(level:int) -> tuple:
    try:
        with open("map%d.map"%level, 'r') as file:
            text = split("\n", file.read(), 1)
    except:
        exit()
    inf = split(":", text[0])
    goals_ = split("~", inf[0])
    goals = []
    for g in goals_:
        g_ = split(",", g)
        goals.append([int(g_[0]), int(g_[1])])
    width = int(inf[1])
    map = text[1]
    return goals, width, map


def rp(text:str, index:int, char:str) -> str:
    lst = list(text)
    lst[index] = char
    return "".join(lst)


def move(map:str, dir:str, wid:int) -> str:
    my_posi = map.find("I") % wid, map.find("I") // wid
    #坐标从左上(0,0)开始，向右，向下分别递增

    if dir == "u": posi = map[my_posi[0] + wid * (my_posi[1] - 1)]
    elif dir == "d": posi = map[my_posi[0] + wid * (my_posi[1] + 1)]
    elif dir == "l": posi = map[my_posi[0] - 1 + wid * my_posi[1]]
    else: posi = map[my_posi[0] + 1 + wid * my_posi[1]]
    print("#",posi)

    if posi == "#":
        pass
    elif posi == "B": #检测箱子是否被推到墙上
        if dir == "u" and map[my_posi[0] + wid * (my_posi[1] - 2)] != "#" and map[my_posi[0] + wid * (my_posi[1] - 2)] != "B":
            map = rp(map, my_posi[0] + wid * (my_posi[1] - 2), "B")
            map = rp(map, my_posi[0] + wid * (my_posi[1] - 1), "I")
        elif dir == "d" and map[my_posi[0] + wid * (my_posi[1] + 2)] != "#" and map[my_posi[0] + wid * (my_posi[1] + 2)] != "B":
            map = rp(map, my_posi[0] + wid * (my_posi[1] + 2), "B")
            map = rp(map, my_posi[0] + wid * (my_posi[1] + 1), "I")
        elif dir == "l" and map[my_posi[0] - 2 + wid * my_posi[1]] != "#" and map[my_posi[0] - 2 + wid * my_posi[1]] != "B":
            map = rp(map, my_posi[0] - 2 + wid * my_posi[1], "B")
            map = rp(map, my_posi[0] - 1 + wid * my_posi[1], "I")
        elif dir == "r" and map[my_posi[0] + 2 + wid * my_posi[1]] != "#" and map[my_posi[0] + 2 + wid * my_posi[1]] != "B":
            map = rp(map, my_posi[0] + 2 + wid * my_posi[1], "B")
            map = rp(map, my_posi[0] + 1 + wid * my_posi[1], "I")
        else:
            return map
        map = rp(map, my_posi[0] + wid * my_posi[1], " ")
    else:
        if dir == "u":
            map = rp(map, my_posi[0] + wid * (my_posi[1] - 1), "I")
        elif dir == "d":
            map = rp(map, my_posi[0] + wid * (my_posi[1] + 1), "I")
        elif dir == "l":
            map = rp(map, my_posi[0] - 1 + wid * my_posi[1], "I")
        else:
            map = rp(map, my_posi[0] + 1 + wid * my_posi[1], "I")
        map = rp(map, my_posi[0] + wid * my_posi[1], " ")
    print(map)
    return map


def draw(map:str, goals:list, width:int) -> None:
    print("\033[2J\033[0;0H")
    for goal in goals:
        char = map[goal[0] + width * goal[1]]
        if char != "B" and char != "I":
            map = rp(map, goal[0] + width * goal[1], "@")
    print(map)


def on_press(key):
    global map_, goals, width
    if key == kb.Key.esc:
        exit()
    elif key == kb.Key.up:
        map_ = move(map_,"u", width)    
    elif key == kb.Key.down:
        map_ = move(map_,"d", width)
    elif key == kb.Key.left:
        map_ = move(map_,"l", width)
    elif key == kb.Key.right:
        map_ = move(map_,"r", width)
    draw(map_, goals, width)
    if if_win(map_, goals, width):
        raise SystemError


def if_win(map:str, goals:list, width:int) -> bool:
    for goal in goals:
        char = map[goal[0] + width * goal[1]]
        if char != "B":
            return False
    return True


if __name__ == "__main__":
    level = 0
    while True:
        level += 1
        goals, width, map_ = read_map(level)

        print("\033?25l")
        draw(map_, goals, width)
        try:
            with kb.Listener(on_press=on_press) as listener:
                listener.join()
        except SystemError:
            system("clear")
