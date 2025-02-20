from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

# Déclare la base pour les modèles
Base = declarative_base()

# Définis ton modèle de table
class UsageStats(Base):
    __tablename__ = 'website'  # Nom de la table
    id = Column(Integer, primary_key=True, autoincrement=True)
    application_name = Column(String(255), nullable=False)
    time_spent = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
