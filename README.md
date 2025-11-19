🍔 SmartDine - Plataforma de Gestión de Restaurantes (MVP)

SmartDine es una plataforma de microservicios diseñada para la gestión de pedidos en tiempo real. Este proyecto implementa una arquitectura orientada a eventos, persistencia políglota y separación completa entre Frontend y Backend.

🚀 Stack Tecnológico

Componente

Tecnología

Puerto

Responsabilidad

Frontend

React (Vite) + JavaScript

5173

Interfaz de Usuario (PWA)

Svc-Menus

Python 3.12 + FastAPI

8001

Gestión de Menús (Lectura intensiva)

Svc-Orders

Python 3.12 + FastAPI

8002

Transacciones de Pedidos

Svc-Notifications

Python Script (Pika)

N/A

Worker de fondo (Consumidor)

MongoDB

v6.0

27017

Base de Datos NoSQL para Menús

PostgreSQL

v15

5432

Base de Datos Relacional para Pedidos

Redis

v7.0

6379

Caché de alto rendimiento

RabbitMQ

v3-Management

5672

Broker de Mensajería

📋 Prerrequisitos

Docker Desktop (Debe estar en ejecución).

Python 3.12+

Node.js v18+

Visual Studio Code (Recomendado).

🛠️ Instalación y Configuración

Sigue estos pasos en orden en tu terminal (PowerShell).

1. Infraestructura (Docker)

Levanta los servicios de base de datos y mensajería.

docker-compose up -d


2. Configuración del Backend (Python)

Se deben crear entornos virtuales aislados para evitar conflictos de versiones.

A. Servicio de Menús (Puerto 8001)

cd svc-menus
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
deactivate
cd ..


B. Servicio de Pedidos (Puerto 8002)

cd svc-orders
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
deactivate
cd ..


C. Servicio de Notificaciones (Worker)

cd svc-notifications
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
deactivate
cd ..


3. Configuración del Frontend (React)

cd frontend-web
npm install
cd ..


▶️ Ejecución del Sistema

Para operar el sistema completo, se recomienda abrir 4 terminales separadas:

Terminal 1: Servicio de Menús

cd svc-menus
.\.venv\Scripts\uvicorn src.main:app --reload --port 8001


Terminal 2: Servicio de Pedidos

cd svc-orders
.\.venv\Scripts\uvicorn src.main:app --reload --port 8002


Terminal 3: Worker de Notificaciones

cd svc-notifications
.\.venv\Scripts\python main.py


Terminal 4: Frontend Web

cd frontend-web
npm run dev


✅ Validación Funcional

Acceso Web: Navega a http://localhost:5173.

Prueba de Integración:

Visualiza el menú (Cargado desde MongoDB/Redis).

Agrega un ítem al carrito.

Haz clic en "Confirmar Pedido".

Resultado Esperado:

Web: Alerta "¡Pedido enviado a cocina!".

Terminal 3 (Worker): Log del evento recibido vía RabbitMQ:

[🔔] NUEVO EVENTO RECIBIDO:
     - Mesa: mesa-5
     - Total: $15.5
     - Acción: Simulando envío de notificación a cocina...


📚 Documentación de API (Swagger UI)

API Menús: http://localhost:8001/docs

API Pedidos: http://localhost:8002/docs

RabbitMQ Dashboard: http://localhost:15672 (User: admin, Pass: password)

🛑 Detener el Proyecto

Para apagar los servicios y liberar recursos:

Detén las terminales con CTRL + C.

Ejecuta:

docker-compose down