from datetime import date
from sqlalchemy.orm import Session
from ..models.entities import Entrega, Venta
from ..models.schemas import EntregaCreate

class EntregaManager:
    """Componente para gestión de entregas (RF05)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def programar_entrega(self, venta_id: int, entrega_data: EntregaCreate) -> Entrega:
        """Programa una entrega (RF05)"""
        try:
            # Verificar que la venta existe
            venta = self.db.query(Venta).filter(Venta.id == venta_id).first()
            if not venta:
                return None
            
            # Verificar que no existe ya una entrega para esta venta
            entrega_existente = self.db.query(Entrega).filter(Entrega.venta_id == venta_id).first()
            if entrega_existente:
                return None
            
            entrega = Entrega(
                venta_id=venta_id,
                fecha_entrega=entrega_data.fecha_entrega,
                direccion=entrega_data.direccion,
                transportista=entrega_data.transportista,
                estado=entrega_data.estado
            )
            self.db.add(entrega)
            self.db.commit()
            self.db.refresh(entrega)
            return entrega
        except Exception as e:
            self.db.rollback()
            print(f"Error programando entrega: {e}")
            return None
    
    def consultar_entrega(self, entrega_id: int) -> Entrega:
        """Consulta una entrega por ID (RF05)"""
        return self.db.query(Entrega).filter(Entrega.id == entrega_id).first()
    
    def listar_entregas_pendientes(self):
        """Lista entregas pendientes (RF05)"""
        return self.db.query(Entrega).filter(Entrega.estado == "PENDIENTE").all()
    
    def actualizar_estado_entrega(self, entrega_id: int, estado: str) -> bool:
        """Actualiza el estado de una entrega (RF05)"""
        try:
            entrega = self.db.query(Entrega).filter(Entrega.id == entrega_id).first()
            if not entrega:
                return False
            
            entrega.estado = estado
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error actualizando estado de entrega: {e}")
            return False

class LogisticaManager:
    """Componente para gestión de logística (RF05)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def registrar_salida_stock(self, venta_id: int) -> bool:
        """Registra la salida de stock por una venta (RF05)"""
        try:
            venta = self.db.query(Venta).filter(Venta.id == venta_id).first()
            if not venta:
                return False
            
            # El stock ya se actualiza en VentaManager.crear_venta()
            # Este método es para registro adicional si es necesario
            return True
        except Exception as e:
            print(f"Error registrando salida de stock: {e}")
            return False
    
    def confirmar_entrega(self, entrega_id: int) -> bool:
        """Confirma una entrega (RF05)"""
        try:
            entrega = self.db.query(Entrega).filter(Entrega.id == entrega_id).first()
            if not entrega:
                return False
            
            entrega.estado = "ENTREGADO"
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error confirmando entrega: {e}")
            return False
    
    def consultar_entregas_por_fecha(self, fecha: date):
        """Consulta entregas por fecha (RF05)"""
        return self.db.query(Entrega).filter(Entrega.fecha_entrega == fecha).all() 