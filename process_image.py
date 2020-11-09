import cv2
import numpy as np

THRESHOLD = 5

def countPixelsOfColor(img, color):
    # color is a list representing the color values in B G R, For Ex: [0,255,255]
    # Find all pixels where the ( NoTE ** BGR not RGB  values match color )
    result = np.count_nonzero(np.all(img == color, axis=2))
    return result

def splitImageIntoThree(img):
    height, width = img.shape[:2]
    img_left = img[0:height, 0:width // 3]
    img_center = img[0:height , width // 3:(2 * width // 3)]
    img_right = img[0:height, (2 * width // 3):width]
    return img_left, img_center, img_right

'''
        Given an image and color, this function returns where the color is maximum
        :returns 00: Target Color Not Ahead
                 01: Target Color at left
                 10: Target Color at center
                 11: Target Color at right
'''
def processImage(img, color):
    img_left, img_center, img_right = splitImageIntoThree(img)
    left_count = countPixelsOfColor(img_left, color)
    center_count = countPixelsOfColor(img_center, color)
    right_count = countPixelsOfColor(img_right, color)

    max_count = max(left_count,right_count,center_count)
    if max_count < THRESHOLD:
        return 0
    if max_count == left_count:
        return 1
    elif max_count == center_count:
        return 2
    elif max_count == right_count:
        return 3


# image = cv2.imread('image.jpg')
# print(processImage(image, [0, 255, 255]))
