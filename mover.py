from filetoarray import filetoarray
import pyautogui
from colorchanger import colorchanger
import time
import numpy as np

class mover():
    def __init__(self, file):
        self.voxel_data = filetoarray.layer_based_voxel_data(file)
        self._color_data = filetoarray.get_color_data(file)
        self._location = (0,0,0)
        pyautogui.PAUSE = 0.035
        self._shape = filetoarray.get_size(file)


    def draw(self):
        organized = {}
        for z in range(len(self.voxel_data)):  # Loop through the first dimension
            for y in range(len(self.voxel_data[z])):  # Loop through the second dimension
                for x in range(len(self.voxel_data[z][y])):  # Loop through the third dimension
                    data = self.voxel_data[z][y][x]
                    loc = (z, y, x)
                    if data != 0 and self.is_edge(loc):
                        if data not in organized:
                            organized[data] = [loc]
                        else:
                            organized[data].append(loc)
                
        for key in organized:
            self._color(key)
            for value in organized[key]:
                value = (value[0] - self._shape[0] // 2, value[1] - self._shape[1] //2 , value[2])
                self._move(value)
    
    def _color(self, index):
        target_rgb = self._color_data[index]
        pyautogui.press('p')
        time.sleep(1.5)
        click_loc = colorchanger.rgb_to_image_pos(np.array([target_rgb[0], target_rgb[1], target_rgb[2]]))
        pyautogui.click(*click_loc)
        pyautogui.click(*click_loc)
        pyautogui.click(*click_loc)
        pyautogui.click(*click_loc)
        pyautogui.click(*click_loc) #shut up
        time.sleep(1)
        pyautogui.press('p')

    def _move(self, location):
        move_to = tuple(map(lambda i, j: i - j, self._location, location))
        x, y, z = move_to
        for _ in range(abs(x)):
            self._move_dir(x, 0)
        for _ in range(abs(y)):
            self._move_dir(y, 1)
        for _ in range(abs(z)):
            self._move_dir(z, 2)
        pyautogui.press('space')
        self._location = location

    def _move_dir(self, direction, axis): #0 is x, 1 is y, 2 is z
        if direction > 0:
            if axis == 0: #x
                pyautogui.press('a')
            elif axis == 1: #y
                pyautogui.press('s')
            else: #z
                pyautogui.press('q')
        elif direction < 0:
            if axis == 0: #x
                pyautogui.press('d')
            elif axis == 1: #y
                pyautogui.press('w')
            else: #z
                pyautogui.press('e')

    def is_edge(self, loc):#pass thru x,y,z and check if in 3d space it's an edge, if not we don't draw it\
        offsets = [
        (-1, 0, 0), (1, 0, 0),
        (0, -1, 0), (0, 1, 0),
        (0, 0, -1), (0, 0, 1)
        ]
        for x, y, z in offsets:
            nx, ny, nz = loc[0] + x, loc[1] + y, loc[2] + z
            if 0 <= nx < len(self.voxel_data) and 0 <= ny < len(self.voxel_data[0]) and 0 <= nz < len(self.voxel_data[0][0]): #if we are in range
                if self.voxel_data[nx][ny][nz] == 0: #if one size has air around it it will be drawn
                    return True
        return False
                
        