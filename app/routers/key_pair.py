from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, key_generation
from app.database import get_db
import logging

router = APIRouter(
    tags=["SSH Key Pair"]
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/create_key_pair", response_model=schemas.SSHKeyResponse, summary="Generate and save an SSH key pair")
def create_key_pair_endpoint(ssh_key: schemas.SSHKeyCreate, db: Session = Depends(get_db)):
    try:
        # Generate key pair
        private_key, public_key = key_generation.generate_key_pair()

        # Save to database
        db_ssh_key = crud.create_ssh_key(db, ssh_key, private_key, public_key)

        # Prepare response
        message = f"SSH key pair saved to database with ID: {db_ssh_key.id} and Description: {db_ssh_key.description}"
        logger.info(message)

        response = schemas.SSHKeyResponse(
            id=db_ssh_key.id,
            description=db_ssh_key.description,
            private_key=db_ssh_key.private_key,
            public_key=db_ssh_key.public_key,
            created_at=db_ssh_key.created_at.isoformat(),
            message=message
        )

        return response
    except Exception as e:
        logger.error(f"Error creating SSH key pair: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the SSH key pair."
        )
