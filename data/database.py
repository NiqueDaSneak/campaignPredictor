from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import logging

# Update the connection string with your actual database credentials
DATABASE_URL = "postgresql://dbuser:password@localhost:5432/mydatabase"

# Set up logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define your table schemas
class RawCampaignData(Base):
    __tablename__ = 'raw_campaign_data'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    goal_amount = Column(Float)
    pledged_amount = Column(Float)
    backers = Column(Integer)

class ProcessedCampaignData(Base):
    __tablename__ = 'processed_campaign_data'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    goal_amount = Column(Float)
    amount_raised = Column(Float)
    backers = Column(Integer)
    feature_1 = Column(Float)
    feature_2 = Column(Float)

class TrainedModel(Base):
    __tablename__ = 'trained_models'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    model = Column(String)

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Function to insert raw data
def insert_raw_data(session, data):
    new_data = RawCampaignData(
        url=data['url'],
        goal_amount=data['goal_amount'],
        pledged_amount=data['pledged_amount'],
        backers=data['backers']
    )
    session.add(new_data)
    session.commit()

# Function to verify database connection
if __name__ == "__main__":
    try:
        engine.connect()
        print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")
