
# CV: Team V. Simple Algorithm

# first zoom in, given some width/height to the joint
# top left most white pixel, start counting from top to bottom black pixels
# until we hit another white pixel
# add the number of pixels into float
# divide by the width of the section

# naive algorithm: section area is arbitrary

# Identify images with > difference in area between 
from matplotlib import pyplot as plt
import numpy as np

from PIL import Image
img = Image.open('test.png').convert('L')
img2 = img
img2 = img2.crop((120,170,240,224)) 
#Left, Upper, Right, Lower
# The right can also be represented as (left+width)
# and lower can be represented as (upper+height).
npimage = np.asarray(img)

plt.imshow(npimage, cmap='summer', vmax = 255, vmin = 0, interpolation=None)
plt.show() 

npimage2 = np.asarray(img2)

threshold = 220

space = 0

print(img2.width)
print(img2.height)

for x in range(img2.width):
    for y in range(img2.height):
        if(img2.getpixel((x,y)) > threshold):
            space += 1

plt.imshow(npimage2, cmap='summer', vmax = 255, vmin = 0, interpolation=None)
plt.show() 

print(space)

#Currently just counts space. need to add each array to an array itself,
# then average by array size or width