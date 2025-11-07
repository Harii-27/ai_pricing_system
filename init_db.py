from database import Base, engine
from models import PriceHistory  # noqa

Base.metadata.create_all(bind=engine)
