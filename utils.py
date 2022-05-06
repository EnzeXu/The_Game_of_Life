import os.path

import pygame
import copy
import time
import pickle
import numpy as np
import matplotlib.pyplot as plt
from config import Config, Coordinate_Nearest_X, Coordinate_Nearest_Y, PyGameConfig
from tkinter import filedialog, Tk
from button import Button
from input_box import InputBox
from surface import Surface

# from tkinter import *
from tkinter.filedialog import askopenfilename


def update_grid(config, tmp_map, x, y):
    # print([(x + xx, y + yy, tmp_map[x + xx][y + yy]) for xx, yy in zip(Coordinate_Nearest_X, Coordinate_Nearest_Y)
    #              if 0 <= x + xx < config.cal_range and 0 <= y + yy < config.cal_range])
    count = sum([tmp_map[x + xx][y + yy] for xx, yy in zip(Coordinate_Nearest_X, Coordinate_Nearest_Y)
                 if 0 <= x + xx < config.cal_range and 0 <= y + yy < config.cal_range])
    # print("({}, {}): count = {}".format(x, y, int(count)))
    if count < 2 or count > 3:
        return 0
    if count == 2:
        return tmp_map[x][y]
    if count == 3:
        return 1


def get_existence_range(tmp_map):
    length = tmp_map.shape[0]
    x_min, x_max, y_min, y_max = -1, -1, -1, -1
    for i in range(0, length, 1):
        if np.sum(tmp_map[i, :]) > 0:
            x_min = i
            break
    for i in range(length - 1, -1, -1):
        if np.sum(tmp_map[i, :]) > 0:
            x_max = i
            break
    for i in range(0, length, 1):
        if np.sum(tmp_map[:, i]) > 0:
            y_min = i
            break
    for i in range(length - 1, -1, -1):
        if np.sum(tmp_map[:, i]) > 0:
            y_max = i
            break
    return x_min, x_max, y_min, y_max


def print_map(config, tmp_map):
    print("({0:d} grids live)".format(int(np.sum(tmp_map))))
    for i in range(config.show_index, config.show_index + config.show_range):
        for j in range(config.show_index, config.show_index + config.show_range):
            print(int(tmp_map[i][j]), end=" ")
        print()


def next_map(config, tmp_map):
    x_min, x_max, y_min, y_max = get_existence_range(tmp_map)
    # print("x in [{},{}], y in [{},{}]".format(x_min, x_max, y_min, y_max))
    x_min = max(x_min - 1, config.x_min)
    x_max = min(x_max + 1, config.x_max)
    y_min = max(y_min - 1, config.y_min)
    y_max = min(y_max + 1, config.y_max)
    # print("check: x in [{},{}], y in [{},{}]".format(x_min, x_max, y_min, y_max))
    new_map = copy.deepcopy(tmp_map)
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            new_map[i][j] = update_grid(config, tmp_map, i, j)
            # print(i, j, int(new_map[i][j]))
    return new_map


def auto_print():
    center = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])
    config = Config
    center_length = len(center)
    start_index = (config.cal_range - center_length) // 2
    end_index = (config.cal_range + center_length) // 2
    init_map = np.zeros([config.cal_range, config.cal_range])
    init_map[start_index: end_index, start_index: end_index] = center
    m = init_map
    for i in range(100):
        print_map(config, m)
        m = next_map(config, m)


def game_auto_print(screen):
    center = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])
    config = Config
    center_length = len(center)
    start_index = (config.cal_range - center_length) // 2
    end_index = (config.cal_range + center_length) // 2
    init_map = np.zeros([config.cal_range, config.cal_range])
    init_map[start_index: end_index, start_index: end_index] = center
    m = init_map
    for i in range(10):
        # print_map(config, m)
        save_figure(config, m, False, True, "./image/tmp.png")
        grids = pygame.image.load("./image/tmp.png")
        screen.blit(grids, (50, 50))
        pygame.display.update()
        m = next_map(config, m)


def save_figure(config, tmp_map, show_flag=False, save_flag=True, save_path=None):
    plt.figure(figsize=[8, 8])
    show_map = tmp_map[config.show_index: config.show_index + config.show_range, config.show_index: config.show_index + config.show_range]
    plt.imshow(show_map, interpolation='nearest', cmap=plt.cm.binary, vmin=0, vmax=1)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax = plt.gca()

    # Major ticks
    ax.set_xticks(np.arange(0, config.show_range, 1))
    ax.set_yticks(np.arange(0, config.show_range, 1))

    # # Labels for major ticks
    # ax.set_xticklabels(np.arange(1, config.show_range + 1, 1))
    # ax.set_yticklabels(np.arange(1, config.show_range + 1, 1))

    # Minor ticks
    ax.set_xticks(np.arange(-.5, config.show_range, 1), minor=True)
    ax.set_yticks(np.arange(-.5, config.show_range, 1), minor=True)

    # Gridlines based on minor ticks
    # ax.grid(which='major', color='w', linestyle='-', linewidth=3)
    ax.grid(which="minor", color='grey', linestyle='-', linewidth=1)

    if save_flag:
        plt.savefig(save_path, dpi=100)
    if show_flag:
        plt.show()
    plt.clf()
    plt.close()


def save_gol(tmp_map, save_path):
    with open(save_path, "wb") as f:
        pickle.dump(tmp_map, f)


def load_gol(save_path):
    with open(save_path, "rb") as f:
        tmp_map = pickle.load(f)
    return tmp_map


# def choose_load_path():
#     # root = Tk()
#     # root.title('Intro')
#     filetypes = [("GameOfLife File", "*.gol")]
#     path = filedialog.askopenfilename(initialdir="./saves/", filetypes=filetypes, title="Please select a folder:")
#     # root.mainloop()
#     return path


def run():
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption("The Game of Life")
    icon = pygame.image.load("image/leaf.ico")
    pygame.display.set_icon(icon)
    config = Config
    bg = pygame.image.load("./image/background4.png")
    # font_addr = pygame.font.get_default_font()
    font = pygame.font.Font("font/DancingScript-Regular.otf", 120)

    screen.blit(bg, (0, 0))

    game_title = font.render("The Game of Life", True, (255, 255, 255))
    screen.blit(game_title, (1600 // 2 - game_title.get_width() // 2, 150))

    by_enze = pygame.font.Font("font/times.ttf", 50).render("Designed by Enze @ CSC 721", True, (255, 255, 255))
    screen.blit(by_enze, (1600 // 2 - by_enze.get_width() // 2, 680))

    # csc = pygame.font.Font("font/times.ttf", 30).render("@ CSC 721", True, (0, 0, 0))
    # screen.blit(csc, (1600 // 2 - csc.get_width() // 2, 740))

    # https://github.com/EnzeXu/The_Game_of_Life
    github_link = pygame.font.Font("font/times.ttf", 30).render("https://github.com/EnzeXu/The_Game_of_Life", True, (0, 0, 0))
    screen.blit(github_link, (1600 // 2 - github_link.get_width() // 2, 770))

    play_button = Button('Play', PyGameConfig.blue, None, PyGameConfig.first_play_y, centered_x=True)
    exit_button = Button('Exit', PyGameConfig.blue, None, PyGameConfig.first_exit_y, centered_x=True)

    play_button.display(screen)
    exit_button.display(screen)

    pygame.display.update()

    while True:
        if play_button.check_click(pygame.mouse.get_pos()):
            play_button = Button('Play', PyGameConfig.red, None, PyGameConfig.first_play_y, centered_x=True)
        else:
            play_button = Button('Play', PyGameConfig.blue, None, PyGameConfig.first_play_y, centered_x=True)

        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button('Exit', PyGameConfig.red, None, PyGameConfig.first_exit_y, centered_x=True)
        else:
            exit_button = Button('Exit', PyGameConfig.blue, None, PyGameConfig.first_exit_y, centered_x=True)

        play_button.display(screen)
        exit_button.display(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if pygame.mouse.get_pressed()[0]:
            if play_button.check_click(pygame.mouse.get_pos()):
                break
            if exit_button.check_click(pygame.mouse.get_pos()):
                pygame.quit()
                exit()

    # bg = pygame.image.load("image/background2.png")
    screen.blit(bg, (0, 0))
    progress_surf = Surface(47, 47, 806, 806, pygame.Color(255, 0, 0, 255))
    button_surf = Surface(950, 47, 580, 806, pygame.Color(227, 191, 191, 127))
    # progress_surf = pygame.Surface((806, 806), pygame.SRCALPHA)
    # progress_surf.fill(pygame.Color(255, 0, 0, 255))
    # screen.blit(progress_surf, (47, 47))
    progress_surf.draw(screen)
    button_surf.draw(screen)
    pygame.display.update()
    # game_auto_print(screen)

    clock = pygame.time.Clock()

    start_button = Button("Run", PyGameConfig.white, PyGameConfig.start_x, PyGameConfig.start_y)
    zoom_button = Button("Zoom", PyGameConfig.white, PyGameConfig.zoom_x, PyGameConfig.zoom_y)
    set_button = Button("Set", PyGameConfig.blue, PyGameConfig.set_x, PyGameConfig.set_y)
    undo_button = Button("Undo", PyGameConfig.white, PyGameConfig.undo_x, PyGameConfig.undo_y)
    redo_button = Button("Redo", PyGameConfig.white, PyGameConfig.redo_x, PyGameConfig.redo_y)
    clear_button = Button("Clear", PyGameConfig.white, PyGameConfig.clear_x, PyGameConfig.clear_y)
    # save_button = Button("Save", PyGameConfig.white, PyGameConfig.save_x, PyGameConfig.save_y)
    # load_button = Button("Load", PyGameConfig.blue, PyGameConfig.load_x, PyGameConfig.load_y)
    exit_button = Button("Exit", PyGameConfig.blue, PyGameConfig.exit_x, PyGameConfig.exit_y)
    home_button = Button("Home", PyGameConfig.blue, PyGameConfig.home_x, PyGameConfig.home_y)

    start_button.display(screen)
    zoom_button.display(screen)
    set_button.display(screen)
    undo_button.display(screen)
    redo_button.display(screen)
    clear_button.display(screen)
    # save_button.display(screen)
    # load_button.display(screen)
    exit_button.display(screen)
    home_button.display(screen)

    input_box = InputBox(pygame.Rect(1150, 190, 200, 80))
    input_box.draw(screen)

    gol = pygame.image.load("./image/gol.png")
    screen.blit(gol, (50, 50))
    tmp_timestamp = time.time()
    tmp_pos = (-1, -1)
    pygame.display.update()

    set_available = True
    start_available = False
    zoom_available = False
    undo_available = False
    redo_available = False
    clear_available = False
    # save_available = False
    # load_available = True
    mmap = np.zeros([config.cal_range, config.cal_range])
    emp = copy.deepcopy(mmap)
    save_figure(config, mmap, False, True, "./image/tmp.png")
    tmp = pygame.image.load("./image/tmp.png")
    archive = [copy.deepcopy(mmap)]
    archive_index = 0
    archive_index_max = 0
    start_epoch = 10
    running_flag = False
    welcome_flag = True
    event_run_flag = False
    # load_flag = True
    config.show_range = config.show_range_0
    config.show_index = (config.cal_range - config.show_range) // 2
    time.sleep(0.2)

    while True:
        clock.tick(60)
        screen.blit(bg, (0, 0))
        progress_surf.draw(screen)
        button_surf.draw(screen)
        if welcome_flag:
            screen.blit(gol, (50, 50))
        else:
            # save_figure(config, mmap, False, True, "./image/tmp.png")
            # tmp = pygame.image.load("./image/tmp.png")
            screen.blit(tmp, (50, 50))
        # print("archive_index, archive_index_max = {}, {}".format(archive_index, archive_index_max))
        try:
            start_epoch = int(input_box.text)
        except:
            start_epoch = 10
        if not running_flag and not welcome_flag and archive_index > 0:
            undo_available = True
        else:
            undo_available = False
        if not (archive[archive_index] == mmap).all():
            undo_available = True
        if not running_flag and not welcome_flag and archive_index < archive_index_max:
            redo_available = True
        else:
            redo_available = False
        # update buttons
        if not running_flag and start_available:
            if start_button.check_click(pygame.mouse.get_pos()):
                start_button = Button("Run", PyGameConfig.red, PyGameConfig.start_x, PyGameConfig.start_y)
            else:
                start_button = Button("Run", PyGameConfig.blue, PyGameConfig.start_x, PyGameConfig.start_y)
        else:
            start_button = Button("Run", PyGameConfig.white, PyGameConfig.start_x, PyGameConfig.start_y)

        if not running_flag and zoom_available:
            if zoom_button.check_click(pygame.mouse.get_pos()):
                zoom_button = Button("Zoom", PyGameConfig.red, PyGameConfig.zoom_x, PyGameConfig.zoom_y)
            else:
                zoom_button = Button("Zoom", PyGameConfig.blue, PyGameConfig.zoom_x, PyGameConfig.zoom_y)
        else:
            zoom_button = Button("Zoom", PyGameConfig.white, PyGameConfig.zoom_x, PyGameConfig.zoom_y)

        if not running_flag and set_available:
            if set_button.check_click(pygame.mouse.get_pos()):
                set_button = Button("Set", PyGameConfig.red, PyGameConfig.set_x, PyGameConfig.set_y)
            else:
                set_button = Button("Set", PyGameConfig.blue, PyGameConfig.set_x, PyGameConfig.set_y)
        else:
            set_button = Button("Set", PyGameConfig.white, PyGameConfig.set_x, PyGameConfig.set_y)

        if not running_flag and undo_available:
            if undo_button.check_click(pygame.mouse.get_pos()):
                undo_button = Button("Undo", PyGameConfig.red, PyGameConfig.undo_x, PyGameConfig.undo_y)
            else:
                undo_button = Button("Undo", PyGameConfig.blue, PyGameConfig.undo_x, PyGameConfig.undo_y)
        else:
            undo_button = Button("Undo", PyGameConfig.white, PyGameConfig.undo_x, PyGameConfig.undo_y)

        if not running_flag and redo_available:
            if redo_button.check_click(pygame.mouse.get_pos()):
                redo_button = Button("Redo", PyGameConfig.red, PyGameConfig.redo_x, PyGameConfig.redo_y)
            else:
                redo_button = Button("Redo", PyGameConfig.blue, PyGameConfig.redo_x, PyGameConfig.redo_y)
        else:
            redo_button = Button("Redo", PyGameConfig.white, PyGameConfig.redo_x, PyGameConfig.redo_y)

        if not running_flag and clear_available:
            if clear_button.check_click(pygame.mouse.get_pos()):
                clear_button = Button("Clear", PyGameConfig.red, PyGameConfig.clear_x, PyGameConfig.clear_y)
            else:
                clear_button = Button("Clear", PyGameConfig.blue, PyGameConfig.clear_x, PyGameConfig.clear_y)
        else:
            clear_button = Button("Clear", PyGameConfig.white, PyGameConfig.clear_x, PyGameConfig.clear_y)

        # if not running_flag and save_available:
        #     if save_button.check_click(pygame.mouse.get_pos()):
        #         save_button = Button("Save", PyGameConfig.red, PyGameConfig.save_x, PyGameConfig.save_y)
        #     else:
        #         save_button = Button("Save", PyGameConfig.blue, PyGameConfig.save_x, PyGameConfig.save_y)
        # else:
        #     save_button = Button("Save", PyGameConfig.white, PyGameConfig.save_x, PyGameConfig.save_y)

        # if not running_flag and load_available:
        #     if load_button.check_click(pygame.mouse.get_pos()):
        #         load_button = Button("Load", PyGameConfig.red, PyGameConfig.load_x, PyGameConfig.load_y)
        #     else:
        #         load_button = Button("Load", PyGameConfig.blue, PyGameConfig.load_x, PyGameConfig.load_y)
        # else:
        #     load_button = Button("Load", PyGameConfig.white, PyGameConfig.load_x, PyGameConfig.load_y)
        #

        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button("Exit", PyGameConfig.red, PyGameConfig.exit_x, PyGameConfig.exit_y)
        else:
            exit_button = Button("Exit", PyGameConfig.blue, PyGameConfig.exit_x, PyGameConfig.exit_y)

        if home_button.check_click(pygame.mouse.get_pos()):
            home_button = Button("Home", PyGameConfig.red, PyGameConfig.home_x, PyGameConfig.home_y)
        else:
            home_button = Button("Home", PyGameConfig.blue, PyGameConfig.home_x, PyGameConfig.home_y)

        start_button.display(screen)
        zoom_button.display(screen)
        set_button.display(screen)
        undo_button.display(screen)
        redo_button.display(screen)
        clear_button.display(screen)
        # save_button.display(screen)
        # load_button.display(screen)
        exit_button.display(screen)
        home_button.display(screen)
        input_box.draw(screen)

        pygame.display.update()
        pygame.display.flip()
        # listening
        if event_run_flag:
            start_archive = copy.deepcopy(mmap)
            for i in range(start_epoch):
                progress_surf.draw(screen)
                progress_surf_finished = Surface(progress_surf.x, progress_surf.y, int(progress_surf.width * (i + 1) / start_epoch), progress_surf.length, pygame.Color(0, 255, 0, 255))
                progress_surf_finished.draw(screen)
                mmap = next_map(config, mmap)
                save_figure(config, mmap, False, True, "./image/tmp.png")
                tmp = pygame.image.load("./image/tmp.png")
                screen.blit(tmp, (50, 50))
                pygame.display.update()
            undo_available = True
            redo_available = True
            clear_available = True
            # save_available = True
            set_available = True
            start_available = True
            # load_available = True

            running_flag = False
            event_run_flag = False
            if not (archive[archive_index] == mmap).all():
                archive.append(copy.deepcopy(mmap))
                archive_index += 1
                archive_index_max += 1
            time.sleep(0.2)
            continue

        for event in pygame.event.get():
            input_box.dealEvent(event, screen)
            if event.type == pygame.QUIT:
                # print("Thank you! Bye~")
                pygame.quit()
                exit()
        if pygame.mouse.get_pressed()[0]:
            # print(pygame.mouse.get_pos())
            new_timestamp = time.time()
            new_pos = pygame.mouse.get_pos()
            if not running_flag and not set_available:
                if 50 <= new_pos[0] < 850 and 50 <= new_pos[0] < 850:
                    if new_pos != tmp_pos or new_timestamp - tmp_timestamp > 0.1:
                        x_offset = int((new_pos[1] - 50) // (800 / config.show_range))
                        y_offset = int((new_pos[0] - 50) // (800 / config.show_range))
                        # print("new click:", new_pos, x_offset, y_offset)
                        mmap[config.show_index + x_offset][config.show_index + y_offset] = 1 - mmap[config.show_index + x_offset][config.show_index + y_offset]
                        save_figure(config, mmap, False, True, "./image/tmp.png")
                        tmp = pygame.image.load("./image/tmp.png")
                        screen.blit(tmp, (50, 50))
                        pygame.display.update()
            tmp_timestamp = new_timestamp
            tmp_pos = new_pos
            if not running_flag and set_available and set_button.check_click(pygame.mouse.get_pos()):
                welcome_flag = False
                set_available = False
                start_available = True
                zoom_available = True
                # save_available = True
                clear_available = True
                # emp = pygame.image.load("./image/empty.png")
                # mmap = np.zeros([config.cal_range, config.cal_range])
                # screen.blit(emp, (50, 50))
                save_figure(config, mmap, False, True, "./image/tmp.png")
                tmp = pygame.image.load("./image/tmp.png")
                screen.blit(tmp, (50, 50))
                archive = archive[: archive_index + 1]
                archive[archive_index] = copy.deepcopy(mmap)
                archive_index_max = archive_index
                pygame.display.update()
            if not running_flag and start_available and start_button.check_click(pygame.mouse.get_pos()):
                # print("starting... epoch = {}".format(start_epoch))
                running_flag = True
                start_available = False
                set_available = False
                # save_available = False
                # load_available = False
                clear_available = False
                undo_available = False
                redo_available = False
                event_run_flag = True
                if not (archive[archive_index] == mmap).all():
                    archive.append(copy.deepcopy(mmap))
                    archive_index += 1
                    archive_index_max += 1
            if not running_flag and clear_available and clear_button.check_click(pygame.mouse.get_pos()):
                # print("clear!")
                mmap = np.zeros([config.cal_range, config.cal_range])
                save_figure(config, mmap, False, True, "./image/tmp.png")
                if not (archive[archive_index] == mmap).all():
                    archive.append(copy.deepcopy(mmap))
                    archive_index += 1
                    archive_index_max += 1
                tmp = pygame.image.load("./image/tmp.png")
                screen.blit(tmp, (50, 50))
                pygame.display.update()
            if not running_flag and zoom_available and zoom_button.check_click(pygame.mouse.get_pos()):
                if config.show_range == config.show_range_0:
                    config.show_range = config.cal_range
                else:
                    config.show_range = config.show_range_0
                config.show_index = (config.cal_range - config.show_range) // 2
                save_figure(config, mmap, False, True, "./image/tmp.png")
                tmp = pygame.image.load("./image/tmp.png")
                screen.blit(tmp, (50, 50))
                pygame.display.update()
            if not running_flag and undo_available and undo_button.check_click(pygame.mouse.get_pos()):
                if not (archive[archive_index] == mmap).all():
                    archive.append(copy.deepcopy(mmap))
                    archive_index += 1
                    archive_index_max += 1

                archive_index -= 1
                mmap = archive[archive_index]
                save_figure(config, mmap, False, True, "./image/tmp.png")
                tmp = pygame.image.load("./image/tmp.png")
                screen.blit(tmp, (50, 50))
                pygame.display.update()
            if not running_flag and redo_available and redo_button.check_click(pygame.mouse.get_pos()):
                archive_index += 1
                mmap = archive[archive_index]
                save_figure(config, mmap, False, True, "./image/tmp.png")
                tmp = pygame.image.load("./image/tmp.png")
                screen.blit(tmp, (50, 50))
                pygame.display.update()
            # if not running_flag and load_flag and load_available and load_button.check_click(pygame.mouse.get_pos()):
            #     print("sad!")
            #     load_flag = False
            #     path = choose_load_path()
            #     if path == "" or not os.path.exists(path):
            #         continue
            #     mmap = load_gol(path)
            #     if not (archive[archive_index] == mmap).all():
            #         archive.append(copy.deepcopy(mmap))
            #         archive_index += 1
            #         archive_index_max += 1
            #     save_figure(config, mmap, False, True, "./image/tmp.png")
            #     tmp = pygame.image.load("./image/tmp.png")
            #     screen.blit(tmp, (50, 50))
            #     pygame.display.update()


            if exit_button.check_click(pygame.mouse.get_pos()):
                pygame.quit()
                exit()
            if home_button.check_click(pygame.mouse.get_pos()):
                pygame.quit()
                run()


if __name__ == "__main__":
    # run()
    # print(filename)

    center = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    # center = np.asarray([
    #     [0, 0, 0, 0, 0, 0],
    #     [0, 0, 1, 0, 0, 0],
    #     [0, 1, 0, 1, 0, 0],
    #     [0, 0, 1, 1, 0, 0],
    #     [0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0]
    # ])
    config = Config
    center_length = len(center)

    start_index = (config.cal_range - center_length) // 2
    end_index = (config.cal_range + center_length) // 2
    init_map = np.zeros([config.cal_range, config.cal_range])
    init_map[start_index: end_index, start_index: end_index] = center
    save_figure(config, init_map, True, True, "./image/gol.png")
    # save_gol(init_map, "saves/boat.gol")
    print_map(config, init_map)
    pass
