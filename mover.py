from filetoarray import filetoarray
import pyautogui
from colorchanger import colorchanger
import time
import numpy as np

class mover():
    def __init__(self, file):
        self.voxel_data = filetoarray.get_voxel_data(file)
        self._color_data = filetoarray.get_color_data(file)
        self._location = (0,0,0,0)
        pyautogui.PAUSE = 0.05


    def draw(self):
        organized = {}
        for color_loc in self.voxel_data:
            if color_loc[3] not in organized:
                organized[color_loc[3]] = [color_loc]
            else:
                organized[color_loc[3]].append(color_loc)

        for key in organized:
            self._color(key)
            for value in organized[key]:
                self._move(value)
    
    def _color(self, index):
        target_rgb = self._color_data[index]
        pyautogui.press('p')
        time.sleep(1)
        pyautogui.click(*colorchanger.rgb_to_image_pos(np.array([target_rgb[0], target_rgb[1], target_rgb[2]])))
        pyautogui.press('p')

    def _move(self, location):
        move_to = tuple(map(lambda i, j: i - j, self._location, location))
        x, y, z, n = move_to
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

                
        