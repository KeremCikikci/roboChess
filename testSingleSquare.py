import cv2
import numpy as np
import math

#cam = cv2.VideoCapture(0)

#ret, frame = cam.read()
# if not ret:
#     print("failed to grab frame")
    
#cv2.imwrite("test.jpg", frame)

lowerWhite_hsv = (0, 0, 125)
upperWhite_hsv = (180, 20, 255)
lowerBlack_hsv = (120, 30, 20)
upperBlack_hsv = (150, 205, 70)

#beyaz = cv2.imread('squares/h7.jpg')
beyaz = cv2.imread('test.jpg')
beyaz = cv2.cvtColor(beyaz, cv2.COLOR_BGR2HSV)

square_pixels = beyaz.shape[0] * beyaz.shape[1]

mask_white = cv2.inRange(beyaz, lowerWhite_hsv, upperWhite_hsv)
mask_black = cv2.inRange(beyaz, lowerBlack_hsv, upperBlack_hsv)

white_pixels = np.sum(mask_white > 0)
white_intensity = white_pixels / square_pixels

black_pixels = np.sum(mask_black > 0)
black_intensity = black_pixels / square_pixels

result_beyaz = cv2.bitwise_and(beyaz, beyaz, mask=mask_white)
result_siyah = cv2.bitwise_and(beyaz, beyaz, mask=mask_black)

stitcher = cv2.Stitcher_create()

vis = np.concatenate((result_beyaz, result_siyah), axis=1)

cv2.imshow("beyaz", vis)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(white_pixels / square_pixels, black_pixels / square_pixels)

def colorDetect(img):
    im = cv2.imread(img)
    imChannelR = im[:,:,2] # R kanalını al
    imChannelG = im[:,:,1] # B kanalını al
    imChannelB = im[:,:,0] # B kanalını al
    imChannelSumR = np.sum(imChannelR)/255 # R kanalı değerleri toplamı
    imChannelSumG = np.sum(imChannelG)/255 # R kanalı değerleri toplamı
    imChannelSumB = np.sum(imChannelB)/255 # B kanalı değerleri toplamı
    
    print(imChannelSumB, imChannelSumG, imChannelSumR)
    if imChannelSumB > 400 and imChannelSumR > 400:
        print("beyaz")
    if (imChannelSumR > imChannelSumB): print("{} Kırmızı taş".format(img))
    else: return print("{} Mavi taş".format(img))

#colorDetect("kareler/e5.jpg")