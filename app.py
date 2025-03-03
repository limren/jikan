import atexit
import time
from tkinter import *

import pywinctl as pwc
from sqlalchemy import create_engine, insert, select, text
from sqlalchemy.orm import sessionmaker

from models import Application, Usage
from config import engine, SessionLocal, Base

# Base.metadata.create_all(engine)

session = SessionLocal()

with engine.connect() as connection:
    # Étape 1: Lister les tables dans la base de données
    result = connection.execute(text("SHOW TABLES"))
    tables = [row[0] for row in result]

    print("Tables dans la base de données :")
    for table in tables:
        print(f"- {table}")

        # Étape 2: Lister les colonnes de chaque table
        print(f"Colonnes de la table {table}:")
        if table == "usage":
            describe_result = connection.execute(text(f"DESCRIBE `usage`"))
        else:
            describe_result = connection.execute(text(f"DESCRIBE {table}"))
        for column in describe_result:
            print(f"  {column[0]} ({column[1]})")

        # Étape 3: Afficher les données de chaque table
        print(f"Données de la table {table}:")
        data_result = connection.execute(text(f"SELECT * FROM `{table}`"))
        for row in data_result:
            print(row)  # Affiche chaque ligne de la table

        print("\n" + "-"*50 + "\n")

app_windows_dict = {}


def get_app_by_name(app_name):
    result = session.query(Application).filter_by(application_name=app_name).first()
    return result

def create_usage(app_id, usage_title, usage_seconds):
    stmt = insert(Usage).values(application_id=app_id, title=usage_title, seconds=usage_seconds)
    return session.execute(stmt)

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
            res = create_usage(app.id, usage['title'], usage['seconds'])
            print("res : ", res)


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

