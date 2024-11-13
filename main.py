from fastapi import FastAPI
from app.routers import key_pair, table_creation

app = FastAPI(
    title="SSH Key Pair Generator API",
    description="API for generating and managing SSH key pairs and database tables.",
    version="1.0.0"
)

# Include routers
app.include_router(key_pair.router)
app.include_router(table_creation.router)
