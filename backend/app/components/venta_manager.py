from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from ..models.entities import Venta, DetalleVenta, Cliente, Producto, Inventario
from ..models.schemas import VentaCreate, ClienteCreate

class VentaManager:
    """Componente para gestión de ventas (RF02)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def crear_venta(self, venta_data: VentaCreate) -> Venta:
        """Crea una nueva venta (RF02)"""
        try:
            # Verificar que el cliente existe
            cliente = self.db.query(Cliente).filter(Cliente.id == venta_data.cliente_id).first()
            if not cliente:
                return None
            
            # Crear la venta
            venta = Venta(
                vendedor_id=venta_data.vendedor_id,
                cliente_id=venta_data.cliente_id,
                fecha=venta_data.fecha,
                estado=venta_data.estado,
                total=Decimal('0.00')
            )
            self.db.add(venta)
            self.db.flush()  # Para obtener el ID de la venta
            
            total_venta = Decimal('0.00')
            
            # Procesar detalles de la venta
            for detalle in venta_data.detalles:
                producto_id = detalle.get('producto_id')
                cantidad = detalle.get('cantidad', 0)
                
                # Verificar disponibilidad
                inventario = self.db.query(Inventario).filter(Inventario.producto_id == producto_id).first()
                if not inventario or inventario.cantidad_disponible < cantidad:
                    self.db.rollback()
                    return None
                
                # Obtener producto para el precio
                producto = self.db.query(Producto).filter(Producto.id == producto_id).first()
                if not producto:
                    self.db.rollback()
                    return None
                
                # Crear detalle de venta
                detalle_venta = DetalleVenta(
                    venta_id=venta.id,
                    producto_id=producto_id,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )
                self.db.add(detalle_venta)
                
                # Actualizar inventario
                inventario.cantidad_disponible -= cantidad
                
                # Calcular total
                total_venta += producto.precio * cantidad
            
            # Actualizar total de la venta
            venta.total = total_venta
            
            self.db.commit()
            self.db.refresh(venta)

            # Crear entrega automáticamente
            from datetime import timedelta
            from ..models.entities import Entrega
            fecha_entrega = venta.fecha + timedelta(days=2)
            entrega = Entrega(
                venta_id=venta.id,
                fecha_entrega=fecha_entrega,
                direccion=cliente.direccion,
                estado="PENDIENTE",
                transportista=None
            )
            self.db.add(entrega)
            self.db.commit()
            self.db.refresh(entrega)

            return venta
            
        except Exception as e:
            self.db.rollback()
            print(f"Error creando venta: {e}")
            return None
    
    def consultar_venta(self, venta_id: int) -> Venta:
        """Consulta una venta por ID (RF02)"""
        return self.db.query(Venta).filter(Venta.id == venta_id).first()
    
    def listar_ventas_por_vendedor(self, vendedor_id: int):
        """Lista ventas por vendedor (RF02)"""
        return self.db.query(Venta).filter(Venta.vendedor_id == vendedor_id).all()
    
    def calcular_total_venta(self, venta_id: int) -> Decimal:
        """Calcula el total de una venta (RF02)"""
        venta = self.db.query(Venta).filter(Venta.id == venta_id).first()
        if not venta:
            return Decimal('0.00')
        
        total = Decimal('0.00')
        for detalle in venta.detalles:
            total += detalle.precio_unitario * detalle.cantidad
        
        return total

class ClienteManager:
    """Componente para gestión de clientes (RF02)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def crear_cliente(self, cliente_data: ClienteCreate) -> Cliente:
        """Crea un nuevo cliente (RF02)"""
        try:
            cliente = Cliente(
                tipo_documento=cliente_data.tipo_documento,
                documento=cliente_data.documento,
                nombre=cliente_data.nombre,
                email=cliente_data.email,
                telefono=cliente_data.telefono,
                direccion=cliente_data.direccion,
                tipo_cliente=cliente_data.tipo_cliente
            )
            self.db.add(cliente)
            self.db.commit()
            self.db.refresh(cliente)
            return cliente
        except Exception as e:
            self.db.rollback()
            print(f"Error creando cliente: {e}")
            return None
    
    def consultar_cliente(self, cliente_id: int) -> Cliente:
        """Consulta un cliente por ID (RF02)"""
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    def listar_clientes(self):
        """Lista todos los clientes (RF02)"""
        return self.db.query(Cliente).all()
    
    def actualizar_cliente(self, cliente_id: int, cliente_data: ClienteCreate) -> bool:
        """Actualiza un cliente (RF02)"""
        try:
            cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
            if not cliente:
                return False
            
            cliente.tipo_documento = cliente_data.tipo_documento
            cliente.documento = cliente_data.documento
            cliente.nombre = cliente_data.nombre
            cliente.email = cliente_data.email
            cliente.telefono = cliente_data.telefono
            cliente.direccion = cliente_data.direccion
            cliente.tipo_cliente = cliente_data.tipo_cliente
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error actualizando cliente: {e}")
            return False 