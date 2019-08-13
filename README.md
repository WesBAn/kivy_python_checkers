# Checkers game on Kivy GUI + Python 3
Simple Checkers game realized using **Kivy** framework and **Python3**. This is first version of the app - *v0.8*, in which you're able to play with someone else on the same PC.

This app uses special Kivy language in [Main.kv](Main.kv) to describe some widgets, used in the app.
## Installation
### Only on MacOS ver>10.0 and Linux
You need to install **Kivy** with all it's extra necessary packages, so you're able to do it using pip

`pip3 install -r requirements.txt` 
## Run
To run app, you need to run main.py file

`python3 main.py`
## Something about the app realization
The first step to create the app bounds with creating the game without any GUI. So, there is [checkers.py](checkers.py) file, which contains a fully-working game app, run in the console mode. So user can only write a move in format a3-b4 and receive the printed game table as an answer.

Consequently, the second step was to include graphical elements, like to surround the backend part with the friendly UI. So all other files constructs frontend part, directly working with [checkers.py](checkers.py) 


