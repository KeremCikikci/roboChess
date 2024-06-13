from ultralytics import YOLO

"""
-> This piece of code is used only once and has no role in executing the main.py code.

-> In this code, 772 manually classified chess square photographs are used to train a yolov8 classifier model.

-> The model was trained in the Google Colab cloud Editor using NVIDIA® T4 data center GPU in 4 hours.

-> The data set structure is as stated below:

dataset
|           |--> black: black_01.jpg, black_02.jpg, ...
|           |
|--> test --|--> space: space_01.jpg, space_02.jpg, ...
|           |
|           |--> white: white_01.jpg, white_02.jpg, ...
|
|
|           |--> black: black_01.jpg, black_02.jpg, ...
|           |
|--> train--|--> space: space_01.jpg, space_02.jpg, ...
|           |
|           |--> white: white_01.jpg, white_02.jpg, ...
|
|
|           |--> black: black_01.jpg, black_02.jpg, ...
|           |
|--> valid--|--> space: space_01.jpg, space_02.jpg, ...
            |
            |--> white: white_01.jpg, white_02.jpg, ...

-> The model outputs 0, 1 or 2, depending on which color chess figure is in the chess square in the photo:

       |       CONFIDENCE      |
SQUARE |-----------------------| OUTPUT
       | BLACK | SPACE | WHITE |       
-------|-------|-------|-------|-------
 black |   >   |   -   |   -   |   0
-------|-------|-------|-------|-------
 space |   -   |   >   |   -   |   1
-------|-------|-------|-------|-------
 white |   -   |   -   |   >   |   2


"""

DATA_DIR = None # The dataset is not included in the folder because it is too large.

model = YOLO("yolov8n-cls.pt")

model.train(data=DATA_DIR, epochs=50, imgsz=640) # image size 640 is not required

# Results saved to runs/classify/train