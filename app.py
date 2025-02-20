from tkinter import *
from screeninfo import get_monitors
import pywinctl as pwc
import time
import atexit
from sqlalchemy import create_engine
from models import Base, UsageStats

engine = create_engine('mysql+mysqlconnector://user:password@127.0.0.1/jikan_db')

Base.metadata.create_all(engine)

print("Tables créées ou déjà existantes.")


app_windows_dict = {}

#def test():
#
#atexit.register(test)


while True:
    if app_windows_dict.get(pwc.getActiveWindowTitle()) is not None:
        app_windows_dict[pwc.getActiveWindowTitle()] += 1
    else:
        app_windows_dict[pwc.getActiveWindowTitle()] = 0
    print(app_windows_dict[pwc.getActiveWindowTitle()], pwc.getActiveWindow())
    # app_windows_dict.pop("gjs")
    pwc.getActiveWindowTitle()
    time.sleep(1)
    print(pwc.getActiveWindowTitle())


print("getting killed")

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
#
#
#window.mainloop()
