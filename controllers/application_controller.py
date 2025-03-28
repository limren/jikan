from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from models import Application
from config import SessionLocal


class ApplicationController:
    def __init__(self):
        self.session: Session = SessionLocal()

    def get_app_by_name(app_name):
        with SessionLocal() as session:
            result = session.query(Application).filter_by(application_name=app_name).first()
            return result



    def create_app(application_name):
        with SessionLocal() as session:
            stmt = insert(Application).values(application_name=application_name)

            session.execute(stmt)
            session.commit()

            app = session.execute(
                select(Application).where(Application.application_name == application_name)
            ).scalar_one()

            return app
