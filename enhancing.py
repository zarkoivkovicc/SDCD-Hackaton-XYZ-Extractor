

import cv2
from matplotlib import pyplot as plt
image_file = "page_1.jpg"
img = cv2.imread(image_file)

def display(im_path):
    dpi = 300
    im_data = plt.imread(im_path)

    height, width  = im_data.shape[:2]
    
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()


inverted_image = cv2.bitwise_not(img)
cv2.imwrite("inverted.jpg", inverted_image)

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_image = grayscale(img)
cv2.imwrite("tgray.jpg", gray_image)

thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
cv2.imwrite("bw_image.jpg", im_bw)

def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)

no_noise = noise_removal(im_bw)
cv2.imwrite("no_noise.jpg", no_noise)

def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((3,3),np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)


eroded_image = thin_font(no_noise)
cv2.imwrite("eroded_image.jpg", eroded_image)


def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((1,1),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

dilated_image = thick_font(no_noise)
cv2.imwrite("dilated_image.jpg", dilated_image)

