from database import Base, engine
from models import PriceHistory

Base.metadata.create_all(bind=engine)
