from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine
from app.models import Base
from app.database import DATABASE_URL
import logging
import secrets
import os

router = APIRouter(
    prefix="/db",
    tags=["Database Operations"]
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up basic authentication
security = HTTPBasic()

# Define your username and password (use environment variables)
USERNAME = os.getenv("ADMIN_USERNAME")
PASSWORD = os.getenv("ADMIN_PASSWORD")

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

@router.post("/create_prereq_table", summary="Create prerequisite tables in the database", dependencies=[Depends(authenticate)])
def create_prereq_table():
    """
    Creates all tables defined in the SQLAlchemy models.
    If tables already exist, they will not be recreated.
    """
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        message = "All prerequisite tables have been created or already exist."
        logger.info(message)
        return {"message": message}
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating tables."
        )
