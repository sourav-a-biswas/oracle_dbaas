from . import models, schemas
from sqlalchemy.orm import Session

def create_ssh_key(db: Session, ssh_key: schemas.SSHKeyCreate, private_key: str, public_key: str):
    db_ssh_key = models.SSHKey(
        description=ssh_key.description,
        private_key=private_key,
        public_key=public_key
    )
    db.add(db_ssh_key)
    db.commit()
    db.refresh(db_ssh_key)
    return db_ssh_key
