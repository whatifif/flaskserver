from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

# Define the database path
db_path = 'sqlite:///db/database.db'

# Check if the database file exists
if os.path.exists('db/database.db'):
    # If the database file exists, delete it
    os.remove('db/database.db')

# Create a new SQLAlchemy engine
engine = create_engine(db_path)

# Create a base class for declarative models
Base = declarative_base()

# Define the Group model
class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    owner = Column(String(50))
    createdAt = Column(DateTime, default=datetime.utcnow)

# Create all tables in the engine
Base.metadata.create_all(engine)

# Define the data for the new groups
group_data = [
    {"name": "group1", "owner": "owner1", "createdAt": datetime.utcnow()},
    {"name": "group2", "owner": "owner2", "createdAt": datetime.utcnow()},
    {"name": "group3", "owner": "owner3", "createdAt": datetime.utcnow()}
]

# Create a new sessionmaker bound to the engine
Session = sessionmaker(bind=engine)

# Open a new session
with Session() as session:
    # Insert the new groups into the groups table
    for group in group_data:
        session.add(Group(**group))
    
    # Commit the transaction
    session.commit()
