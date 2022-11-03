from front.front import MyWindow
from tkinter import *
window = Tk() # open new window
mywin= MyWindow(window) # מעביר את החלון החדש דרך הקלאס שיצרנו בפרונט
window.title("BRAINPUT") # title for window
window.geometry("600x350") # size
window.mainloop() #עושה שאפשר לשנות- מקשיב לשינויים ולא סופי כמו הקומנד ליין
