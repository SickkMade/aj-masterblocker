from PIL import Image
import numpy as np

class colorchanger():
    def rgb_to_image_pos(target_rgb):
        image = 'images/colors.png'
    
        # Open the image and convert to RGB mode
        img = Image.open(image).convert("RGB")
        img_data = np.array(img)
        
        # Initialize a mask to keep track of visited pixels
        visited = np.zeros_like(img_data[:, :, 0], dtype=bool)

        # Reshape the image to a 2D array of pixels
        img_pixels = img_data.reshape((-1, 3))

        # Calculate the Euclidean distance between each pixel and the target RGB value
        distances = np.linalg.norm(img_pixels - target_rgb, axis=1)

        # Find the index of the pixel with the smallest distance that has not been visited
        closest_pixel_index = np.argmin(distances * ~visited.ravel())

        # Convert the 1D index to 2D coordinates
        closest_pixel_y, closest_pixel_x = np.unravel_index(closest_pixel_index, img_data.shape[:2])

        # Mark the pixel as visited
        visited[closest_pixel_y, closest_pixel_x] = True

        return closest_pixel_x + 930 + 20, closest_pixel_y + 545 + 20
        # image = 'images/colors.png'
        # # Open the image and convert to RGB mode
        # img = Image.open(image).convert("RGB")

        # colors = np.array(img)
        # distances = np.sqrt(np.sum((colors-target_rgb)**2,axis=1))
        # index_of_smallest = np.where(distances==np.amin(distances))
        # smallest_distance = colors[index_of_smallest]
        # return smallest_distance

        # return col + 930, row + 545