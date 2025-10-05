# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator
import resend
import os
from pymongo import MongoClient
from bson import ObjectId
import logging
from dotenv import load_dotenv


# Cargar variables de entorno desde .env
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Crear la aplicación
app = FastAPI(title="El Encanto de la Huerta API")

# Configurar Resend con manejo de errores
resend_api_key = os.environ.get("RESEND_API_KEY")
if not resend_api_key:
    logger.warning("⚠️ RESEND_API_KEY no configurada. Los emails no se enviarán.")
else:
    resend.api_key = resend_api_key
    logger.info("✅ Resend API configurada correctamente")

# Configurar MongoDB con manejo de errores
MONGODB_URL = os.environ.get("MONGODB_URL")
if not MONGODB_URL:
    logger.error("❌ MONGODB_URL no configurada. La aplicación no funcionará correctamente.")
    raise ValueError("MONGODB_URL es requerida")

try:
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    # Verificar conexión
    client.server_info()
    db = client.eedlh_database
    pedidos_collection = db.pedidos
    logger.info("✅ Conexión a MongoDB exitosa")
except Exception as e:
    logger.error(f"❌ Error conectando a MongoDB: {e}")
    raise

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
        "version": "2.1",
        "database": "MongoDB Atlas",
        "endpoints": ["/productos", "/api/pedidos", "/docs"],
        "status": "online"
    }


# Ruta para obtener productos
@app.get("/productos")
def obtener_productos():
    try:
        productos = [
            {
                "id": 1,
                "nombre": "Manzanas Golden",
                "categoria": "frutas",
                "precio": 2.25,
                "stock": 100,
                "unidad": "kg",
                "imagen": "img/golden.webp",
                "descripcion": "Manzanas dulces y crujientes de temporada"
            },
            {
                "id": 2,
                "nombre": "Manzanas Pink Lady",
                "categoria": "frutas",
                "precio": 3.75,
                "stock": 100,
                "unidad": "kg",
                "imagen": "img/pink_lady.webp",
                "descripcion": "Manzanas dulces y crujientes de temporada"
            },
            {
                "id": 3,
                "nombre": "Manzanas Reineta",
                "categoria": "frutas",
                "precio": 2.95,
                "stock": 100,
                "unidad": "kg",
                "imagen": "img/manzana_reineta.webp",
                "descripcion": "Manzanas dulces y crujientes de temporada"
            },
            {
                "id": 4,
                "nombre": "Manzanas Ambrosia",
                "categoria": "frutas",
                "precio": 3.75,
                "stock": 100,
                "unidad": "kg",
                "imagen": "img/ambrosia.webp",
                "descripcion": "Manzanas dulces y crujientes de temporada"
            },
            {
                "id": 5,
                "nombre": "Manzanas Granny Smith",
                "categoria": "frutas",
                "precio": 2.85,
                "stock": 100,
                "unidad": "kg",
                "imagen": "img/granny_smit.webp",
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
                "imagen": "img/naranja_zumo.jpg",
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
            },
            {
                "id": 17,
                "nombre": "Lechuga Iceberg",
                "categoria": "verduras",
                "precio": 1.35,
                "stock": 90,
                "unidad": "kg",
                "imagen": "img/lechuga_icebrg.jpg",
                "descripcion": "Lechugas frescas de la huerta"
            },
            {
                "id": 18,
                "nombre": "Lechuga Corazones",
                "categoria": "verduras",
                "precio": 1.00,
                "stock": 90,
                "unidad": "kg",
                "imagen": "img/corazon_lechuga.jpg",
                "descripcion": "Corazones de lechuga tiernos"
            },
            {
                "id": 19,
                "nombre": "Lechuga Hoja de Roble",
                "categoria": "verduras",
                "precio": 2.20,
                "stock": 90,
                "unidad": "kg",
                "imagen": "img/lechuga_roble.jpg",
                "descripcion": "Lechuga hoja de roble fresca"
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
                "descripcion": "Pimientos verdes de la huerta"
            },
            {
                "id": 23,
                "nombre": "Pimiento Rojo",
                "categoria": "verduras",
                "precio": 3.25,
                "stock": 80,
                "unidad": "kg",
                "imagen": "img/pimiento_rojo.jpg",
                "descripcion": "Pimientos rojos de la huerta"
            },
            {
                "id": 24,
                "nombre": "Pimiento Amarillo",
                "categoria": "verduras",
                "precio": 2.80,
                "stock": 80,
                "unidad": "kg",
                "imagen": "img/pimiento_amarillo.jpg",
                "descripcion": "Pimientos amarillos de la huerta"
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
                "imagen": "img/sandia.jpg",
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
        logger.info(f"✅ Productos obtenidos: {len(productos)}")
        return productos
    except Exception as e:
        logger.error(f"❌ Error obteniendo productos: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener productos")


# Ruta para obtener UN producto específico
@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    try:
        productos = obtener_productos()
        for producto in productos:
            if producto["id"] == producto_id:
                logger.info(f"✅ Producto {producto_id} encontrado")
                return producto

        logger.warning(f"⚠️ Producto {producto_id} no encontrado")
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error obteniendo producto {producto_id}: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener el producto")


# Modelo para los items del pedido
class ItemPedido(BaseModel):
    producto_id: int
    nombre: str
    precio: float
    cantidad: int
    unidad: str

    @validator('cantidad')
    def validar_cantidad(cls, v):
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        if v > 1000:
            raise ValueError('La cantidad máxima es 1000')
        return v

    @validator('precio')
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v


# Modelo para el pedido completo con validaciones mejoradas
class Pedido(BaseModel):
    id: Optional[int] = None
    items: List[ItemPedido]
    total: float
    fecha: Optional[str] = None
    estado: str = "pendiente"
    cliente_nombre: str
    cliente_email: EmailStr
    cliente_telefono: str
    direccion_entrega: str

    @validator('cliente_nombre')
    def validar_nombre(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError('El nombre debe tener al menos 3 caracteres')
        if len(v) > 100:
            raise ValueError('El nombre es demasiado largo')
        return v

    @validator('cliente_telefono')
    def validar_telefono(cls, v):
        # Eliminar espacios y caracteres especiales
        v = v.strip().replace(' ', '').replace('-', '').replace('+', '')

        # Validar que tenga entre 9 y 15 dígitos
        if not v.isdigit():
            raise ValueError('El teléfono debe contener solo números')
        if len(v) < 9 or len(v) > 15:
            raise ValueError('El teléfono debe tener entre 9 y 15 dígitos')
        return v

    @validator('direccion_entrega')
    def validar_direccion(cls, v):
        v = v.strip()
        if len(v) < 10:
            raise ValueError('La dirección debe tener al menos 10 caracteres')
        if len(v) > 500:
            raise ValueError('La dirección es demasiado larga')
        return v

    @validator('items')
    def validar_items(cls, v):
        if not v or len(v) == 0:
            raise ValueError('El pedido debe tener al menos un producto')
        if len(v) > 100:
            raise ValueError('El pedido no puede tener más de 100 productos')
        return v

    @validator('total')
    def validar_total(cls, v):
        if v <= 0:
            raise ValueError('El total debe ser mayor a 0')
        if v > 10000:
            raise ValueError('El total máximo es 10000€')
        return v


# Función para enviar email con manejo de errores
def enviar_email_pedido(pedido: Pedido):
    if not resend_api_key:
        logger.warning("⚠️ Email no enviado: RESEND_API_KEY no configurada")
        return False

    try:
        items_html = ""
        for item in pedido.items:
            subtotal = item.precio * item.cantidad
            items_html += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">{item.nombre}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">{item.cantidad}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: right;">{item.precio:.2f}€/{item.unidad}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: right;">{subtotal:.2f}€</td>
            </tr>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0b3d0b; border-bottom: 2px solid #0b3d0b; padding-bottom: 10px;">
                    🛒 Nuevo Pedido #{pedido.id}
                </h2>

                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #0b3d0b;">Datos del Cliente</h3>
                    <p><strong>Nombre:</strong> {pedido.cliente_nombre}</p>
                    <p><strong>Email:</strong> {pedido.cliente_email}</p>
                    <p><strong>Teléfono:</strong> {pedido.cliente_telefono}</p>
                    <p><strong>Dirección:</strong> {pedido.direccion_entrega}</p>
                </div>

                <h3 style="color: #0b3d0b;">Productos del Pedido</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background-color: #0b3d0b; color: white;">
                            <th style="padding: 10px; text-align: left;">Producto</th>
                            <th style="padding: 10px; text-align: center;">Cantidad</th>
                            <th style="padding: 10px; text-align: right;">Precio</th>
                            <th style="padding: 10px; text-align: right;">Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_html}
                    </tbody>
                </table>

                <div style="text-align: right; margin-top: 20px; padding: 15px; background-color: #e6f1e6; border-radius: 5px;">
                    <h3 style="margin: 0; color: #0b3d0b;">TOTAL: {pedido.total:.2f}€</h3>
                </div>

                <div style="margin-top: 30px; padding: 15px; background-color: #fff3cd; border-left: 4px solid #ffc107;">
                    <p style="margin: 0;"><strong>Fecha del pedido:</strong> {pedido.fecha}</p>
                    <p style="margin: 5px 0 0 0;"><strong>Estado:</strong> {pedido.estado}</p>
                </div>
            </div>
        </body>
        </html>
        """

        params = {
            "from": "El Encanto de la Huerta <onboarding@resend.dev>",
            "to": ["elencantodelahuertaa@gmail.com"],
            "subject": f"Nuevo Pedido #{pedido.id} - {pedido.cliente_nombre}",
            "html": html_content,
        }

        resend.Emails.send(params)
        logger.info(f"✅ Email enviado correctamente para pedido #{pedido.id}")
        return True

    except Exception as e:
        logger.error(f"❌ Error enviando email para pedido #{pedido.id}: {e}")
        return False


# Endpoint para crear un nuevo pedido con mejor manejo de errores
@app.post("/api/pedidos")
def crear_pedido(pedido: Pedido):
    try:
        # Obtener el último ID de pedido
        ultimo_pedido = pedidos_collection.find_one(sort=[("id", -1)])
        nuevo_id = 1 if not ultimo_pedido else ultimo_pedido["id"] + 1

        pedido.id = nuevo_id
        pedido.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar en MongoDB
        pedido_dict = pedido.model_dump()
        result = pedidos_collection.insert_one(pedido_dict)

        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Error al guardar el pedido en la base de datos")

        logger.info(f"✅ Pedido #{nuevo_id} creado exitosamente")

        # Enviar email de notificación (no bloqueante)
        email_enviado = enviar_email_pedido(pedido)
        if not email_enviado:
            logger.warning(f"⚠️ Email no enviado para pedido #{nuevo_id}")

        return {
            **pedido_dict,
            "mensaje": "Pedido creado exitosamente",
            "email_enviado": email_enviado
        }

    except ValueError as e:
        logger.error(f"❌ Error de validación: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error creando pedido: {e}")
        raise HTTPException(status_code=500, detail="Error al crear el pedido. Por favor, inténtalo de nuevo.")


# Endpoint para obtener todos los pedidos
@app.get("/api/pedidos")
def obtener_pedidos():
    try:
        pedidos = list(pedidos_collection.find({}, {"_id": 0}))
        logger.info(f"✅ {len(pedidos)} pedidos obtenidos")
        return pedidos
    except Exception as e:
        logger.error(f"❌ Error obteniendo pedidos: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener los pedidos")


# Endpoint para obtener un pedido específico
@app.get("/api/pedidos/{pedido_id}")
def obtener_pedido(pedido_id: int):
    try:
        pedido = pedidos_collection.find_one({"id": pedido_id}, {"_id": 0})
        if pedido:
            logger.info(f"✅ Pedido {pedido_id} encontrado")
            return pedido

        logger.warning(f"⚠️ Pedido {pedido_id} no encontrado")
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error obteniendo pedido {pedido_id}: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener el pedido")


# Health check endpoint
@app.get("/health")
def health_check():
    try:
        # Verificar MongoDB
        client.server_info()
        mongodb_status = "ok"
    except:
        mongodb_status = "error"

    return {
        "status": "ok" if mongodb_status == "ok" else "degraded",
        "mongodb": mongodb_status,
        "resend": "ok" if resend_api_key else "not_configured"
    }


handler = app