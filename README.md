# 🍎 El Encanto de la Huerta - Backend API

API REST desarrollada con FastAPI para gestionar pedidos, productos y administración online de mi propia tienda de frutas y verduras (la tuve antes de decidirme por la programación).


## 🚀 Demo en Vivo

- **API Backend**: [https://eedlh-web-back.onrender.com](https://eedlh-web-back.onrender.com)
- **Documentación Interactiva**: [https://eedlh-web-back.onrender.com/docs](https://eedlh-web-back.onrender.com/docs)
- **Panel Admin**: [https://eedlh-web-back.onrender.com/admin](https://eedlh-web-back.onrender.com/admin)
- **Frontend**: [https://jiisraell.github.io/EEDLH-Web/](https://jiisraell.github.io/EEDLH-Web/)

## ✨ Características

### 🛒 Sistema de Pedidos
- ✅ Creación de pedidos con validación completa de datos
- ✅ Gestión de items con cantidades y precios
- ✅ Cálculo automático de totales
- ✅ Almacenamiento en memoria (ideal para portfolio/demo)
- ✅ Notificaciones por email con Resend

### 🔐 Panel de Administración
- ✅ Autenticación con HTTP Basic Auth
- ✅ Cambio de estado de pedidos (pendiente → en preparación → enviado → entregado)
- ✅ Edición de precios (ajuste por peso real)
- ✅ Estadísticas en tiempo real
- ✅ Filtros y búsqueda de pedidos

### 📦 Gestión de Productos
- ✅ Catálogo completo con 28 productos
- ✅ Información detallada (nombre, categoría, precio, stock, imagen)
- ✅ Separación por categorías (frutas/verduras)
- ✅ API RESTful para consultas

### 🎯 Validaciones Robustas
- ✅ Validación de emails con Pydantic
- ✅ Validación de teléfonos (9-15 dígitos)
- ✅ Validación de nombres y direcciones
- ✅ Validación de cantidades y precios
- ✅ Límites de seguridad (máximo 100 productos por pedido, total máximo 10000€)

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| **FastAPI** | Framework web moderno y rápido |
| **Pydantic** | Validación de datos y serialización |
| **Resend** | Envío de emails transaccionales |
| **Passlib + Bcrypt** | Hashing y seguridad de contraseñas |
| **Python-dotenv** | Gestión de variables de entorno |
| **Uvicorn** | Servidor ASGI de alto rendimiento |

## 📋 Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Cuenta en [Resend](https://resend.com) para envío de emails (opcional)

## 🔧 Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/jiisraell/EEDLH-WEB-BACK.git
cd EEDLH-WEB-BACK
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Resend API Key (opcional, para envío de emails)
RESEND_API_KEY=re_tu_clave_api_aqui

# Credenciales de administrador
ADMIN_USERNAME=admin
ADMIN_PASSWORD=tu_password_seguro
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura

# Configuración (opcional)
PORT=8000
ENVIRONMENT=development
```

### 5. Ejecutar el servidor

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación de la API

### Endpoints Principales

#### Productos

```http
GET /productos
```
Obtiene la lista completa de productos disponibles.

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Manzanas Golden",
    "categoria": "frutas",
    "precio": 2.25,
    "stock": 100,
    "unidad": "kg",
    "imagen": "img/golden.webp",
    "descripcion": "Manzanas dulces y crujientes de temporada"
  }
]
```

---

```http
GET /productos/{producto_id}
```
Obtiene un producto específico por su ID.

---

#### Pedidos

```http
POST /api/pedidos
```
Crea un nuevo pedido.

**Body:**
```json
{
  "items": [
    {
      "producto_id": 1,
      "nombre": "Manzanas Golden",
      "precio": 2.25,
      "cantidad": 3,
      "unidad": "kg"
    }
  ],
  "total": 6.75,
  "cliente_nombre": "Juan Pérez",
  "cliente_email": "juan@example.com",
  "cliente_telefono": "612345678",
  "direccion_entrega": "Calle Ejemplo 123, Santa Pola"
}
```

**Respuesta:**
```json
{
  "id": 1,
  "items": [...],
  "total": 6.75,
  "fecha": "2025-10-07 14:30:00",
  "estado": "pendiente",
  "cliente_nombre": "Juan Pérez",
  "mensaje": "Pedido creado exitosamente",
  "email_enviado": true,
  "almacenamiento": "memoria"
}
```

---

```http
GET /api/pedidos
```
Obtiene todos los pedidos (sin autenticación).

---

#### Administración (requiere autenticación)

```http
POST /api/admin/login
```
Login de administrador (HTTP Basic Auth).

**Headers:**
```
Authorization: Basic base64(username:password)
```

---

```http
GET /api/admin/pedidos
```
Obtiene todos los pedidos (endpoint protegido).

---

```http
PUT /api/admin/pedidos/{pedido_id}/estado
```
Cambia el estado de un pedido.

**Body:**
```json
{
  "nuevo_estado": "en_preparacion"
}
```

Estados válidos: `pendiente`, `en_preparacion`, `enviado`, `entregado`, `cancelado`

---

```http
PUT /api/admin/pedidos/{pedido_id}/precio
```
Ajusta el precio total de un pedido (útil para ajustar por peso real).

**Body:**
```json
{
  "nuevo_total": 25.50
}
```

---

```http
GET /api/admin/estadisticas
```
Obtiene estadísticas generales de los pedidos.

**Respuesta:**
```json
{
  "total_pedidos": 15,
  "total_ingresos": 342.50,
  "pedidos_por_estado": {
    "pendiente": 5,
    "en_preparacion": 3,
    "enviado": 4,
    "entregado": 3
  },
  "pedido_promedio": 22.83
}
```

---

#### Health Check

```http
GET /health
```
Verifica el estado de la API.

**Respuesta:**
```json
{
  "status": "ok",
  "database": "memoria",
  "pedidos_guardados": 15,
  "resend": "ok"
}
```

---

### Documentación Interactiva

FastAPI genera automáticamente documentación interactiva:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔒 Seguridad

### Autenticación
- **HTTP Basic Authentication** para endpoints de administración
- Comparación segura de credenciales con `secrets.compare_digest()`
- Hashing de contraseñas con bcrypt (preparado para futuras mejoras)

### Validaciones
- Validación exhaustiva con Pydantic
- Límites de longitud en strings
- Validación de formatos (email, teléfono)
- Sanitización de inputs

### CORS
- Configurado para aceptar requests del frontend
- Headers permitidos para comunicación cross-origin

## 📧 Configuración de Emails

La API envía notificaciones por email usando [Resend](https://resend.com).

### Obtener API Key de Resend:

1. Regístrate en [resend.com](https://resend.com)
2. Verifica tu dominio (o usa `onboarding@resend.dev` para pruebas)
3. Genera una API Key en el dashboard
4. Añádela al archivo `.env`

**Nota**: La API funciona perfectamente sin Resend configurado. Los pedidos se guardan de todas formas, solo no se enviarán emails.

## 🚀 Deploy en Render

### Configuración

1. Crea una cuenta en [Render](https://render.com)
2. Conecta tu repositorio de GitHub
3. Crea un nuevo **Web Service**
4. Configura las variables de entorno en el dashboard de Render

### Variables de Entorno en Render

```
RESEND_API_KEY=re_tu_clave_real
ADMIN_USERNAME=admin
ADMIN_PASSWORD=tu_password_seguro
SECRET_KEY=clave_secreta_produccion
```

### Configuración de Deploy

El archivo `render.yaml` ya está configurado:

```yaml
services:
  - type: web
    name: eedlh-web-back
    env: python
    buildCommand: pip install --upgrade pip && pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 📁 Estructura del Proyecto

```
EEDLH-WEB-BACK/
├── main.py                 # Aplicación principal FastAPI
├── requirements.txt        # Dependencias Python
├── runtime.txt            # Versión de Python
├── render.yaml            # Configuración de deploy
├── .env.example           # Ejemplo de variables de entorno
├── .gitignore             # Archivos ignorados por Git
├── static/                # Archivos estáticos
│   ├── admin.html         # Panel de administración
│   └── js/
│       └── admin.js       # Lógica del panel admin
└── README.md              # Este archivo
```

## 🎨 Integración con Frontend

### Configuración en el Frontend

En `js/tienda.js`:

```javascript
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000'
  : 'https://eedlh-web-back.onrender.com';
```

Esto permite que funcione tanto en desarrollo local como en producción.

## 📊 Base de Datos

**Actualmente**: Almacenamiento en memoria (ideal para portfolio/demo)

### Ventajas del almacenamiento en memoria:
- ✅ Sin configuración adicional
- ✅ Deploy simple y rápido
- ✅ Perfecto para demos y portfolio
- ✅ Cero costos de base de datos

### Migración futura a MongoDB (opcional):

Si deseas persistencia real, puedes migrar fácilmente a MongoDB:

```python
# Descomentar en main.py y añadir motor a requirements.txt
from motor.motor_asyncio import AsyncIOMotorClient

mongodb_url = os.environ.get("MONGODB_URL")
client = AsyncIOMotorClient(mongodb_url)
db = client.eedlh_database
```

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "Port already in use"
```bash
# Cambia el puerto
uvicorn main:app --reload --port 8001
```

### Los emails no se envían
- Verifica que `RESEND_API_KEY` esté configurada
- Revisa los logs para mensajes de error
- La API funciona sin emails, es opcional

### Error de CORS
- Verifica la configuración de `allow_origins` en `main.py`
- Asegúrate de que el frontend usa la URL correcta

## 📈 Mejoras Futuras

- [ ] Migración a MongoDB para persistencia real (no trabaja muy bien con render)
- [ ] Migración a Railway para trabajar con MongoDB
- [ ] Sistema de autenticación con JWT
- [ ] Roles de usuario (admin, empleado, cliente)
- [ ] Pasarela de pago (Stripe/PayPal)
- [ ] Sistema de cupones de descuento
- [ ] Seguimiento de envíos en tiempo real
- [ ] API de notificaciones push
- [ ] Tests unitarios y de integración
- [ ] Rate limiting y throttling
- [ ] Cache con Redis

## 👨‍💻 Autor

**Israel**
- GitHub: [@jiisraell](https://github.com/jiisraell)
- Email: israeltrabajo02@gmail.com

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y de portfolio.

---

**Desarrollado con ❤️ para El Encanto de la Huerta**
