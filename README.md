# PoliMarket - Sistema de Gestión Empresarial

## Descripción del Proyecto

Este proyecto implementa el sistema de gestión de PoliMarket con arquitectura de componentes, siguiendo los requisitos de la asignatura "Temas Avanzados de Diseño de Software".

## Estructura del Proyecto

```
PoliMarket-System/
├── backend/                 # API REST en Python (FastAPI)
│   ├── app/
│   │   ├── components/      # Componentes Manager
│   │   │   ├── auth_manager.py
│   │   │   ├── venta_manager.py
│   │   │   ├── inventario_manager.py
│   │   │   ├── entrega_manager.py
│   │   │   └── proveedor_manager.py
│   │   ├── models/          # Modelos de datos
│   │   │   ├── database.py
│   │   │   ├── entities.py
│   │   │   └── schemas.py
│   │   ├── api/             # Endpoints de la API
│   │   │   ├── auth.py
│   │   │   ├── ventas.py
│   │   │   ├── inventario.py
│   │   │   ├── entregas.py
│   │   │   └── proveedores.py
│   │   └── main.py          # Aplicación principal
│   ├── requirements.txt
│   ├── run.py
│   └── init_data.py         # Script para inicializar datos
├── client-web/              # Cliente web en JavaScript
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── client-console/          # Cliente de consola en Python
│   └── console_client.py
└── README.md
```

## Requisitos Funcionales Implementados

- **RF01**: Gestión de Autorizaciones - Autenticación y autorización de vendedores
- **RF02**: Gestión de Ventas - Creación y consulta de ventas, gestión de clientes
- **RF03**: Gestión de Inventario - Consulta de productos y control de stock
- **RF04**: Gestión de Proveedores - Registro de productos y proveedores, gestión de compras
- **RF05**: Gestión de Entregas - Programación y seguimiento de entregas

## Instalación y Ejecución

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno

### 1. Backend (API REST)

1. **Instalar dependencias:**
```bash
cd PoliMarket-System/backend
pip install -r requirements.txt
```

2. **Inicializar la base de datos con datos de ejemplo:**
```bash
python init_data.py
```

3. **Ejecutar el servidor:**
```bash
python run.py
```

El servidor estará disponible en: http://localhost:8000

**Datos de prueba disponibles:**
- Vendedor 1: `carlos.rodriguez@polimarket.com` / `password123`
- Vendedor 2: `ana.martinez@polimarket.com` / `password123`
- Clientes: ID 1 y 2
- Productos: ID 1, 2 y 3
- Proveedores: ID 1 y 2
- Compras: ID 1 y 2

### 2. Cliente Web

1. **Abrir el archivo HTML:**
```bash
# Desde el directorio raíz del proyecto
start client-web/index.html
```

2. **O navegar directamente a:**
```
file:///ruta/completa/a/PoliMarket-System/client-web/index.html
```

El cliente web incluye:
- **RF01**: Login de vendedores, consulta de autorizaciones
- **RF02**: Consulta de ventas por vendedor, listado de clientes
- **RF03**: Listado de productos, consulta de inventario
- **RF04**: Listado de proveedores, búsqueda de proveedores, consulta de compras
- **RF05**: Consulta de entregas pendientes, consulta de entregas por fecha

### 3. Cliente Consola

1. **Ejecutar desde el directorio raíz:**
```bash
python client-console/console_client.py
```

El cliente de consola incluye:
- **RF01**: Login de vendedores
- **RF02**: Consulta de ventas, creación de ventas
- **RF03**: Listado de productos, consulta de inventario
- **RF04**: Listado de proveedores, búsqueda de proveedores, consulta de compras
- **RF05**: Consulta de entregas pendientes, consulta de entregas por fecha

## Componentes Implementados

### Capa de Negocio (Managers)
- **AutorizacionManager**: Gestión de autenticación y autorizaciones
- **VentaManager**: Gestión de ventas y transacciones
- **ClienteManager**: Gestión de clientes
- **InventarioManager**: Control de inventario y stock
- **ProductoManager**: Gestión de productos
- **EntregaManager**: Gestión de entregas
- **LogisticaManager**: Coordinación logística
- **ProveedorManager**: Gestión de proveedores
- **CompraManager**: Gestión de compras y órdenes

### Capa de Cliente (Facades)
- **AuthFacade**: Endpoints de autenticación
- **VentasFacade**: Endpoints de ventas y clientes
- **InventarioFacade**: Endpoints de productos e inventario
- **EntregasFacade**: Endpoints de entregas
- **ProveedoresFacade**: Endpoints de proveedores y compras

## Endpoints de la API

### Autenticación (RF01)
- `POST /auth/login` - Login de vendedor
- `POST /auth/vendedores` - Crear vendedor
- `POST /auth/autorizar/{vendedor_id}` - Autorizar vendedor
- `GET /auth/vendedores` - Listar vendedores
- `GET /auth/vendedores/no-autorizados` - Vendedores no autorizados

### Ventas (RF02)
- `POST /ventas/` - Crear venta
- `GET /ventas/{venta_id}` - Consultar venta
- `GET /ventas/vendedor/{vendedor_id}` - Ventas por vendedor
- `GET /ventas/{venta_id}/total` - Calcular total
- `GET /ventas/clientes` - Listar clientes
- `POST /ventas/clientes` - Crear cliente

### Inventario (RF03)
- `GET /inventario/productos` - Listar productos
- `GET /inventario/productos/{producto_id}` - Consultar producto
- `GET /inventario/disponibilidad/{producto_id}/{cantidad}` - Verificar disponibilidad
- `GET /inventario/stock/{producto_id}` - Consultar inventario
- `GET /inventario/bajo-stock` - Productos bajo stock
- `POST /inventario/productos` - Crear producto
- `POST /inventario/stock/{producto_id}` - Actualizar stock

### Proveedores (RF04)
- `POST /proveedores/` - Crear proveedor
- `GET /proveedores/{proveedor_id}` - Consultar proveedor
- `GET /proveedores/` - Listar proveedores
- `PUT /proveedores/{proveedor_id}` - Actualizar proveedor
- `DELETE /proveedores/{proveedor_id}` - Eliminar proveedor
- `GET /proveedores/buscar/{nombre}` - Buscar proveedores
- `POST /proveedores/compras/` - Registrar compra
- `GET /proveedores/compras/{compra_id}` - Consultar compra
- `GET /proveedores/compras/proveedor/{proveedor_id}` - Compras por proveedor
- `GET /proveedores/compras/pendientes` - Compras pendientes
- `PUT /proveedores/compras/{compra_id}/estado` - Actualizar estado de compra
- `GET /proveedores/compras/{compra_id}/total` - Calcular total de compra

### Entregas (RF05)
- `POST /entregas/{venta_id}` - Programar entrega
- `GET /entregas/{entrega_id}` - Consultar entrega
- `GET /entregas/pendientes` - Entregas pendientes
- `PUT /entregas/{entrega_id}/estado` - Actualizar estado
- `POST /entregas/{entrega_id}/confirmar` - Confirmar entrega

## Tecnologías Utilizadas

- **Backend**: Python 3.8+, FastAPI, SQLAlchemy, SQLite, PyJWT
- **Cliente Web**: HTML5, CSS3, JavaScript (Vanilla)
- **Cliente Consola**: Python, requests
- **Base de Datos**: SQLite
- **Autenticación**: JWT (JSON Web Tokens)

## Arquitectura

El sistema sigue una arquitectura de componentes con:

- **Separación clara de responsabilidades** entre capas
- **Interfaces bien definidas** entre componentes
- **Comunicación a través de APIs REST** estándar
- **Patrón Facade** para simplificar el acceso a los servicios
- **Autenticación JWT** para seguridad
- **Validación de datos** con Pydantic
- **Manejo de errores** centralizado

## Funcionalidades por Cliente

### Cliente Web
- Interfaz gráfica moderna con tabs
- Consulta de productos disponibles (RF03)
- Login y gestión de vendedores (RF01)
- Consulta de ventas y clientes (RF02)
- Gestión de proveedores y compras (RF04)
- Seguimiento de entregas (RF05)

### Cliente Consola
- Menú interactivo por consola
- Autenticación de vendedores (RF01)
- Consulta de inventario (RF03)
- Creación de ventas (RF02)
- Gestión de proveedores y compras (RF04)
- Seguimiento de entregas (RF05)

## Notas de Desarrollo

- Los errores de linter (imports no resueltos) son normales en el entorno de desarrollo sin las dependencias instaladas
- La base de datos se crea automáticamente al ejecutar el servidor
- Los datos de ejemplo se cargan con el script `init_data.py`
- El sistema incluye autenticación básica con JWT
- CORS está configurado para permitir conexiones desde el cliente web

## Solución de Problemas

1. **Error de conexión**: Verificar que el servidor esté ejecutándose en puerto 8000
2. **Dependencias faltantes**: Ejecutar `pip install -r requirements.txt`
3. **Base de datos**: Ejecutar `python init_data.py` para inicializar datos
4. **CORS**: El servidor está configurado para aceptar conexiones desde cualquier origen

## Documentación de la API

Una vez ejecutado el servidor, la documentación automática estará disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc