from PIL import Image 
import numpy as np

# table.png is necessary 

img = Image.open('binary_checkerboard.png')
img = np.array(img)
# print(img.shape)
# print(np.unique(img, return_counts=True))
img[img > 255//2] = 255
img[img <= 255//2 ] = 200
print(np.unique(img, return_counts=True))

image = Image.fromarray(img)
image.save('light_checkerboard.png')
