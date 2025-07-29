from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from ..models.entities import Proveedor, Compra, DetalleCompra, Producto, Inventario
from ..models.schemas import ProveedorCreate, CompraCreate

class ProveedorManager:
    """Componente para gestión de proveedores (RF04)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def crear_proveedor(self, proveedor_data: ProveedorCreate) -> Proveedor:
        """Crea un nuevo proveedor (RF04)"""
        try:
            proveedor = Proveedor(
                tipo_documento=proveedor_data.tipo_documento,
                documento=proveedor_data.documento,
                nombre=proveedor_data.nombre,
                contacto=proveedor_data.contacto,
                email=proveedor_data.email,
                telefono=proveedor_data.telefono,
                direccion=proveedor_data.direccion
            )
            self.db.add(proveedor)
            self.db.commit()
            self.db.refresh(proveedor)
            return proveedor
        except Exception as e:
            self.db.rollback()
            print(f"Error creando proveedor: {e}")
            return None
    
    def consultar_proveedor(self, proveedor_id: int) -> Proveedor:
        """Consulta un proveedor por ID (RF04)"""
        return self.db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    
    def listar_proveedores(self):
        """Lista todos los proveedores (RF04)"""
        return self.db.query(Proveedor).all()
    
    def actualizar_proveedor(self, proveedor_id: int, proveedor_data: ProveedorCreate) -> bool:
        """Actualiza un proveedor (RF04)"""
        try:
            proveedor = self.db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
            if not proveedor:
                return False
            
            proveedor.tipo_documento = proveedor_data.tipo_documento
            proveedor.documento = proveedor_data.documento
            proveedor.nombre = proveedor_data.nombre
            proveedor.contacto = proveedor_data.contacto
            proveedor.email = proveedor_data.email
            proveedor.telefono = proveedor_data.telefono
            proveedor.direccion = proveedor_data.direccion
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error actualizando proveedor: {e}")
            return False
    
    def eliminar_proveedor(self, proveedor_id: int) -> bool:
        """Elimina un proveedor (RF04)"""
        try:
            proveedor = self.db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
            if not proveedor:
                return False
            
            # Verificar que no tenga productos asociados
            productos = self.db.query(Producto).filter(Producto.proveedor_id == proveedor_id).count()
            if productos > 0:
                return False  # No se puede eliminar si tiene productos
            
            self.db.delete(proveedor)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error eliminando proveedor: {e}")
            return False
    
    def buscar_proveedores_por_nombre(self, nombre: str):
        """Busca proveedores por nombre (RF04)"""
        return self.db.query(Proveedor).filter(Proveedor.nombre.ilike(f"%{nombre}%")).all()

class CompraManager:
    """Componente para gestión de compras (RF04)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def registrar_compra(self, compra_data: CompraCreate) -> Compra:
        """Registra una nueva compra (RF04)"""
        try:
            # Verificar que el proveedor existe
            proveedor = self.db.query(Proveedor).filter(Proveedor.id == compra_data.proveedor_id).first()
            if not proveedor:
                return None
            
            # Crear la compra
            compra = Compra(
                proveedor_id=compra_data.proveedor_id,
                fecha_compra=compra_data.fecha_compra,
                fecha_entrega=compra_data.fecha_entrega,
                total=Decimal('0.00'),
                estado=compra_data.estado,
                numero_orden=compra_data.numero_orden
            )
            self.db.add(compra)
            self.db.flush()  # Para obtener el ID de la compra
            
            total_compra = Decimal('0.00')
            
            # Procesar detalles de la compra
            for detalle in compra_data.detalles:
                producto_id = detalle.get('producto_id')
                cantidad = detalle.get('cantidad', 0)
                precio_compra = detalle.get('precio_compra', 0)
                
                # Verificar que el producto existe
                producto = self.db.query(Producto).filter(Producto.id == producto_id).first()
                if not producto:
                    self.db.rollback()
                    return None
                
                # Crear detalle de compra
                detalle_compra = DetalleCompra(
                    compra_id=compra.id,
                    producto_id=producto_id,
                    cantidad=cantidad,
                    precio_compra=precio_compra
                )
                self.db.add(detalle_compra)
                
                # Calcular total
                total_compra += precio_compra * cantidad
            
            # Actualizar total de la compra
            compra.total = total_compra
            
            self.db.commit()
            self.db.refresh(compra)
            return compra
            
        except Exception as e:
            self.db.rollback()
            print(f"Error registrando compra: {e}")
            return None
    
    def consultar_compra(self, compra_id: int) -> Compra:
        """Consulta una compra por ID (RF04)"""
        return self.db.query(Compra).filter(Compra.id == compra_id).first()
    
    def listar_compras_por_proveedor(self, proveedor_id: int):
        """Lista compras por proveedor (RF04)"""
        return self.db.query(Compra).filter(Compra.proveedor_id == proveedor_id).all()
    
    def listar_compras_pendientes(self):
        """Lista compras pendientes (RF04)"""
        return self.db.query(Compra).filter(Compra.estado == "PENDIENTE").all()
    
    def actualizar_estado_compra(self, compra_id: int, estado: str) -> bool:
        """Actualiza el estado de una compra (RF04)"""
        try:
            compra = self.db.query(Compra).filter(Compra.id == compra_id).first()
            if not compra:
                return False
            
            compra.estado = estado
            
            # Si la compra se marca como recibida, actualizar inventario
            if estado == "RECIBIDA":
                self._actualizar_inventario_por_compra(compra_id)
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error actualizando estado de compra: {e}")
            return False
    
    def _actualizar_inventario_por_compra(self, compra_id: int):
        """Actualiza el inventario cuando se recibe una compra (RF04)"""
        try:
            compra = self.db.query(Compra).filter(Compra.id == compra_id).first()
            if not compra:
                return
            
            for detalle in compra.detalles:
                # Buscar o crear inventario para el producto
                inventario = self.db.query(Inventario).filter(Inventario.producto_id == detalle.producto_id).first()
                if inventario:
                    inventario.cantidad_disponible += detalle.cantidad
                else:
                    # Crear nuevo inventario si no existe
                    inventario = Inventario(
                        producto_id=detalle.producto_id,
                        cantidad_disponible=detalle.cantidad,
                        cantidad_minima=10,
                        ubicacion="Bodega Principal"
                    )
                    self.db.add(inventario)
            
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Error actualizando inventario por compra: {e}")
    
    def calcular_total_compra(self, compra_id: int) -> Decimal:
        """Calcula el total de una compra (RF04)"""
        compra = self.db.query(Compra).filter(Compra.id == compra_id).first()
        if not compra:
            return Decimal('0.00')
        
        total = Decimal('0.00')
        for detalle in compra.detalles:
            total += detalle.precio_compra * detalle.cantidad
        
        return total 