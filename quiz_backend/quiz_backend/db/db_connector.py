from sqlmodel import Session, create_engine, SQLModel

# Importing database URLs from settings module
from quiz_backend.setting import db_url, test_db_url

# Adjusting connection string for PostgreSQL with psycopg2 driver
connection_string = str(db_url).replace("postgresql", "postgresql+psycopg2")

# Creating the SQLAlchemy engine
engine = create_engine(connection_string)

# Function to create tables based on SQLModel metadata
def createTable():
    SQLModel.metadata.create_all(engine)

# Function to get a session for database operations
def get_session():
    # Using context manager to manage database sessions
    with Session(engine) as session:
        yield session
