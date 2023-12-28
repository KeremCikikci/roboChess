# RoboChess
 
Each frame captured by the camera undergoes various processes to eliminate proportional distortions and noise. In the obtained output, each frame is observed individually and converted from BGR format to HSV format.

To reduce errors, colors of chess pieces that are far apart in the spectrum are made more distinguishable through different processes. Thus, the colors of the pieces on all squares are recorded. Since the positions of the pieces are known at the beginning of a chess game, there is no need to determine the types of pieces from the captured image.

For a chess game played on an online platform like Lichess, a unique ID is assigned to the game, and necessary information is retrieved using the Lichess API. However, to prevent cheating attempts, the Lichess API provides move information with a delay. Therefore, in a Lichess game, when a change occurs, a screenshot is taken to detect the move. Moves are recorded in the UCI (Universal Chess Interface) notation, which specifies the starting and ending coordinates of the pieces.

Additionally, the pieces obtained from Lichess at the beginning of the game are compared with the pieces detected in the squares from the camera. If they are not in sync, differing square coordinates are marked. When it's a player's turn, data flow is monitored from the Arduino, and if the button is pressed, the camera observes the pieces in the squares again. By identifying the differing pieces from the previously saved content, it's determined whether any piece has been captured. Then, a move notation is created in UCI format, and the move's validity is checked. The move is sent to the Lichess game with the assigned ID using the Lichess API. Additionally, time information obtained from the API is sent to Arduino via the Serial port.

At the start of each game, motors rotate until switches are triggered, bringing the robot arm to its home position. This resets all angle values and motors, enabling the robot arm to move to the desired coordinate in subsequent commands. After the home position, the arm moves to a waiting position. A function written in the Arduino code determines the slowest and fastest motor values on the arm, as well as the instantaneous speed during the motor's duty cycle, using a mathematical function.

While power is transmitted via a pulley on the X-axis, reducers are used on the Y and Z axes to greatly reduce the motor's speed and increase its torque by about 60 times. These reducers allow smooth movement of the load motors without excessive force.

In the final arm segment of the robot, there is a structure that lifts the chess pieces using a funnel. When triggered in the center of the funnel, a coil creates a magnetic field to lift the pieces by attracting the screws on top of them. Due to the high current drawn by the coil, it's triggered by a relay.

In the program, the chessboard is considered a coordinate axis, and after providing the coordinates where only the farthest point of the arm will be, the most economical angle values for the arm to reach the desired location are calculated. Motors bring the robot to the calculated angle values.

The movement path of the arm is determined by the move notation sent from the Serial monitor. When the arm movement is complete, it notifies the Python program. Additionally, time information is conveyed throughout the game. The remaining time of the opponents is visualised on displays. While each LED control of the displays requires 20 separate data wires, with 2 shift register chips, the data is transmitted using only 3 wires. The shift registers sequentially light up the required LEDs in each segment of the display. This process happens so quickly that the human eye perceives the LEDs as lit simultaneously.
