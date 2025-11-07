from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from database import Base

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer)
    recommended_price = Column(Float)
    reasoning = Column(String)
    created_at = Column(DateTime, server_default=func.now())
