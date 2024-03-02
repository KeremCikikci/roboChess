import numpy as np
import cv2
import json
from PIL import ImageGrab
import time

horizontal = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']

#For now, it is not saved to the settings.json file for testing purposes.
fx = 914.413655169
fy = 915.827825362
cx = 634.088633608
cy = 373.530293726
k1 = -0.474162217
k2 = 0.296860407
k3 = 0.000851414
k4 = -0.001612337

def calibCorner():
    def fare_konumu(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"Left Click: x={x}, y={y}")
            corners.append([x, y])

    corners = []

    with open('settings.json', 'r') as file:
        data = json.load(file)

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Select Corner")
    cv2.setMouseCallback("Select Corner", fare_konumu)

    while True:
        ret, frame = cam.read()

        cv2.imshow("Select Corner", frame)

        if len(corners) == 4:
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    data['corners'] = corners

    with open('settings.json', 'w') as file:
        json.dump(data, file, indent=2)

def calibBoard(width, height):
    references = [[None] * 8 for _ in range(8)]
    squareWidth, squareHeight = width / 8, height / 8

    with open('settings.json', 'r') as file:
        data = json.load(file)
    
    assert "corners" in data, "corners data is missing!"
    pts1 = np.float32(data["corners"])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    cam = cv2.VideoCapture(0)

    ret, board = cam.read()

    im = cv2.warpPerspective(board, matrix, (width, height))

    for x in range(8):
        for y in range(8):
            square = im[int(y * squareHeight):int((y+1) * squareHeight), int(x * squareWidth):int((x+1)*squareWidth)]

            references[x][y] = channelSums(square)

    cam.release()

    cv2.destroyAllWindows()

    data["references"] = references

    with open('settings.json', 'w') as file:
        json.dump(data, file, indent=2)

def channelSums(im):
    imChannelSumR = np.sum(im[:,:,2])/255
    imChannelSumG = np.sum(im[:,:,1])/255
    imChannelSumB = np.sum(im[:,:,0])/255

    return int((imChannelSumR + imChannelSumG + imChannelSumB) / 3)

### Last Version ###
def detectColor(square, lowerWhite_hsv, upperWhite_hsv, lowerBlack_hsv, upperBlack_hsv, whiteTreshold, blackTreshold):
    color = 1
    
    square = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)

    square_pixels = square.shape[0] * square.shape[1]

    mask_white = cv2.inRange(square, lowerWhite_hsv, upperWhite_hsv)
    mask_black = cv2.inRange(square, lowerBlack_hsv, upperBlack_hsv)

    white_pixels = np.sum(mask_white > 0)
    white_intensity = white_pixels / square_pixels

    black_pixels = np.sum(mask_black > 0)
    black_intensity = black_pixels / square_pixels
    
    if white_intensity > whiteTreshold and white_intensity > black_intensity:
        color = 2
    elif black_intensity > blackTreshold and black_intensity > white_intensity:
        color = 0

    return color

def detectChanges(list1, list2):
    changes = []
    for i in range(8):
        for a in range(8):
            if list1[i][a] != list2[i][a]:
                changes.append(horizontal[7-i] + str(a+1))
                # if reverse:
                #     changes.append(horizontal[7-i] + str(a + 1))
                # else:
                #     changes.append(horizontal[i] + str(8-a))
    if len(changes) > 4:
        changes = []
    return changes

def detectMove(changes, newContents, oldContents):
    captured = None
    print("DETECT MOVE")
    print(oldContents, newContents)
    # Castling
    if len(changes) == 4:
        if all(element in changes for element in ['e1', 'f1', 'g1', 'h1']) or all(element in changes for element in ['e8', 'f8', 'g8', 'h8']):
            return "KISA", captured
        else:
            return "UZUN", captured
    
    if len(changes) == 2:
        from_ = None
        to_ = None

        if oldContents[horizontal[::-1].index(changes[0][0])][int(changes[0][-1]) - 1] == 1:
            from_ = changes[0]
            to_ = changes[1]
        else:
            from_ = changes[1]
            to_ = changes[0]

        if newContents[horizontal[::-1].index(to_[0])][int(to_[1]) - 1] != 1:
            captured = to_
        
        #print("from: " + from_)
        #print("to: " + to_)
        return from_ + to_, captured
    
def detectLiContents(lowerWhite_hsv, upperWhite_hsv, lowerBlack_hsv, upperBlack_hsv, color_threshold_lichess, x1, y1, x2, y2):
    liContents = [[None] * 8 for _ in range(8)]

    ss = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
    width, height = ss.size
    total_pixels = width * height / 64
    squareWidth, squareHeight = width // 8, height // 8
    ss.save("lichess_sample.jpg")
    for h in range(0, 8):
        for n in range(0, 8):
            square = (h * squareWidth, n * squareHeight, (h+1)*squareWidth, (n+1)*squareHeight)
            cropped = np.array(ss.crop(square))
            cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

            mask_white = cv2.inRange(cropped, lowerWhite_hsv, upperWhite_hsv)
            mask_black = cv2.inRange(cropped, lowerBlack_hsv, upperBlack_hsv)

            white_pixels = np.sum(mask_white > 0)
            white_intensity = white_pixels / total_pixels

            black_pixels = np.sum(mask_black > 0)
            black_intensity = black_pixels / total_pixels
            c = 1

            if white_intensity > color_threshold_lichess or black_intensity > color_threshold_lichess:
                if white_intensity >= black_intensity:
                    c = 2
                else:
                    c = 0
            
            #liContents[h][n] = c
            
            # Vertical Reverse Version
            liContents[h][7-n] = c

            # Horizontal Reverse Version
            #liContents[7- h][n] = c 
    
    return liContents

def move(arduino, move, captured):
    for i in range(3):
        arduino.write(bytes(move, 'utf-8'))
        time.sleep(.2)
    print(captured)
    if captured:
        for i in range(3):
            arduino.write(bytes("C", 'utf-8'))
            time.sleep(.2)
    else:
        for i in range(3):
            arduino.write(bytes("M", 'utf-8'))
            time.sleep(.2)
        

### THE FOLLOWING FUNCTIONS WERE USED IN PREVIOUS VERSIONS ###
def colorDetect(im, mid, midDefPerBlack, midDefPerWhite, vis = False):
    sum = channelSums(im)
    
    color = 1#'Grey_'#+ str(sum - mid)
    if vis:
        color = "1#" + str(sum - mid)

    if sum < mid / 100 * (100 - midDefPerBlack):
        color = 0#'black'#+ str(sum - mid)
        if vis:
            color = "0#" + str(sum - mid)
    elif sum > mid / 100 * (100 + midDefPerWhite):
        color = 2#'white'#+ str(sum - mid)
        if vis:
            color = "2#" + str(sum - mid)

    return color

def colorDetect2(square, lowerWhite_hsv, upperWhite_hsv, lowerBlack_hsv, upperBlack_hsv, color_threshold, vis=False):     
    square = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)
    
    color = 1#'Grey_'#+ str(sum - mid)

    square_pixels = square.shape[0] * square.shape[1]

    mask_white = cv2.inRange(square, lowerWhite_hsv, upperWhite_hsv)
    mask_black = cv2.inRange(square, lowerBlack_hsv, upperBlack_hsv)

    white_pixels = np.sum(mask_white > 0)
    white_intensity = white_pixels / square_pixels

    black_pixels = np.sum(mask_black > 0)
    black_intensity = black_pixels / square_pixels

    if vis:
        color = "1#"# + str(sum - mid)

    if white_intensity > color_threshold:
        color = 2
    elif black_intensity > color_threshold:
        color = 0
    
    print(mask_white, mask_black, black_pixels, white_pixels, square_pixels)
    # if sum < mid / 100 * (100 - midDefPerBlack):
    #     color = 0#'black'#+ str(sum - mid)
    #     if vis:
    #         color = "0#" + str(sum - mid)
    # elif sum > mid / 100 * (100 + midDefPerWhite):
    #     color = 2#'white'#+ str(sum - mid)
    #     if vis:
    #         color = "2#" + str(sum - mid)

    return color
   
def fisheye_correction(img, fx, fy, cx, cy, k1, k2, k3, k4):
    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0, 0, 1]], dtype=np.float64)

    D = np.array([k1, k2, k3, k4], dtype=np.float64)
    
    corrected_img = cv2.fisheye.undistortImage(img, K, D, Knew=K)
    return corrected_img

def findSym(board, corners, model, width, height):
    board = fisheye_correction(board, fx, fy, cx, cy, k1, k2, k3, k4)

    prediction = model.predict(board)

    boxes = prediction[0].boxes

    if len(boxes) == 4:
        x1, y1, w1, h1 = boxes[0].xyxy[0]
        x2, y2, w2, h2 = boxes[1].xyxy[0]
        x3, y3, w3, h3 = boxes[2].xyxy[0]
        x4, y4, w4, h4 = boxes[3].xyxy[0]

        p1 = [int(getClosest(x1, w1, width / 2)), int(getClosest(y1, h1, height / 2))]
        p2 = [int(getClosest(x2, w2, width / 2)), int(getClosest(y2, h2, height / 2))]
        p3 = [int(getClosest(x3, w3, width / 2)), int(getClosest(y3, h3, height / 2))]
        p4 = [int(getClosest(x4, w4, width / 2)), int(getClosest(y4, h4, height / 2))]

        corners = [p1, p2, p3, p4]

        corners = sort_points(corners)

    else:
        print("Detection of missing or excess symbols")
        findSym(board, corners)

    return board, corners

def sort_points(points):
    # Sort by x coordinates
    sorted_points = sorted(points, key=lambda x: x[0])

    # Determine top left and top right points
    leftmost = sorted_points[:2]
    rightmost = sorted_points[2:]

    # Determine upper left and lower left points
    leftmost = sorted(leftmost, key=lambda x: x[1])
    (tl, bl) = leftmost

    # Identify the upper right and lower right points
    rightmost = sorted(rightmost, key=lambda x: x[1])
    (tr, br) = rightmost

    return [tl, tr, br, bl]

def getClosest(x, y, z):
    if abs(x-z) < abs(y-z):
        return x
    else:
        return y
    
def Clock(client, gameID, arduino):
    clocks = client.games.export(gameID)["clocks"]

    whiteClock = None
    blackClock = None

    if len(clocks) >= 2:
        if len(clocks) % 2 == 0:
            whiteClock = clocks[-2] // 100
            blackClock = clocks[-1] // 100
        else:
            whiteClock = clocks[-1] // 100
            blackClock = clocks[-2] // 100

        clock = str(whiteClock) + str(blackClock)
        arduino.write(bytes(clock, 'utf-8'))
    time.sleep(.2)

    arduino.write(bytes(move, 'utf-8'))
    time.sleep(.2)