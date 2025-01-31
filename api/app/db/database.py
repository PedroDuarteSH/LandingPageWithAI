from sqlmodel import create_engine, SQLModel, Session
from config import Settings

settings = Settings()
engine = create_engine(settings.database_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency to get a database session
def get_session():
    with Session(engine) as session:
        yield session