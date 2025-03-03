from tkinter import *

from screeninfo import get_monitors

from config import SessionLocal, engine
from models import Application, Usage

session = SessionLocal()

print(session.query(Application).filter_by(application_name="discord").first())




#window = Tk()
#
#w_window = 1920*0.6
#h_window = 1080*0.6
#
#for m in get_monitors():
#    if m.is_primary:
#        w_window = int(m.width * 0.6)
#        h_window = int(m.height * 0.6)
#
#window.title("Jikan")
#window.minsize(w_window, h_window)
#
#window.mainloop()
