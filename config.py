class Config:
    cal_range = 75
    x_min = 0
    x_max = cal_range - 1
    y_min = 0
    y_max = cal_range - 1
    show_range = 25
    show_range_0 = 25
    show_index = (cal_range - show_range) // 2


Coordinate_Nearest_X = [-1, 0, 1, -1, 1, -1, 0, 1]
Coordinate_Nearest_Y = [-1, -1, -1, 0, 0, 1, 1, 1]


class PyGameConfig:
    first_play_y = 350
    first_exit_y = 500

    column_1 = 1000
    column_2 = 1300
    row_1 = 100 + 65
    row_2 = 250 + 65
    row_3 = 400 + 65
    row_4 = 550 + 65
    row_5 = 700 + 65

    start_x = column_1
    start_y = row_1
    zoom_x = column_2
    zoom_y = row_1

    set_x = column_1
    set_y = row_2
    clear_x = column_2
    clear_y = row_2

    undo_x = column_1
    undo_y = row_3
    redo_x = column_2
    redo_y = row_3

    # save_x = column_1
    # save_y = row_4
    # load_x = column_1
    # load_y = row_4


    exit_x = column_2
    exit_y = row_4
    home_x = column_1
    home_y = row_4

    white = (255, 255, 255)
    grey = (127, 127, 127)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)

