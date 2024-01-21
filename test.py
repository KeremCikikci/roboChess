import cv2
import numpy as np

fx = 914.413655169
fy = 915.827825362
cx = 634.088633608
cy = 373.530293726
k1 = -0.474162217
k2 = 0.296860407
k3 = 0.000851414
k4 = -0.001612337

def fisheye_correction(img):
    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0, 0, 1]], dtype=np.float64)

    D = np.array([k1, k2, k3, k4], dtype=np.float64)

    corrected_img = cv2.fisheye.undistortImage(img, K, D, Knew=K)
    return corrected_img

#cam = cv2.VideoCapture(0)

#ret, frame = cam.read()
#if not ret:
#    print("failed to grab frame")

foto = cv2.imread("squares/e6.jpg")

foto = cv2.cvtColor(foto, cv2.COLOR_BGR2HSV)
cv2.imwrite("test.jpg", foto)