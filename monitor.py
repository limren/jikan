from tkinter import *

from screeninfo import get_monitors

from config import SessionLocal, engine
from models import Application, Usage
from datetime import datetime, timedelta

start_of_day = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

end_of_day = start_of_day + timedelta(days=1) - timedelta(microseconds=1)

session = SessionLocal()

resId = session.query(Application).filter_by(application_name="chrome").first().id
print(session.query(Application).filter_by(application_name="code").first().application_name)

usagesTdy = session.query(Usage).filter_by(application_id=resId).all()
# usages = session.query(Usage).filter_by(application_id=resId).all()
print("usage tdy : ", usagesTdy)
for usage in usagesTdy:
    print(usage.title, usage.seconds, usage.date)



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
