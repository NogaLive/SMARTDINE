from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pika
import json
from .database import engine, Base, get_db
from .models import Pedido
from fastapi.middleware.cors import CORSMiddleware

# Crear tablas (En producción usar Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartDine Order Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración RabbitMQ
def publicar_evento_pedido(pedido_data):
    # 1. Definimos las credenciales que pusimos en Docker
    credentials = pika.PlainCredentials('admin', 'password')
    
    # 2. Nos conectamos pasando esas credenciales
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()
    
    # 3. Aseguramos que la cola exista
    channel.queue_declare(queue='pedidos_queue', durable=True)
    
    # 4. Publicamos el mensaje
    channel.basic_publish(
        exchange='',
        routing_key='pedidos_queue',
        body=json.dumps(pedido_data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Hace persistente el mensaje
        )
    )
    print(f" [x] Enviado a RabbitMQ: {pedido_data}") # Log para confirmar envío
    connection.close()

# DTO para recibir datos
class PedidoCreate(BaseModel):
    mesa_qr_id: str
    total: float

@app.post("/pedidos/")
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    # 1. Guardar en PostgreSQL (Transaccional)
    nuevo_pedido = Pedido(mesa_qr_id=pedido.mesa_qr_id, total=pedido.total)
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    
    # 2. Publicar evento asíncrono a RabbitMQ
    evento = {
        "id": nuevo_pedido.id,
        "mesa_qr_id": nuevo_pedido.mesa_qr_id,
        "total": nuevo_pedido.total,
        "accion": "NUEVO_PEDIDO"
    }
    try:
        publicar_evento_pedido(evento)
    except Exception as e:
        print(f"Error conectando a RabbitMQ: {e}")
        # No fallamos el request HTTP si falla RabbitMQ, pero logueamos error (Patrón Outbox recomendado)

    return {"mensaje": "Pedido creado", "id": nuevo_pedido.id, "estado": nuevo_pedido.estado}