import numpy as np

def coordinate_transfer(x, y, max_dis, grid_side_length):

    if x >= 0:
        x = x if x <= max_dis else max_dis
    else:
        x = x if x >= -max_dis else -max_dis

    if y >= 0:
        y = y if y <= max_dis else max_dis
    else:
        y = y if y >= -max_dis else -max_dis

    # print('{:.2f}'.format(x / (max_dis / (grid_side_length / 2))))
    # print('{:.2f}'.format(y / (max_dis / (grid_side_length / 2))))

    if x >= 0:
        t_x = (np.ceil(x / (max_dis / (grid_side_length / 2))) if int('{:.2f}'.format(x / (max_dis / (grid_side_length / 2)))[-2 : ]) > 50 else np.floor(x / (max_dis / (grid_side_length / 2))))
    else:
        t_x = (np.floor(x / (max_dis / (grid_side_length / 2))) if int('{:.2f}'.format(x / (max_dis / (grid_side_length / 2)))[-2 : ]) > 50 else np.ceil(x / (max_dis / (grid_side_length / 2))))
    if y >= 0:
        t_y = (np.ceil(y / (max_dis / (grid_side_length / 2))) if int('{:.2f}'.format(y / (max_dis / (grid_side_length / 2)))[-2 : ]) > 50 else np.floor(y / (max_dis / (grid_side_length / 2))))
    else:
        t_y = (np.floor(y / (max_dis / (grid_side_length / 2))) if int('{:.2f}'.format(y / (max_dis / (grid_side_length / 2)))[-2 : ]) > 50 else np.ceil(y / (max_dis / (grid_side_length / 2))))

    c_x = np.int32(t_x + (grid_side_length // 2))
    c_y = np.int32((grid_side_length - 1) - (t_y + (grid_side_length // 2)))

    # print('c_x, c_y:', c_x, c_y)

    return c_x, c_y
