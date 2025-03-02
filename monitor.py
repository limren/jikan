from tkinter import *

from screeninfo import get_monitors
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://user:password@127.0.0.1/jikan_db')

window = Tk()

w_window = 1920*0.6
h_window = 1080*0.6

for m in get_monitors():
    if m.is_primary:
        w_window = int(m.width * 0.6)
        h_window = int(m.height * 0.6)

window.title("Jikan")
window.minsize(w_window, h_window)



window.mainloop()
