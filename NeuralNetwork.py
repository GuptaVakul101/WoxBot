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
    img_left_l_half = img[0:height, 0:width //6]
    img_left_r_half = img[0:height, width // 6: width // 3]
    img_center = img[0:height , width // 3:(2 * width // 3)]
    img_right_l_half = img[0:height, (2 * width // 3): (5 * width)//6]
    img_right_r_half = img[0:height, (5 * width // 6):width]


    return img_left_l_half, img_left_r_half, img_center, img_right_l_half, img_right_r_half

'''
        Given an image and color, this function returns where the color is maximum
        :returns 000: Target Color Not Ahead
                 001: Target Color at left
                 010: Target Color at center
                 011: Target Color at right
                 100: Target Color at center-Left
                 101: Target Color at center-right
'''
def NeuralNetwork(img, color):
    img_left_l_half, img_left_r_half, img_center, img_right_l_half, img_right_r_half = splitImageIntoThree(img)
    img_left_l_half_count = countPixelsOfColor(img_left_l_half, color)
    img_left_r_half_count = countPixelsOfColor(img_left_r_half, color)
    center_count = countPixelsOfColor(img_center, color)
    img_right_l_half = countPixelsOfColor(img_right_l_half, color)
    img_right_r_half = countPixelsOfColor(img_right_r_half, color)

    max_count = max(img_left_l_half_count,img_left_r_half_count,center_count,img_right_l_half,img_right_r_half)
    if max_count < THRESHOLD:
        return 0
    if max_count == img_left_l_half_count:
        return 1
    elif max_count == center_count:
        return 2
    elif max_count == img_right_r_half:
        return 3
    elif max_count == img_left_r_half_count:
        return 4
    elif max_count == img_right_l_half:
        return 5


# image = cv2.imread('image.jpg')
# print(NeuralNetwork(image, [0, 255, 255]))
