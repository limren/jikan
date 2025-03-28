from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from models import Usage
from config import SessionLocal
from .application_controller import ApplicationController

class UsageController:

    @staticmethod
    def create_usage(app_id, usage_title, usage_seconds):
        with SessionLocal() as session:
            stmt = insert(Usage).values(application_id=app_id, title=usage_title, seconds=usage_seconds)
            session.execute(stmt)

    @staticmethod
    def register_usages_per_app(app_dictionary):
       with SessionLocal() as session:
            try:
                for app_name, usages in app_dictionary.items():
                    app = ApplicationController.get_app_by_name(app_name)
                    if app is None:
                        app = ApplicationController.create_app(app_name)

                    usage_entries = [
                        {"application_id": app.id, "title": usage["title"], "seconds": usage["seconds"]}
                        for usage in usages
                    ]
                    session.execute(insert(Usage), usage_entries)

                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error while inserting usages: {e}")


