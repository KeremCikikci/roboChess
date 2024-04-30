## Run RoboChess
Install the necessary packages before running the code.
<pre lang=lisp
pip install -r requirements.txt
</pre>

Before running the code, Arduino Uno must be connected to the computer and the `main.py` file must be configured.

+ Connect Arduino to your computer and specify its port
`ARDUINO_PORT = <your_arduino_port>`
+ Create a game from Lichess and assign the game link to the code.
`GAME_ID = <your_game_id>`
+ Position an external camera to see the chessboard and connect the camera to your computer.

Run the main code in the directory where you downloaded the repository.
<pre lang=lisp
python main.py
</pre>

