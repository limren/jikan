import atexit
import time
from tkinter import *

import pywinctl as pwc
from sqlalchemy import create_engine, insert, select, text
from sqlalchemy.orm import sessionmaker

from models import Application, Usage
from config import engine, SessionLocal, Base
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


def get_app_by_name(app_name):
    result = session.query(Application).filter_by(application_name=app_name).first()
    return result

def create_usage(app_id, usage_title, usage_seconds):
    stmt = insert(Usage).values(application_id=app_id, title=usage_title, seconds=usage_seconds)
    session.execute(stmt)
    session.commit()

def create_app(application_name):
    stmt = insert(Application).values(application_name=application_name)

    session.execute(stmt)
    session.commit()

    app = session.execute(
        select(Application).where(Application.application_name == application_name)
    ).scalar_one()

    return app

def register_usages_per_app():
    print(app_windows_dict)
    for app_name, usages in app_windows_dict.items():
        app = get_app_by_name(app_name)

        if app is None:
            app = create_app(app_name)

        for usage in usages:
            create_usage(app.id, usage['title'], usage['seconds'])


atexit.register(register_usages_per_app)

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

