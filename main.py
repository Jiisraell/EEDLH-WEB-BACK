# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# Crear la aplicación
app = FastAPI(title="El Encanto de la Huerta API")

# ===== CONFIGURAR CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ruta principal
@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de El Encanto de la Huerta",
        "version": "1.0",
        "endpoints": ["/productos", "/docs"]
    }


# Ruta para obtener productos CON IMÁGENES
@app.get("/productos")
def obtener_productos():
    productos = [
        {
            "id": 1,
            "nombre": "Manzanas Golden",
            "categoria": "frutas",
            "precio": 2.25,
            "stock": 100,
            "unidad": "kg",
            "imagen": "img/golden.webp",  # Añadir imágenes
            "descripcion": "Manzanas dulces y crujientes de temporada"
        },
        {
            "id": 2,
            "nombre": "Manzanas Pink Lady",
            "categoria": "frutas",
            "precio": 3.75,
            "stock": 100,
            "unidad": "kg",
            "imagen": "img/pink_lady.webp",  # Añadir imágenes
            "descripcion": "Manzanas dulces y crujientes de temporada"
        },
        {
            "id": 3,
            "nombre": "Manzanas Reineta",
            "categoria": "frutas",
            "precio": 2.95,
            "stock": 100,
            "unidad": "kg",
            "imagen": "img/manzana_reineta.webp",  # Añadir imágenes
            "descripcion": "Manzanas dulces y crujientes de temporada"
        },
        {
            "id": 4,
            "nombre": "Manzanas Ambrosia",
            "categoria": "frutas",
            "precio": 3.75,
            "stock": 100,
            "unidad": "kg",
            "imagen": "img/ambrosia.webp",  # Añadir imágenes
            "descripcion": "Manzanas dulces y crujientes de temporada"
        },
        {
            "id": 5,
            "nombre": "Manzanas Granny Smith",
            "categoria": "frutas",
            "precio": 2.85,
            "stock": 100,
            "unidad": "kg",
            "imagen": "img/granny_smit.webp",  # Añadir imágenes
            "descripcion": "Manzanas dulces y crujientes de temporada"
        },
        {
            "id": 6,
            "nombre": "Naranjas Mutxamel",
            "categoria": "frutas",
            "precio": 2.25,
            "stock": 200,
            "unidad": "kg",
            "imagen": "img/naranja_mesa.jpeg",
            "descripcion": "Naranjas de Mutxamel jugosas, perfectas para zumo"
        },
        {
            "id": 7,
            "nombre": "Naranja Zumo",
            "categoria": "frutas",
            "precio": 1.65,
            "stock": 100,
            "unidad": "kg",
            "imagen": "img/naranja_zumo.jpg",  # Añadir imágenes
            "descripcion": "Naranjas dulces y con mucho zumo de temporada"
        },
        {
            "id": 8,
            "nombre": "Plátanos de Canarias",
            "categoria": "frutas",
            "precio": 1.80,
            "stock": 120,
            "unidad": "kg",
            "imagen": "img/Platano.jpg",
            "descripcion": "Plátanos de Canarias maduros y dulces"
        },
        {
            "id": 9,
            "nombre": "Tomates Pera",
            "categoria": "verduras",
            "precio": 2.25,
            "stock": 90,
            "unidad": "kg",
            "imagen": "img/tomate_pera.jpg",
            "descripcion": "Tomates frescos de la huerta"
        },
        {
            "id": 10,
            "nombre": "Tomates Rama",
            "categoria": "verduras",
            "precio": 2.25,
            "stock": 90,
            "unidad": "kg",
            "imagen": "img/tomate_rama.png",
            "descripcion": "Tomates frescos de la huerta"
        },
        {
            "id": 11,
            "nombre": "Tomates Daniela",
            "categoria": "verduras",
            "precio": 2.25,
            "stock": 90,
            "unidad": "kg",
            "imagen": "img/tomate_Daniela.jpg",
            "descripcion": "Tomates frescos de la huerta"
        },
        {
            "id": 12,
            "nombre": "Tomates Raff",
            "categoria": "verduras",
            "precio": 8.95,
            "stock": 90,
            "unidad": "kg",
            "imagen": "img/tomate_raf.webp",
            "descripcion": "Tomates frescos de la huerta"
        },
        {
            "id": 13,
            "nombre": "Tomate Azul",
            "categoria": "verduras",
            "precio": 6.75,
            "stock": 90,
            "unidad": "kg",
            "imagen": "img/Tomate-azul.jpg",
            "descripcion": "Tomates frescos de la huerta"
        },
        {
            "id": 14,
            "nombre": "Tomate Rosa",
            "categoria": "verduras",
            "precio": 4.85,
            "stock": 90,
            "unidad": "kg",
            "imagen": "img/tomate_rosa.webp",
            "descripcion": "Tomates frescos de la huerta"
        },
        {
            "id": 15,
            "nombre": "Tomate Mutxamel",
            "categoria": "verduras",
            "precio": 2.65,
            "stock": 90,
            "unidad": "kg",
            "imagen": "img/tomate_mtx.webp",
            "descripcion": "Tomates frescos de la huerta"
        },
        {
            "id": 16,
            "nombre": "Lechuga Romana",
            "categoria": "verduras",
            "precio": 1.50,
            "stock": 73,
            "unidad": "ud",
            "imagen": "img/lechuga_romana.jpg",
            "descripcion": "Lechugas frescas recién cosechadas"
        },{
            "id": 17,
            "nombre": "Lechuga Iceberg",
            "categoria": "verduras",
            "precio": 1.35,
            "stock": 90,
            "unidad": "kg",
            "imagen": "img/lechuga_icebrg.jpg",
            "descripcion": "Tomates frescos de la huerta"
        },
        {
            "id": 18,
            "nombre": "Lechuga Corazones",
            "categoria": "verduras",
            "precio": 1,
            "stock": 90,
            "unidad": "kg",
            "imagen": "img/corazon_lechuga.jpg",
            "descripcion": "Tomates frescos de la huerta"
        },
        {
            "id": 19,
            "nombre": "Lechuga Hoja de Roble",
            "categoria": "verduras",
            "precio": 2.20,
            "stock": 90,
            "unidad": "kg",
            "imagen": "img/lechuga_roble.jpg",
            "descripcion": "Tomates frescos de la huerta"
        },

        {
            "id": 20,
            "nombre": "Fresas",
            "categoria": "frutas",
            "precio": 7.25,
            "stock": 60,
            "unidad": "kg",
            "imagen": "img/fresas.jpg",
            "descripcion": "Fresas dulces y aromáticas de temporada"
        },
        {
            "id": 21,
            "nombre": "Aguacates",
            "categoria": "frutas",
            "precio": 4.20,
            "stock": 45,
            "unidad": "kg",
            "imagen": "img/aguacate.webp",
            "descripcion": "Aguacates cremosos perfectos para ensaladas"
        },
        {
            "id": 22,
            "nombre": "Pimiento Verde",
            "categoria": "verduras",
            "precio": 2.85,
            "stock": 80,
            "unidad": "kg",
            "imagen": "img/pimiento_verde.jpg",
            "descripcion": "Pimientos rojos y verdes de la huerta"
        },
        {
            "id": 23,
            "nombre": "Pimiento Rojo",
            "categoria": "verduras",
            "precio": 3.25,
            "stock": 80,
            "unidad": "kg",
            "imagen": "img/pimiento_rojo.jpg",
            "descripcion": "Pimientos rojos y verdes de la huerta"
        },
        {
            "id": 24,
            "nombre": "Pimiento Amarillo",
            "categoria": "verduras",
            "precio": 2.80,
            "stock": 80,
            "unidad": "kg",
            "imagen": "img/pimiento_amarillo.jpg",
            "descripcion": "Pimientos rojos y verdes de la huerta"
        },
        {
            "id": 25,
            "nombre": "Zanahorias",
            "categoria": "verduras",
            "precio": 1.60,
            "stock": 150,
            "unidad": "kg",
            "imagen": "img/zanahorias.jpg",
            "descripcion": "Zanahorias frescas y crujientes"
        },
        {
            "id": 26,
            "nombre": "Sandías",
            "categoria": "frutas",
            "precio": 1.25,
            "stock": 30,
            "unidad": "kg",
            "imagen": "img/Sandía.avif",
            "descripcion": "Sandías jugosas y refrescantes"
        },
        {
            "id": 27,
            "nombre": "Melón bollo",
            "categoria": "frutas",
            "precio": 4.25,
            "stock": 30,
            "unidad": "kg",
            "imagen": "img/bollo_bodega.jpeg",
            "descripcion": "Melones tan dulces como el algodón de azúcar"
        },
        {
            "id": 28,
            "nombre": "Melón Terreno",
            "categoria": "frutas",
            "precio": 2.50,
            "stock": 30,
            "unidad": "kg",
            "imagen": "img/melon.png",
            "descripcion": "Melón de cercanía, refrescante y crujiente"
        },

    ]
    return productos


# Ruta para obtener UN producto específico
@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    productos = obtener_productos()

    for producto in productos:
        if producto["id"] == producto_id:
            return producto

    return {"error": "Producto no encontrado"}


# Lista temporal para almacenar pedidos
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
    pedido.id = len(pedidos_db) + 1
    pedido.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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