from PIL import Image
import numpy as np

class colorchanger():
    def rgb_to_image_pos(target_rgb):
        image = 'images/colors.png'
        # Open the image and convert to RGB mode
        img = Image.open(image).convert("RGB")

        colors = np.array(img)
        distances = np.sqrt(np.sum((colors-target_rgb)**2,axis=1))
        index_of_smallest = np.where(distances==np.amin(distances))
        smallest_distance = colors[index_of_smallest]
        return smallest_distance

        return col + 930, row + 545
    

print(colorchanger.rgb_to_image_pos(np.array([0, 0,0])))