from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Text
from sqlalchemy.types import Numeric
from sqlalchemy.orm import relationship
from .database import Base

class Vendedor(Base):
    __tablename__ = "vendedores"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_documento = Column(String(10), nullable=False)
    documento = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20))
    estado_autorizacion = Column(Boolean, default=False)
    fecha_autorizacion = Column(Date, nullable=True)
    password_hash = Column(String(255), nullable=False)
    
    # Relaciones
    autorizacion = relationship("Autorizacion", back_populates="vendedor", uselist=False)
    ventas = relationship("Venta", back_populates="vendedor")

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_documento = Column(String(10), nullable=False)
    documento = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion = Column(Text)
    tipo_cliente = Column(String(20), default="REGULAR")
    
    # Relaciones
    ventas = relationship("Venta", back_populates="cliente")

class Proveedor(Base):
    __tablename__ = "proveedores"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_documento = Column(String(10), nullable=False)
    documento = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    contacto = Column(String(100))
    email = Column(String(100))
    telefono = Column(String(20))
    direccion = Column(Text)
    
    # Relaciones
    productos = relationship("Producto", back_populates="proveedor")

class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(50))
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
    
    # Relaciones
    proveedor = relationship("Proveedor", back_populates="productos")
    inventario = relationship("Inventario", back_populates="producto", uselist=False)
    detalles_venta = relationship("DetalleVenta", back_populates="producto")

class Inventario(Base):
    __tablename__ = "inventario"
    
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), unique=True)
    cantidad_disponible = Column(Integer, default=0)
    cantidad_minima = Column(Integer, default=10)
    ubicacion = Column(String(50))
    
    # Relaciones
    producto = relationship("Producto", back_populates="inventario")

class Venta(Base):
    __tablename__ = "ventas"
    
    id = Column(Integer, primary_key=True, index=True)
    vendedor_id = Column(Integer, ForeignKey("vendedores.id"))
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    fecha = Column(Date, nullable=False)
    total = Column(Numeric(10, 2), default=0)
    estado = Column(String(20), default="PENDIENTE")
    
    # Relaciones
    vendedor = relationship("Vendedor", back_populates="ventas")
    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta")
    entrega = relationship("Entrega", back_populates="venta", uselist=False)

class DetalleVenta(Base):
    __tablename__ = "detalles_venta"
    
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    
    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")

class Entrega(Base):
    __tablename__ = "entregas"
    
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), unique=True)
    fecha_entrega = Column(Date, nullable=False)
    direccion = Column(Text, nullable=False)
    estado = Column(String(20), default="PENDIENTE")
    transportista = Column(String(100))
    
    # Relaciones
    venta = relationship("Venta", back_populates="entrega")

class Autorizacion(Base):
    __tablename__ = "autorizaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    vendedor_id = Column(Integer, ForeignKey("vendedores.id"), unique=True)
    fecha_autorizacion = Column(Date, nullable=False)
    estado = Column(String(20), default="PENDIENTE")
    rrhh_responsable = Column(String(100), nullable=False)
    
    # Relaciones
    vendedor = relationship("Vendedor", back_populates="autorizacion")

class Compra(Base):
    __tablename__ = "compras"
    
    id = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
    fecha_compra = Column(Date, nullable=False)
    fecha_entrega = Column(Date, nullable=False)
    total = Column(Numeric(10, 2), default=0)
    estado = Column(String(20), default="PENDIENTE")
    numero_orden = Column(String(50), unique=True)
    
    # Relaciones
    proveedor = relationship("Proveedor")
    detalles = relationship("DetalleCompra", back_populates="compra")

class DetalleCompra(Base):
    __tablename__ = "detalles_compra"
    
    id = Column(Integer, primary_key=True, index=True)
    compra_id = Column(Integer, ForeignKey("compras.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precio_compra = Column(Numeric(10, 2), nullable=False)
    
    # Relaciones
    compra = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto") 