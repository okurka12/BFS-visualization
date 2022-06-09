import PySimpleGUI as sg
from config import board_size
from random import randint

def_button_color = "#333333"
clicked_button_color = "#ffff00"
unclickable_button_color = "#800000"
unclickable_button_color_2 = "#805300"


def generate_list(values: dict):  # ze slovniku {(x, y): True/False} to udela 2d list, neni to potreba,
    # ale puvodne jsem ty obstacly vystupoval jako list, a tak aby to fungovalo tak jsem to takhle udelal

    output = []
    for i in range(board_size):
        row = []
        for j in range(board_size):
            row.append(values[j, i])
        output.append(row)
    return output


def generate_random():
    start_pos = (randint(0, board_size-1), randint(0, board_size-1))

    done = False
    while not done:
        end_pos = (randint(0, board_size-1), randint(0, board_size-1))
        if end_pos != start_pos:
            done = True

    obstacledict = {}
    print((round((board_size**2)/4)), round((board_size**2)/6))
    obstaclecount = randint((round(board_size**2/6)), round(board_size**2/3))
    obstacles = []

    for i in range(obstaclecount):  # vygeneruje list prekazek
        done = False
        while not done:
            obstacle = (randint(0, board_size-1), randint(0, board_size-1))
            if obstacle not in obstacles and obstacle != start_pos and obstacle != end_pos:
                obstacles.append(obstacle)
                done = True

    for i in range(board_size):  # vygeneruje dict prekazek kde vsechny false
        for j in range(board_size):
            obstacledict[j, i] = False

    for obstaclepos in obstacles:  # v dictu prekaze to da true pro kazdou prekazku v listu prekazek
        obstacledict[obstaclepos] = True

    return start_pos, end_pos, obstacledict


def obstacle_gui(generate_random_obstacles=False):
    start_pos = (0, 0)  # deklarace defaultniho startu
    end_pos = (board_size - 1, board_size - 1)  # deklarace defaultniho konce
    obstacles_output = {}

    if not generate_random_obstacles:
        for i in range(board_size):  # vygeneruje to klice ve slovniku obstacles_output,
            # aby jich bylo tolik, kolik je prekazek
            for j in range(board_size):
                obstacles_output[j, i] = False

    if generate_random_obstacles:
        start_pos, end_pos, obstacles_output = generate_random()

    sg.theme("BluePurple")
    layout = [  # layout je 2d pole prvku (tlacitka, texty atd.) v okne
        [sg.Text("Výběr začátku", key="-STATE-")]
    ]
    for i in range(board_size):  # prida pro kazde policko tlacitko
        tmp = []
        for j in range(board_size):
            if (j, i) == start_pos:
                tmp.append(sg.Button("x", key=f"-TLACITKOXX{j}XX{i}XX-", button_color=clicked_button_color))
            elif (j, i) == end_pos:  # startovni stav programu je 0 takze vyber zacatku takze proto
                # tenhle elif, ktery prida disabled tlacitko
                # (prvky jdou updatovat teprve az probehne prvni window.read()), proto je potreba to udelat uz ted
                tmp.append(sg.Button("x", key=f"-TLACITKOXX{j}XX{i}XX-", button_color=unclickable_button_color_2,
                                     disabled=True))
            elif obstacles_output[j, i]:  # to stejny jako ten elif predtim ale s prekazkami
                tmp.append(sg.Button("x", key=f"-TLACITKOXX{j}XX{i}XX-", button_color=unclickable_button_color,
                                     disabled=True))
            else:
                tmp.append(sg.Button("x", key=f"-TLACITKOXX{j}XX{i}XX-", button_color=def_button_color))
        layout.append(tmp)
    layout.append([sg.Button("Výběr začátku", key="-STARTSELECT-")])
    layout.append([sg.Button("Výběr konce", key="-ENDSELECT-")])
    layout.append([sg.Button("Výběr překážek", key="-OBSTSELECT-")])
    if generate_random_obstacles:
        layout.append([sg.Button("Přegenerovat", key="-RE-GENERATE-")])
    layout.append([sg.Button("Vyhledat cestu", key="-END-")])
    window = sg.Window("Program", layout)

    def color_button(_pos, color):
        window[f"-TLACITKOXX{_pos[0]}XX{_pos[1]}XX-"].update(button_color=color)

    def disable_button(_pos):
        window[f"-TLACITKOXX{_pos[0]}XX{_pos[1]}XX-"].update(disabled=True)

    def enable_button(_pos):
        window[f"-TLACITKOXX{_pos[0]}XX{_pos[1]}XX-"].update(disabled=False)

    def clear_all_buttons():
        for i in range(board_size):
            for j in range(board_size):
                color_button((j, i), def_button_color)
                enable_button((j, i))

    def color_obstacles():
        clear_all_buttons()
        for obstaclepos in obstacles_output:
            if obstacles_output[obstaclepos]:
                color_button(obstaclepos, clicked_button_color)
        color_button(start_pos, unclickable_button_color_2)
        color_button(end_pos, unclickable_button_color_2)
        disable_button(start_pos)
        disable_button(end_pos)

    def color_start():
        clear_all_buttons()
        for obstaclepos in obstacles_output:
            if obstacles_output[obstaclepos]:
                color_button(obstaclepos, unclickable_button_color)
                disable_button(obstaclepos)
        color_button(end_pos, unclickable_button_color_2)
        disable_button(end_pos)
        color_button(start_pos, clicked_button_color)

    def color_end():
        clear_all_buttons()
        for obstaclepos in obstacles_output:
            if obstacles_output[obstaclepos]:
                color_button(obstaclepos, unclickable_button_color)
                disable_button(obstaclepos)
        color_button(start_pos, unclickable_button_color_2)
        disable_button(start_pos)
        color_button(end_pos, clicked_button_color)

    state = 0  # 0 - start, 1 - end, 2 - obstacles
    while True:
        event, values = window.read()
        if event == "-END-" or event == sg.WIN_CLOSED:
            break

        if event == "-STARTSELECT-":
            window["-STATE-"].update("Výběr začátku")
            color_start()
            state = 0
            continue

        if event == "-ENDSELECT-":
            window["-STATE-"].update("Výběr konce")
            color_end()
            state = 1
            continue

        if event == "-OBSTSELECT-":
            color_obstacles()
            window["-STATE-"].update("Výběr překážek")
            state = 2
            continue

        if event == "-RE-GENERATE-":
            start_pos, end_pos, obstacles_output = generate_random()
            if state == 0:
                color_start()
            if state == 1:
                color_end()
            if state == 2:
                color_obstacles()
            continue

        if isinstance(event, str):
            if event.startswith("-TLACITKO"):
                if state == 0:
                    color_button(start_pos, def_button_color)
                    start_pos = (int(event.split("XX")[1]), int(event.split("XX")[2]))
                    color_button(start_pos, clicked_button_color)
                if state == 1:
                    color_button(end_pos, def_button_color)
                    end_pos = (int(event.split("XX")[1]), int(event.split("XX")[2]))
                    color_button(end_pos, clicked_button_color)
                if state == 2:
                    pos = int(event.split("XX")[1]), int(event.split("XX")[2])
                    if not obstacles_output[pos]:
                        obstacles_output[pos] = True
                        color_button(pos, clicked_button_color)
                    else:
                        obstacles_output[pos] = False
                        color_button(pos, def_button_color)

    window.close()

    return generate_list(obstacles_output), start_pos, end_pos



