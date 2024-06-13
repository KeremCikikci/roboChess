import cv2
import numpy as np

#cam = cv2.VideoCapture(0)

#ret, frame = cam.read()
# if not ret:
#     print("failed to grab frame")
    
#cv2.imwrite("test.jpg", frame)

lowerWhite_hsv, upperWhite_hsv = (0, 0, 125), (180, 20, 255)
lowerBlack_hsv, upperBlack_hsv = (120, 30, 20), (150, 205, 70)

def colorDetect():
    white = cv2.imread('squares/e6.jpg')
    #white = cv2.imread('test.jpg')
    white = cv2.cvtColor(white, cv2.COLOR_BGR2HSV)

    square_pixels = white.shape[0] * white.shape[1]

    mask_white = cv2.inRange(white, lowerWhite_hsv, upperWhite_hsv)
    mask_black = cv2.inRange(white, lowerBlack_hsv, upperBlack_hsv)

    white_pixels = np.sum(mask_white > 0)
    white_intensity = white_pixels / square_pixels

    black_pixels = np.sum(mask_black > 0)
    black_intensity = black_pixels / square_pixels

    result_white = cv2.bitwise_and(white, white, mask=mask_white)
    result_black = cv2.bitwise_and(white, white, mask=mask_black)

    stitcher = cv2.Stitcher_create()

    vis = np.concatenate((result_white, result_black), axis=1)

    cv2.imwrite("Test.jpg", vis)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(white_pixels / square_pixels, black_pixels / square_pixels)

def colorDetecter2(img):
    im = cv2.imread(img)
    imChannelR = im[:,:,2] # R 
    imChannelG = im[:,:,1] # G 
    imChannelB = im[:,:,0] # B 
    imChannelSumR = np.sum(imChannelR)/255 # R
    imChannelSumG = np.sum(imChannelG)/255 # G
    imChannelSumB = np.sum(imChannelB)/255 # B
    
    print(imChannelSumB, imChannelSumG, imChannelSumR)
    # if imChannelSumB > 400 and imChannelSumR > 400:
    #     print("white")
    # if (imChannelSumR > imChannelSumB): print("{} Red".format(img))
    # else: return print("{} Blue".format(img))