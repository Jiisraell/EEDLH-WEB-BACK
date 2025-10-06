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
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, status
import secrets
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar seguridad para admin
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
SECRET_KEY = os.environ.get("SECRET_KEY", "clave-super-secreta-cambiar-en-produccion")


def verificar_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """Verificar credenciales de admin"""
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# Crear la aplicación
app = FastAPI(title="El Encanto de la Huerta API")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/admin")
async def admin_panel():
    return FileResponse("static/admin.html")


# Configurar Resend con manejo de errores
resend_api_key = os.environ.get("RESEND_API_KEY")
if not resend_api_key:
    logger.warning("⚠️ RESEND_API_KEY no configurada. Los emails no se enviarán.")
else:
    resend.api_key = resend_api_key
    logger.info("✅ Resend API configurada correctamente")

# Configurar MongoDB con manejo de errores
pedidos_en_memoria = []

# Desactivar MongoDB completamente para evitar problemas
usar_mongodb = False
logger.info("✅ Usando almacenamiento en MEMORIA (perfecto para portfolio)")

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
        "version": "2.2",
        "database": "MongoDB Atlas" if usar_mongodb else "Memoria",
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
                "unidad": "ud",
                "imagen": "img/lechuga_icebrg.jpg",
                "descripcion": "Lechugas frescas de la huerta"
            },
            {
                "id": 18,
                "nombre": "Lechuga Corazones",
                "categoria": "verduras",
                "precio": 1.00,
                "stock": 90,
                "unidad": "ud",
                "imagen": "img/corazon_lechuga.jpg",
                "descripcion": "Corazones de lechuga tiernos"
            },
            {
                "id": 19,
                "nombre": "Lechuga Hoja de Roble",
                "categoria": "verduras",
                "precio": 2.20,
                "stock": 90,
                "unidad": "ud",
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
                "precio": 2.25,
                "stock": 45,
                "unidad": "ud",
                "imagen": "img/aguacate.webp",
                "descripcion": "Aguacates cremosos perfectos para ensaladas"
            },
            {
                "id": 22,
                "nombre": "Pimiento Verde",
                "categoria": "verduras",
                "precio": 1.10,
                "stock": 80,
                "unidad": "ud",
                "imagen": "img/pimiento_verde.jpg",
                "descripcion": "Pimientos verdes de la huerta"
            },
            {
                "id": 23,
                "nombre": "Pimiento Rojo",
                "categoria": "verduras",
                "precio": 1.10,
                "stock": 80,
                "unidad": "ud",
                "imagen": "img/pimiento_rojo.jpg",
                "descripcion": "Pimientos rojos de la huerta"
            },
            {
                "id": 24,
                "nombre": "Pimiento Amarillo",
                "categoria": "verduras",
                "precio": 1.85,
                "stock": 80,
                "unidad": "ud",
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
                "nombre": "Sandías (7kg aprx)",
                "categoria": "frutas",
                "precio": 1.25,
                "stock": 30,
                "unidad": "kg",
                "imagen": "img/sandia.jpg",
                "descripcion": "Sandías jugosas y refrescantes"
            },
            {
                "id": 27,
                "nombre": "Melón bollo (5kg aprx)",
                "categoria": "frutas",
                "precio": 4.25,
                "stock": 30,
                "unidad": "kg",
                "imagen": "img/bollo_bodega.jpeg",
                "descripcion": "Melones tan dulces como el algodón de azúcar"
            },
            {
                "id": 28,
                "nombre": "Melón Terreno (5kg aprx)",
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
        v = v.strip().replace(' ', '').replace('-', '').replace('+', '')
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
        if usar_mongodb:
            try:
                ultimo_pedido = pedidos_collection.find_one(sort=[("id", -1)])
                nuevo_id = 1 if not ultimo_pedido else ultimo_pedido["id"] + 1
            except Exception as e:
                logger.warning(f"⚠️ MongoDB no disponible para generar ID: {e}. Usando ID de memoria")
                nuevo_id = len(pedidos_en_memoria) + 1
        else:
            nuevo_id = len(pedidos_en_memoria) + 1

        pedido.id = nuevo_id
        pedido.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Convertir el pedido a diccionario ANTES de guardarlo
        pedido_dict = {
            "id": pedido.id,
            "items": [
                {
                    "producto_id": item.producto_id,
                    "nombre": item.nombre,
                    "precio": item.precio,
                    "cantidad": item.cantidad,
                    "unidad": item.unidad
                }
                for item in pedido.items
            ],
            "total": pedido.total,
            "fecha": pedido.fecha,
            "estado": pedido.estado,
            "cliente_nombre": pedido.cliente_nombre,
            "cliente_email": pedido.cliente_email,
            "cliente_telefono": pedido.cliente_telefono,
            "direccion_entrega": pedido.direccion_entrega
        }

        # Intentar guardar en MongoDB
        if usar_mongodb:
            try:
                result = pedidos_collection.insert_one(pedido_dict.copy())
                logger.info(f"✅ Pedido #{nuevo_id} guardado en MongoDB con _id: {result.inserted_id}")
            except Exception as e:
                logger.error(f"⚠️ No se pudo guardar en MongoDB: {e}. Guardando en memoria.")
                pedidos_en_memoria.append(pedido_dict)
        else:
            pedidos_en_memoria.append(pedido_dict)
            logger.info(f"✅ Pedido #{nuevo_id} guardado en memoria")

        # Enviar email
        email_enviado = enviar_email_pedido(pedido)
        if not email_enviado:
            logger.warning(f"⚠️ Email no enviado para pedido #{nuevo_id}")

        return {
            **pedido_dict,
            "mensaje": "Pedido creado exitosamente",
            "email_enviado": email_enviado,
            "almacenamiento": "mongodb" if usar_mongodb else "memoria"
        }

    except ValueError as e:
        logger.error(f"❌ Error de validación: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error creando pedido: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error al crear el pedido.")


# Función auxiliar para convertir ObjectId a string
def convertir_objectid(pedidos):
    """Convierte ObjectId a string en todos los pedidos"""
    pedidos_limpios = []
    for pedido in pedidos:
        pedido_limpio = {}
        for key, value in pedido.items():
            if key == "_id":
                continue  # Omitir el _id
            elif isinstance(value, ObjectId):
                pedido_limpio[key] = str(value)
            elif isinstance(value, list):
                pedido_limpio[key] = [
                    {k: str(v) if isinstance(v, ObjectId) else v for k, v in item.items()}
                    if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                pedido_limpio[key] = value
        pedidos_limpios.append(pedido_limpio)
    return pedidos_limpios


# Endpoint para obtener todos los pedidos
@app.get("/api/pedidos")
def obtener_pedidos():
    try:
        if usar_mongodb:
            try:
                pedidos_raw = list(pedidos_collection.find())
                logger.info(f"📊 Pedidos encontrados en MongoDB: {len(pedidos_raw)}")

                if len(pedidos_raw) > 0:
                    logger.info(f"📋 Ejemplo de pedido: {pedidos_raw[0]}")

                pedidos_limpios = convertir_objectid(pedidos_raw)
                logger.info(f"✅ {len(pedidos_limpios)} pedidos procesados de MongoDB")
                return pedidos_limpios
            except Exception as e:
                logger.error(f"⚠️ Error en MongoDB: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                logger.warning("⚠️ Usando pedidos de memoria")
                return pedidos_en_memoria
        else:
            logger.info(f"✅ Devolviendo {len(pedidos_en_memoria)} pedidos de memoria")
            return pedidos_en_memoria
    except Exception as e:
        logger.error(f"❌ Error obteniendo pedidos: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []


# Health check endpoint
@app.get("/health")
def health_check():
    try:
        client.server_info()
        mongodb_status = "ok"
    except:
        mongodb_status = "error"

    return {
        "status": "ok" if mongodb_status == "ok" else "degraded",
        "mongodb": mongodb_status,
        "resend": "ok" if resend_api_key else "not_configured"
    }


# ===== ENDPOINTS DE ADMINISTRACIÓN =====

@app.post("/api/admin/login")
def admin_login(credentials: HTTPBasicCredentials = Depends(security)):
    """Login de administrador"""
    try:
        admin = verificar_admin(credentials)
        return {
            "mensaje": "Login exitoso",
            "usuario": admin,
            "token": "authenticated"
        }
    except HTTPException as e:
        raise e


# Modelo para cambio de estado
class CambioEstado(BaseModel):
    nuevo_estado: str


@app.put("/api/admin/pedidos/{pedido_id}/estado")
def cambiar_estado_pedido(
        pedido_id: int,
        cambio: CambioEstado,
        admin: str = Depends(verificar_admin)
):
    """Cambiar estado de un pedido (solo admin)"""
    try:
        estados_validos = ["pendiente", "en_preparacion", "enviado", "entregado", "cancelado"]

        if cambio.nuevo_estado not in estados_validos:
            raise HTTPException(
                status_code=400,
                detail=f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}"
            )

        if usar_mongodb:
            try:
                result = pedidos_collection.update_one(
                    {"id": pedido_id},
                    {"$set": {"estado": cambio.nuevo_estado}}
                )
                if result.modified_count == 0:
                    raise HTTPException(status_code=404, detail="Pedido no encontrado")
                logger.info(f"✅ Pedido #{pedido_id} actualizado a '{cambio.nuevo_estado}' por {admin}")
            except Exception as e:
                for pedido in pedidos_en_memoria:
                    if pedido.get("id") == pedido_id:
                        pedido["estado"] = cambio.nuevo_estado
                        logger.info(f"✅ Pedido #{pedido_id} actualizado en memoria")
                        return {"mensaje": "Estado actualizado", "pedido_id": pedido_id,
                                "nuevo_estado": cambio.nuevo_estado}
                raise HTTPException(status_code=404, detail="Pedido no encontrado")
        else:
            for pedido in pedidos_en_memoria:
                if pedido.get("id") == pedido_id:
                    pedido["estado"] = cambio.nuevo_estado
                    logger.info(f"✅ Pedido #{pedido_id} actualizado en memoria")
                    return {"mensaje": "Estado actualizado", "pedido_id": pedido_id,
                            "nuevo_estado": cambio.nuevo_estado}
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        return {
            "mensaje": "Estado actualizado exitosamente",
            "pedido_id": pedido_id,
            "nuevo_estado": cambio.nuevo_estado
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error actualizando pedido: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el pedido")


@app.get("/api/admin/pedidos")
def obtener_pedidos_admin(admin: str = Depends(verificar_admin)):
    """Obtener todos los pedidos (solo admin)"""
    return obtener_pedidos()


@app.get("/api/admin/estadisticas")
def obtener_estadisticas(admin: str = Depends(verificar_admin)):
    """Obtener estadísticas de pedidos"""
    try:
        if usar_mongodb:
            try:
                pedidos = list(pedidos_collection.find())
                pedidos = convertir_objectid(pedidos)
            except:
                pedidos = pedidos_en_memoria
        else:
            pedidos = pedidos_en_memoria

        total_pedidos = len(pedidos)
        total_ingresos = sum(p.get("total", 0) for p in pedidos)

        estados = {}
        for pedido in pedidos:
            estado = pedido.get("estado", "pendiente")
            estados[estado] = estados.get(estado, 0) + 1

        return {
            "total_pedidos": total_pedidos,
            "total_ingresos": round(total_ingresos, 2),
            "pedidos_por_estado": estados,
            "pedido_promedio": round(total_ingresos / total_pedidos, 2) if total_pedidos > 0 else 0
        }
    except Exception as e:
        logger.error(f"❌ Error obteniendo estadísticas: {e}")
        return {
            "total_pedidos": 0,
            "total_ingresos": 0,
            "pedidos_por_estado": {},
            "pedido_promedio": 0
        }


handler = app