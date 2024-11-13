import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from a .env file
load_dotenv()

# Database credentials from environment variables
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_name = os.getenv("DB_NAME")
db_pass = os.getenv("DB_PASS")

# URL encode the password
encoded_db_pass = urllib.parse.quote_plus(db_pass)

# Database URL
DATABASE_URL = f"postgresql+psycopg://{db_user}:{encoded_db_pass}@{db_host}:{db_port}/{db_name}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
