import atexit
import time
from tkinter import *

import pywinctl as pwc
from sqlalchemy import create_engine, insert, select, text
from sqlalchemy.orm import sessionmaker

from models import Application, Usage
from config import engine, SessionLocal, Base
from controllers import UsageController, ApplicationController
import pandas as pd
# Base.metadata.create_all(engine)

session = SessionLocal()


# Récupérer les données sous forme de DataFrame
applications_df = pd.read_sql(session.query(Application).statement, engine)
usage_df = pd.read_sql(session.query(Usage).statement, engine)

result = session.execute(text("SELECT count(*) FROM `usage`"))
rows = result.fetchall()  # Récupère toutes les lignes

for row in rows:
    print(row)  # Affiche chaque ligne
#
#with engine.connect() as connection:
#    # Étape 1: Lister les tables
#    result = connection.execute(text("SHOW TABLES"))
#    tables = [row[0] for row in result.fetchall()]
#
#    print("Tables dans la base de données :")
#    for table in tables:
#        print(f"\n- {table}")
#
#        # Étape 2: Lister les colonnes
#        describe_result = connection.execute(text(f"DESCRIBE `{table}`")).fetchall()
#        columns = [col[0] for col in describe_result]
#        print(f"Colonnes: {', '.join(columns)}")
#
#        # Étape 3: Récupérer les données
#        data_result = connection.execute(text(f"SELECT * FROM `{table}`"))
#        data = data_result.fetchall()
#
#        if data:
#            df = pd.DataFrame(data, columns=columns)
#            print(df.to_string(index=False))  # Affiche bien en tableau sans index
#            df.to_csv(f"{table}_data.csv", index=False, encoding="utf-8")
#        else:
#            print("Aucune donnée dans cette table.")
#
#        print("\n" + "-" * 50 + "\n")

app_windows_dict = {}



atexit.register(lambda: UsageController.register_usages_per_app(app_dictionary=app_windows_dict))

while True:
    active_window = pwc.getActiveWindow()

    # Handling the case where there's no app running or an error occurred
    if not active_window:
        time.sleep(1)
        if 'idling' not in app_windows_dict:
            app_windows_dict['idling'] = [{
                'title': 'None',
                'seconds': 1
            }]
        else:
            app_windows_dict['idling'][0]['seconds'] += 1
        continue
    app_name = active_window.getAppName()
    active_window_title = pwc.getActiveWindowTitle()
    time.sleep(1)

    in_dict = False

    if app_name not in app_windows_dict:
        app_windows_dict[app_name] = []

    for item in app_windows_dict[app_name]:
        if item['title'] == active_window_title:
            in_dict = True
            item['seconds'] += 1
            break

    if not in_dict:
        if app_windows_dict[app_name] is not None:
            app_windows_dict[app_name].append({
                'title': active_window_title,
                'seconds': 1
            })

