# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel




# Crear la aplicación
app = FastAPI(title="El Encanto de la Huerta API")



# ===== CONFIGURAR CORS (NUEVO) =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (para desarrollo)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)


# Ruta principal - Cuando alguien visite /
@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de El Encanto de la Huerta",
        "version": "1.0",
        "endpoints": ["/productos", "/docs"]
    }


# Ruta para obtener productos
@app.get("/productos")
def obtener_productos():
    # Por ahora, productos de prueba (hardcoded)
    productos = [
        {
            "id": 1,
            "nombre": "Manzanas Golden",
            "categoria": "frutas",
            "precio": 1.50,
            "stock": 100,
            "unidad": "kg"
        },
        {
            "id": 2,
            "nombre": "Naranjas Valencia",
            "categoria": "frutas",
            "precio": 2.25,
            "stock": 200,
            "unidad": "kg"
        },
        {
            "id": 3,
            "nombre": "Plátanos de Canarias",
            "categoria": "frutas",
            "precio": 1.80,
            "stock": 120,
            "unidad": "kg"
        },
        {
            "id": 4,
            "nombre": "Tomates",
            "categoria": "verduras",
            "precio": 2.20,
            "stock": 90,
            "unidad": "kg"
        },
        {
            "id": 5,
            "nombre": "Lechugas",
            "categoria": "verduras",
            "precio": 1.50,
            "stock": 73,
            "unidad": "ud"
        }
    ]
    return productos


# Ruta para obtener UN producto específico
@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    # Lista de productos (la misma de arriba)
    productos = [
        {"id": 1, "nombre": "Manzanas Golden", "precio": 2.50},
        {"id": 2, "nombre": "Naranjas Valencia", "precio": 3.00},
        {"id": 3, "nombre": "Plátanos de Canarias", "precio": 1.80},
        {"id": 4, "nombre": "Tomates", "precio": 2.20},
        {"id": 5, "nombre": "Lechugas", "precio": 1.50}
    ]

    # Buscar el producto con ese ID
    for producto in productos:
        if producto["id"] == producto_id:
            return producto

    # Si no existe, devolver error
    return {"error": "Producto no encontrado"}


# Lista temporal para almacenar pedidos (más adelante será base de datos)
pedidos_db = []


# Modelo para los items del pedido
class ItemPedido(BaseModel):
    producto_id: int
    nombre: str
    precio: float
    cantidad: int
    unidad: str


# Modelo para el pedido completo
class Pedido(BaseModel):
    id: Optional[int] = None
    items: List[ItemPedido]
    total: float
    fecha: Optional[str] = None
    estado: str = "pendiente"
    cliente_nombre: Optional[str] = None
    cliente_email: Optional[str] = None
    cliente_telefono: Optional[str] = None
    direccion_entrega: Optional[str] = None


# Endpoint para crear un nuevo pedido
@app.post("/api/pedidos", response_model=Pedido)
def crear_pedido(pedido: Pedido):
    # Generar ID automático
    pedido.id = len(pedidos_db) + 1

    # Añadir fecha actual
    pedido.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Guardar en la "base de datos" temporal
    pedidos_db.append(pedido.model_dump())

    return pedido


# Endpoint para obtener todos los pedidos
@app.get("/api/pedidos")
def obtener_pedidos():
    return pedidos_db


# Endpoint para obtener un pedido específico
@app.get("/api/pedidos/{pedido_id}")
def obtener_pedido(pedido_id: int):
    for pedido in pedidos_db:
        if pedido["id"] == pedido_id:
            return pedido
    return {"error": "Pedido no encontrado"}


handler = app