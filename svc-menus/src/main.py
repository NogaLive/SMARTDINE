from fastapi import FastAPI, HTTPException
from .database import db
from .models import Plato
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SmartDine Menu Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    db.connect()

@app.on_event("shutdown")
async def shutdown():
    db.close()

@app.post("/menus/{restaurante_id}/platos", response_model=Plato)
async def crear_plato(restaurante_id: str, plato: Plato):
    plato_dict = plato.dict(by_alias=True, exclude={"id"})
    plato_dict["restaurante_id"] = restaurante_id
    
    new_plato = await db.client.smartdine_menus.platos.insert_one(plato_dict)
    plato.id = str(new_plato.inserted_id)
    
    # Invalidar caché del restaurante
    await db.redis_client.delete(f"menu:{restaurante_id}")
    return plato

@app.get("/menus/{restaurante_id}")
async def obtener_menu(restaurante_id: str):
    # 1. Intentar obtener de Redis (Cache Hit)
    cached_menu = await db.redis_client.get(f"menu:{restaurante_id}")
    if cached_menu:
        return json.loads(cached_menu)

    # 2. Buscar en Mongo (Cache Miss)
    platos_cursor = db.client.smartdine_menus.platos.find({"restaurante_id": restaurante_id})
    platos = []
    async for plato in platos_cursor:
        plato["_id"] = str(plato["_id"])
        platos.append(plato)

    # 3. Guardar en Redis por 10 minutos
    await db.redis_client.setex(f"menu:{restaurante_id}", 600, json.dumps(platos))
    
    return platos