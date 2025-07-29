from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, engine
from app.models.entities import Base, Vendedor, Cliente, Producto, Inventario, Proveedor, Compra, DetalleCompra
from app.models.schemas import VendedorCreate
from app.components.auth_manager import AutorizacionManager

def init_db():
    """Inicializa la base de datos con datos de ejemplo"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Crear proveedores
        proveedor1 = Proveedor(
            tipo_documento="NIT",
            documento="900123456-7",
            nombre="Proveedor ABC",
            contacto="Juan Pérez",
            email="contacto@proveedorabc.com",
            telefono="3001234567",
            direccion="Calle 123 #45-67, Bogotá"
        )
        db.add(proveedor1)
        db.flush()
        
        proveedor2 = Proveedor(
            tipo_documento="NIT", 
            documento="900987654-3",
            nombre="Proveedor XYZ",
            contacto="María García",
            email="ventas@proveedorxyz.com",
            telefono="3009876543",
            direccion="Carrera 78 #90-12, Medellín"
        )
        db.add(proveedor2)
        db.flush()
        
        # Crear productos
        producto1 = Producto(
            nombre="Laptop HP Pavilion",
            descripcion="Laptop de 15 pulgadas, 8GB RAM, 256GB SSD",
            precio=Decimal('2500000.00'),
            categoria="Tecnología",
            proveedor_id=proveedor1.id
        )
        db.add(producto1)
        db.flush()
        
        producto2 = Producto(
            nombre="Mouse Inalámbrico",
            descripcion="Mouse óptico inalámbrico con receptor USB",
            precio=Decimal('45000.00'),
            categoria="Tecnología",
            proveedor_id=proveedor1.id
        )
        db.add(producto2)
        db.flush()
        
        producto3 = Producto(
            nombre="Teclado Mecánico",
            descripcion="Teclado mecánico RGB con switches blue",
            precio=Decimal('180000.00'),
            categoria="Tecnología",
            proveedor_id=proveedor2.id
        )
        db.add(producto3)
        db.flush()
        
        # Crear inventario
        inventario1 = Inventario(
            producto_id=producto1.id,
            cantidad_disponible=10,
            cantidad_minima=5,
            ubicacion="Estante A1"
        )
        db.add(inventario1)
        
        inventario2 = Inventario(
            producto_id=producto2.id,
            cantidad_disponible=25,
            cantidad_minima=10,
            ubicacion="Estante A2"
        )
        db.add(inventario2)
        
        inventario3 = Inventario(
            producto_id=producto3.id,
            cantidad_disponible=8,
            cantidad_minima=5,
            ubicacion="Estante B1"
        )
        db.add(inventario3)
        
        # Crear vendedores
        auth_manager = AutorizacionManager(db)
        
        vendedor1_data = VendedorCreate(
            tipo_documento="CC",
            documento="12345678",
            nombre="Carlos Rodríguez",
            email="carlos.rodriguez@polimarket.com",
            telefono="3001111111",
            password="password123"
        )
        vendedor1 = auth_manager.crear_vendedor(vendedor1_data)
        
        vendedor2_data = VendedorCreate(
            tipo_documento="CC", 
            documento="87654321",
            nombre="Ana Martínez",
            email="ana.martinez@polimarket.com",
            telefono="3002222222",
            password="password123"
        )
        vendedor2 = auth_manager.crear_vendedor(vendedor2_data)
        
        # Autorizar vendedores
        if vendedor1 and vendedor2:
            vendedor1_id = vendedor1.id
            vendedor2_id = vendedor2.id
            auth_manager.autorizar_vendedor(vendedor1_id, "RRHH Admin")
            auth_manager.autorizar_vendedor(vendedor2_id, "RRHH Admin")
        
        # Crear clientes
        cliente1 = Cliente(
            tipo_documento="CC",
            documento="11111111",
            nombre="Pedro López",
            email="pedro.lopez@email.com",
            telefono="3003333333",
            direccion="Calle 45 #67-89, Bogotá",
            tipo_cliente="REGULAR"
        )
        db.add(cliente1)
        
        cliente2 = Cliente(
            tipo_documento="CC",
            documento="22222222", 
            nombre="Laura Silva",
            email="laura.silva@email.com",
            telefono="3004444444",
            direccion="Carrera 34 #56-78, Medellín",
            tipo_cliente="VIP"
        )
        db.add(cliente2)
        
        # Crear compras de ejemplo (RF04)
        compra1 = Compra(
            proveedor_id=proveedor1.id,
            fecha_compra=date.today(),
            fecha_entrega=date(2024, 12, 15),
            total=Decimal('5000000.00'),
            estado="PENDIENTE",
            numero_orden="ORD-001-2024"
        )
        db.add(compra1)
        db.flush()
        
        # Detalles de compra 1
        detalle_compra1 = DetalleCompra(
            compra_id=compra1.id,
            producto_id=producto1.id,
            cantidad=2,
            precio_compra=Decimal('2200000.00')  # Precio de compra menor al de venta
        )
        db.add(detalle_compra1)
        
        detalle_compra2 = DetalleCompra(
            compra_id=compra1.id,
            producto_id=producto2.id,
            cantidad=10,
            precio_compra=Decimal('35000.00')  # Precio de compra menor al de venta
        )
        db.add(detalle_compra2)
        
        compra2 = Compra(
            proveedor_id=proveedor2.id,
            fecha_compra=date.today(),
            fecha_entrega=date(2024, 12, 20),
            total=Decimal('900000.00'),
            estado="RECIBIDA",
            numero_orden="ORD-002-2024"
        )
        db.add(compra2)
        db.flush()
        
        # Detalles de compra 2
        detalle_compra3 = DetalleCompra(
            compra_id=compra2.id,
            producto_id=producto3.id,
            cantidad=5,
            precio_compra=Decimal('150000.00')  # Precio de compra menor al de venta
        )
        db.add(detalle_compra3)
        
        db.commit()
        print("Base de datos inicializada con datos de ejemplo")
        print("✅ RF04 - Gestión de Proveedores implementado")
        
    except Exception as e:
        db.rollback()
        print(f"Error inicializando datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 