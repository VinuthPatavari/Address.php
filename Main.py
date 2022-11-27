from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, Float, String, Integer

app = FastAPI()

# SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3:'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# A SQLAlchemny ORM Place
class DBAddress(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String, nullable=True)
    lat = Column(Float)
    lng = Column(Float)

Base.metadata.create_all(bind=engine)

# A Pydantic Address
class Address(BaseModel):
    name: str
    description: Optional[str] = None
    lat: float
    lng: float

    class Config:
        orm_mode = True

# Methods for interacting with the database
def get_address(db: Session, address_id: int):
    return db.query(DBAddress).where(DBAddress.id == address_id).first()

def get_address(db: Session):
    return db.query(DBAddress).all()

def create_address(db: Session, address: Address):
    db_address = DBAddress(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    return db_address

# Routes for interacting with the API
@app.post('/address/', response_model=Address)
def create_address_view(address: Address, db: Session = Depends(get_db)):
    db_address = create_address(db, address)
    return db_address

@app.get('/address/', response_model=List[Address])
def get_address_view(db: Session = Depends(get_db)):
    return get_address(db)

@app.get('/address/{address_id}')
def get_address_view(address_id: int, db: Session = Depends(get_db)):
    return get_address(db, address_id)

require('dbAddress.php');
$address=$_REQUEST['address'];
$query = "DELETE FROM new_record WHERE address=$address"; 
$result = mysqli_query($con,$query) or die ( mysqli_error());
header("Location: view.php");

@app.get('/')
async def root():
    return {'message': 'Location for You'}
