from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta, timezone

Base = declarative_base()

# Define the IST timezone as UTC+5:30
IST = timezone(timedelta(hours=5, minutes=30))

class SSHKey(Base):
    __tablename__ = 'ssh_keys'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=True)
    private_key = Column(Text, nullable=False)
    public_key = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(IST))
