import numpy as np
import cv2
import json
import copy
import berserk
from colorama import init, Fore, Style
from datetime import timedelta, datetime
import time
import serial
from ultralytics import YOLO

import functions as func

init(autoreset=True)

### CONSTANTS ###
GAME_ID = 'P5JOI8sD'
ARDUINO_PORT = 'COM6'
VIDEO_DEVICE = 0
GAMER = "WHITE"

# For the Old Color Detection Function
midDefPerBlack = 12
midDefPerWhite = 2
showDetails = False

color_threshold = .25
color_threshold_lichess = .1

whiteTreshold = .12
blackTreshold = .1


width, height = 800, 800
squareWidth, squareHeight = int(width / 8), int(height / 8)
horizontal = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']

path = "squares/"

button_trigger = datetime.now()

### ON THE CHESSBOARD ###
# They are not used in the current version
lowerBoardWhite_hsv, upperBoardWhite_hsv = (50, 30, 150), (255, 250, 255)
lowerBoardBlack_hsv, upperBoardBlack_hsv = (120, 30, 20), (150, 205, 70)

lowerWhite_hsv = (0, 0, 50)
upperWhite_hsv = (5, 3, 255)
lowerBlack_hsv = (0, 0, 0)
upperBlack_hsv = (5, 3, 50)

rival = 'WHITE'
if GAMER == 'WHITE':
    rival = 'BLACK'

### VARIABLES ###
contents = [[None] * 8 for _ in range(8)]
liContents = [[None] * 8 for _ in range(8)]
turn = GAMER

### CALIBRATIONS ###
### Calibrate Corners ###
#func.calibCorner()

### Calibrate Board ###
#func.calibBoard(width, height)

### INITIATE ARDUINO ###
arduino = serial.Serial(port=ARDUINO_PORT, baudrate=115200, timeout=0)

### FETCH SETTINGS ###
with open('settings.json', 'r') as file:
    data = json.load(file)

assert "references" in data, "references data is missing!"
references = data['references']

assert "corners" in data, "corners data is missing!"
pts1 = np.float32(data["corners"])

pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)

cam = cv2.VideoCapture(VIDEO_DEVICE)
model = YOLO('best.pt')

### LICHESS ###
API_TOKEN = 'lip_LaYVt0nOKwUnjEv1gJSZ'
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session=session)

x1, y1, x2, y2 = 400, 160, 905, 670

### MATCH THE BOARDS ###
ret, board = cam.read()
cv2.imwrite("board.jpg", board)
board = cv2.warpPerspective(board, matrix, (width, height))

for x in range(8):
    for y in range(8):
        square = board[int(y * squareHeight):int((y+1) * squareHeight), int(x * squareWidth):int((x+1)*squareWidth)]
        
        contents[7-x][y] = func.detectColor(square, model)

        # Old Color Detection Functions

        #contents[7-x][y] = func.detectColor(square, lowerBoardWhite_hsv, upperBoardWhite_hsv, lowerBoardBlack_hsv, upperBoardBlack_hsv, whiteTreshold, blackTreshold)
        #contents[7-x][y] = func.colorDetect(square, references[x][y], midDefPerBlack, midDefPerWhite, vis=showDetails)
        #contents[7-x][y] = func.colorDetect2(square, lowerBoardWhite_hsv, upperWhite_hsv, lowerBlack_hsv, upperBlack_hsv, color_threshold, vis=showDetails)
        
        cv2.imwrite(path+horizontal[x]+str(y+1)+'.jpg', square)
liContents = func.detectLiContents(lowerWhite_hsv, upperWhite_hsv, lowerBlack_hsv, upperBlack_hsv, color_threshold_lichess, x1, y1, x2, y2)

print(contents, liContents)

if liContents == contents:
    print_ = "Boards are synchronous ✔"
    print(f"{Fore.GREEN}{print_}{Style.RESET_ALL}")
else:
    print_ = "Boards are not synchronous ✗"
    print(f"{Fore.RED}{print_}{Style.RESET_ALL}")

    differences = []
    for i in range(len(contents)):
        for j in range(len(contents[i])):
            if contents[i][j] != liContents[i][j]:
                differences.append([i, j])

    for i, j in differences:
        _1 = contents[i][j]
        _2 = liContents[i][j]
        format_1 = f"{Fore.RED}{_1}{Style.RESET_ALL}"
        format_2 = f"{Fore.RED}{_2}{Style.RESET_ALL}"
        print(f"({i}, {j}): {format_1} (Chess Board) -> {format_2} (Lichess)")

while True:
    button_time = datetime.now()

    move = None
    captured = None
    changes = []

    if turn == GAMER:
        #nextMove = input() ##### => If button is not active
        try:
            #pass
            read = arduino.readline().decode().strip()
        except:
            pass
        else:
            if len(read) > 1:
                print(read)
            if read == 'move' and button_time > button_trigger:
            #if 1 == 1: -> Placeholder
                button_trigger = button_time + timedelta(seconds=1)
                
                ret, board = cam.read()
                
                board = cv2.warpPerspective(board, matrix, (width, height))

                newContents = copy.deepcopy(contents)
                #print("check1")
                
                for x in range(8):
                    for y in range(8):
                        square = board[int(y * squareHeight):int((y+1) * squareHeight), int(x * squareWidth):int((x+1)*squareWidth)]

                        contents[7-x][y] = func.detectColor(square, model)

                        # They are not used in the current version
                        #contents[7-x][y] = func.detectColor(square, lowerBoardWhite_hsv, upperBoardWhite_hsv, lowerBoardBlack_hsv, upperBoardBlack_hsv, whiteTreshold, blackTreshold)
                        #contents[7-x][y] = func.colorDetect(square, references[x][y], midDefPerBlack, midDefPerWhite, vis=showDetails)
                
                        cv2.imwrite(path+horizontal[x]+str(y+1)+'.jpg', square)

                changes = func.detectChanges(newContents, contents)

                print(changes)

                if len(changes) == 2 or len(changes) == 4: # for better result set it > 0
                    move, captured = func.detectMove(changes, newContents, contents)
                    
                    print(move, captured)
                    
                    # CASTLING
                    if move == "KISA":
                        if GAMER == "BLACK":
                            move = "e8g8"
                        else:
                            move = "e1g1"
                    elif move == "UZUN":
                        if GAMER == "BLACK":
                            move = "e8c8"
                        else:
                            move = "e1c1"

                    for i in range(20):
                        try:
                            berserk.clients.Board(session=session).make_move(GAME_ID, move)            
                        except berserk.exceptions.ResponseError as e:
                            print(e)
                        else:
                            #print("check2")
                            #print(contents, newContents)

                            #contents = copy.deepcopy(newContents)
                            #liContents = copy.deepcopy(newContents)

                            move, captured = None, None
                            changes = []
                            turn = rival
                            print("It's the opponent's turn!")
                            break
        
    else:
        time.sleep(0.5)
        #newLiContents = copy.deepcopy(liContents)

        newLiContents = func.detectLiContents(lowerWhite_hsv, upperWhite_hsv, lowerBlack_hsv, upperBlack_hsv, color_threshold_lichess, x1, y1, x2, y2)
        changes = func.detectChanges(contents, newLiContents)
        print(contents, newLiContents, len(changes))

        if len(changes) == 2 or len(changes) == 4: # for better result set it > 0
            move, captured = func.detectMove(changes, contents, newLiContents)
    
        if move != None:
            button_trigger = button_time + timedelta(seconds=8)
            print(f"{Fore.CYAN}{move}{Style.RESET_ALL}")

            # Reverse Vertically for Robot
            if len(changes) == 2:
                moveNumber1 = move[1]
                moveNumber2 = move[3]
                move = move[0] + str(9-int(moveNumber1)) + move[2] + str(9-int(moveNumber2))
            
                if captured != None:
                    print(f"{Fore.YELLOW}{captured}{Style.RESET_ALL}")
                    func.move(arduino, move, True)
                else:
                    func.move(arduino, move, False)
                
            else:
                print(f"{Fore.YELLOW}{captured}{Style.RESET_ALL}")
                # Castling
                if move == "UZUN":
                    func.move(arduino, "L", True)
                elif move == "KISA":
                    func.move(arduino, "S", True)

            #liContents = copy.deepcopy(newLiContents)
            contents = copy.deepcopy(newLiContents)
            
            move = None
            turn = GAMER
            print("It's the first player's turn!")
        

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cam.release() 
cv2.destroyAllWindows() 