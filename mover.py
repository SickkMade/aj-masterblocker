from filetoarray import filetoarray
import pyautogui
from colorchanger import colorchanger
import time
import pyscreeze
import numpy as np

class mover():
    def __init__(self, file):
        self.voxel_data = filetoarray.layer_based_voxel_data(file)
        self._color_data = filetoarray.get_color_data(file)
        self._location = (0,0,0)
        self._pause = 0.05
        pyautogui.PAUSE = self._pause
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
                            organized[data] = {}
                        else:
                            if z not in organized[data]:
                                organized[data][z] = [loc]
                            else:
                                if z % 2 == 1: #every other row we put in reverse so cursor doesnt have to go all the way back to start
                                    organized[data][z].insert(0, loc)
                                else:
                                    organized[data][z].append(loc)
                
        for key in organized:
            self._color(key)
            for second_key in organized[key]: # for every new layer
                self._check_timeout()
                for value in organized[key][second_key]:
                    value = (value[0] - self._shape[0] // 2, value[1] - self._shape[1] //2 , value[2])
                    self._move(value)
        self._save()
    
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
        time.sleep(1)

    def _move(self, location):
        move_to = tuple(map(lambda i, j: i - j, self._location, location))
        x, y, z = move_to
        for _ in range(abs(x)):
            self._move_dir(x, 0)
        for _ in range(abs(y)):
            self._move_dir(y, 1)
        for _ in range(abs(z)):
            self._move_dir(z, 2)
        time.sleep(0.01)
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

    def _save(self):
        location = pyscreeze.locateCenterOnScreen('images/save.png', confidence=0.7)
        pyautogui.click(location)
        time.sleep(0.3)
        location = pyscreeze.locateCenterOnScreen('images/add.png', confidence=0.7)
        pyautogui.click(location)
        time.sleep(0.3)
        location = pyscreeze.locateCenterOnScreen('images/okay.png', confidence=0.7)
        pyautogui.click(location)

    def _check_timeout(self):
        try:
            location = pyscreeze.locateCenterOnScreen('images/timeout.png', confidence = 0.9)
            pyautogui.click(location)
            time.sleep(0.2)
        except pyscreeze.ImageNotFoundException:
            pass