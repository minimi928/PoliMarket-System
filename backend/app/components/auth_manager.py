import hashlib
import jwt
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from ..models.entities import Vendedor, Autorizacion
from ..models.schemas import VendedorCreate, AutorizacionCreate

SECRET_KEY = "polimarket_secret_key_2024"
ALGORITHM = "HS256"

class AutorizacionManager:
    """Componente para gestión de autorizaciones (RF01)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _hash_password(self, password: str) -> str:
        """Hashea la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        return self._hash_password(plain_password) == hashed_password
    
    def _create_access_token(self, data: dict) -> str:
        """Crea un token JWT"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=24)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def autorizar_vendedor(self, vendedor_id: int, responsable: str) -> bool:
        """Autoriza un vendedor (RF01)"""
        try:
            vendedor = self.db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
            if not vendedor:
                return False
            
            # Crear autorización
            autorizacion = Autorizacion(
                vendedor_id=vendedor_id,
                fecha_autorizacion=date.today(),
                estado="AUTORIZADO",
                rrhh_responsable=responsable
            )
            
            # Actualizar estado del vendedor
            vendedor.estado_autorizacion = True
            vendedor.fecha_autorizacion = date.today()
            
            self.db.add(autorizacion)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error autorizando vendedor: {e}")
            return False
    
    def validar_autorizacion(self, vendedor_id: int) -> bool:
        """Valida si un vendedor está autorizado (RF01)"""
        vendedor = self.db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
        return vendedor and vendedor.estado_autorizacion
    
    def consultar_vendedores_no_autorizados(self):
        """Consulta vendedores no autorizados (RF01)"""
        return self.db.query(Vendedor).filter(Vendedor.estado_autorizacion == False).all()
    
    def revocar_autorizacion(self, vendedor_id: int) -> bool:
        """Revoca la autorización de un vendedor (RF01)"""
        try:
            vendedor = self.db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
            if not vendedor:
                return False
            
            vendedor.estado_autorizacion = False
            vendedor.fecha_autorizacion = None
            
            # Actualizar autorización
            autorizacion = self.db.query(Autorizacion).filter(Autorizacion.vendedor_id == vendedor_id).first()
            if autorizacion:
                autorizacion.estado = "REVOCADO"
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error revocando autorización: {e}")
            return False
    
    def login_vendedor(self, email: str, password: str):
        """Autentica un vendedor y retorna token"""
        vendedor = self.db.query(Vendedor).filter(Vendedor.email == email).first()
        if not vendedor or not self._verify_password(password, vendedor.password_hash):
            return None
        
        if not vendedor.estado_autorizacion:
            return None
        
        access_token = self._create_access_token(data={"sub": str(vendedor.id)})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "vendedor": vendedor
        }
    
    def crear_vendedor(self, vendedor_data: VendedorCreate) -> Vendedor:
        """Crea un nuevo vendedor (RF01)"""
        try:
            hashed_password = self._hash_password(vendedor_data.password)
            vendedor = Vendedor(
                tipo_documento=vendedor_data.tipo_documento,
                documento=vendedor_data.documento,
                nombre=vendedor_data.nombre,
                email=vendedor_data.email,
                telefono=vendedor_data.telefono,
                password_hash=hashed_password,
                estado_autorizacion=False
            )
            self.db.add(vendedor)
            self.db.commit()
            self.db.refresh(vendedor)
            return vendedor
        except Exception as e:
            self.db.rollback()
            print(f"Error creando vendedor: {e}")
            return None
    
    def consultar_vendedor(self, vendedor_id: int) -> Vendedor:
        """Consulta un vendedor por ID (RF01)"""
        return self.db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
    
    def listar_vendedores(self):
        """Lista todos los vendedores (RF01)"""
        return self.db.query(Vendedor).all() 