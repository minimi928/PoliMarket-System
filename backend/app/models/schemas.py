from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from decimal import Decimal

# Esquemas base
class VendedorBase(BaseModel):
    tipo_documento: str
    documento: str
    nombre: str
    email: str
    telefono: Optional[str] = None

class VendedorCreate(VendedorBase):
    password: str

class Vendedor(VendedorBase):
    id: int
    estado_autorizacion: bool
    fecha_autorizacion: Optional[date] = None
    
    class Config:
        from_attributes = True

class ClienteBase(BaseModel):
    tipo_documento: str
    documento: str
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    tipo_cliente: str = "REGULAR"

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    
    class Config:
        from_attributes = True

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    categoria: Optional[str] = None
    proveedor_id: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    
    class Config:
        from_attributes = True

class InventarioBase(BaseModel):
    producto_id: int
    cantidad_disponible: int
    cantidad_minima: int = 10
    ubicacion: Optional[str] = None

class InventarioCreate(InventarioBase):
    pass

class Inventario(InventarioBase):
    id: int
    
    class Config:
        from_attributes = True

class VentaBase(BaseModel):
    vendedor_id: int
    cliente_id: int
    fecha: date
    estado: str = "PENDIENTE"

class VentaCreate(VentaBase):
    detalles: List[dict]  # Lista de productos con cantidad

class Venta(VentaBase):
    id: int
    total: Decimal
    
    class Config:
        from_attributes = True

class AutorizacionBase(BaseModel):
    vendedor_id: int
    rrhh_responsable: str
    estado: str = "PENDIENTE"

class AutorizacionCreate(AutorizacionBase):
    pass

class Autorizacion(AutorizacionBase):
    id: int
    fecha_autorizacion: date
    
    class Config:
        from_attributes = True

class EntregaBase(BaseModel):
    venta_id: int
    fecha_entrega: date
    direccion: str
    transportista: Optional[str] = None
    estado: str = "PENDIENTE"

class EntregaCreate(EntregaBase):
    pass

class Entrega(EntregaBase):
    id: int
    
    class Config:
        from_attributes = True

# Esquemas para autenticación
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    vendedor: Vendedor

# Esquemas para respuestas de API
class ResponseDTO(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

# Esquemas para RF04 - Gestión de Proveedores
class ProveedorBase(BaseModel):
    tipo_documento: str
    documento: str
    nombre: str
    contacto: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    pass

class Proveedor(ProveedorBase):
    id: int
    
    class Config:
        from_attributes = True

class CompraBase(BaseModel):
    proveedor_id: int
    fecha_compra: date
    fecha_entrega: date
    estado: str = "PENDIENTE"
    numero_orden: str

class CompraCreate(CompraBase):
    detalles: List[dict]  # Lista de productos con cantidad y precio_compra

class Compra(CompraBase):
    id: int
    total: Decimal
    
    class Config:
        from_attributes = True

class DetalleCompraBase(BaseModel):
    compra_id: int
    producto_id: int
    cantidad: int
    precio_compra: Decimal

class DetalleCompra(DetalleCompraBase):
    id: int
    
    class Config:
        from_attributes = True 