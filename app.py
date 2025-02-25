from tkinter import *
from screeninfo import get_monitors
import pywinctl as pwc
import time
import atexit
from sqlalchemy import create_engine, insert, text
from models import Base, Application, Usage
import pandas as pd
import matplotlib.pyplot as plt

engine = create_engine('mysql+mysqlconnector://user:password@127.0.0.1/jikan_db')

Base.metadata.create_all(engine)

#stmt = insert(Application).values(application_name="Discord", date="2025-02-19")

#with engine.connect() as connection:
#    connection.execute(stmt)
#    connection.commit()
#with engine.connect() as connection:
#    # Étape 1: Lister les tables dans la base de données
#    result = connection.execute(text("SHOW TABLES"))
#    tables = [row[0] for row in result]
#
#    print("Tables dans la base de données :")
#    for table in tables:
#        print(f"- {table}")
#
#        # Étape 2: Lister les colonnes de chaque table
#        print(f"Colonnes de la table {table}:")
#        if table == "usage":
#            describe_result = connection.execute(text(f"DESCRIBE `usage`"))
#        else:
#            describe_result = connection.execute(text(f"DESCRIBE {table}"))
#        for column in describe_result:
#            print(f"  {column[0]} ({column[1]})")
#
#        # Étape 3: Afficher les données de chaque table
#        print(f"Données de la table {table}:")
#        data_result = connection.execute(text(f"SELECT * FROM `{table}`"))
#        for row in data_result:
#            print(row)  # Affiche chaque ligne de la table
#
#        print("\n" + "-"*50 + "\n")
# df = pd.read_sql_table('application', engine)
# print(df)
# df['count'] = 1
# df.plot(kind='bar', x='application_name', y='count')
# plt.show()
#

app_windows_dict = {}

#def test():
#
#atexit.register(test)


while True:
    time.sleep(1)
    if app_windows_dict.get(pwc.getActiveWindowTitle()) is not None:
        app_windows_dict[pwc.getActiveWindowTitle()] += 1
    else:
        app_windows_dict[pwc.getActiveWindowTitle()] = 0
    print(app_windows_dict[pwc.getActiveWindowTitle()], pwc.getActiveWindow())
    print(pwc.getAllAppsWindowsTitles())
    # app_windows_dict.pop("gjs")
    pwc.getActiveWindowTitle()

    # print(pwc.getActiveWindowTitle())


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
