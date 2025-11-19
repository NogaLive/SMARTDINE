from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    mesa_qr_id = Column(String, index=True)
    estado = Column(String, default="RECIBIDO")
    total = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)