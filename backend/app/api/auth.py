from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.schemas import VendedorCreate, LoginRequest, ResponseDTO
from ..components.auth_manager import AutorizacionManager

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=ResponseDTO)
def login_vendedor(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Endpoint para login de vendedores (RF01)"""
    auth_manager = AutorizacionManager(db)
    result = auth_manager.login_vendedor(login_data.email, login_data.password)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas o vendedor no autorizado"
        )
    
    return ResponseDTO(
        success=True,
        message="Login exitoso",
        data={
            "access_token": result["access_token"],
            "token_type": result["token_type"],
            "vendedor": {
                "id": result["vendedor"].id,
                "nombre": result["vendedor"].nombre,
                "email": result["vendedor"].email,
                "estado_autorizacion": result["vendedor"].estado_autorizacion
            }
        }
    )

@router.post("/vendedores", response_model=ResponseDTO)
def crear_vendedor(vendedor_data: VendedorCreate, db: Session = Depends(get_db)):
    """Endpoint para crear vendedor (RF01)"""
    auth_manager = AutorizacionManager(db)
    vendedor = auth_manager.crear_vendedor(vendedor_data)
    
    if not vendedor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creando vendedor"
        )
    
    return ResponseDTO(
        success=True,
        message="Vendedor creado exitosamente",
        data={"vendedor_id": vendedor.id}
    )

@router.post("/autorizar/{vendedor_id}", response_model=ResponseDTO)
def autorizar_vendedor(vendedor_id: int, responsable: str, db: Session = Depends(get_db)):
    """Endpoint para autorizar vendedor (RF01)"""
    auth_manager = AutorizacionManager(db)
    success = auth_manager.autorizar_vendedor(vendedor_id, responsable)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error autorizando vendedor"
        )
    
    return ResponseDTO(
        success=True,
        message="Vendedor autorizado exitosamente"
    )

@router.get("/vendedores/no-autorizados", response_model=ResponseDTO)
def consultar_vendedores_no_autorizados(db: Session = Depends(get_db)):
    """Endpoint para consultar vendedores no autorizados (RF01)"""
    auth_manager = AutorizacionManager(db)
    vendedores = auth_manager.consultar_vendedores_no_autorizados()
    
    return ResponseDTO(
        success=True,
        message="Vendedores no autorizados consultados",
        data={"vendedores": [
            {
                "id": v.id,
                "nombre": v.nombre,
                "email": v.email,
                "documento": v.documento
            } for v in vendedores
        ]}
    )

@router.get("/vendedores", response_model=ResponseDTO)
def listar_vendedores(db: Session = Depends(get_db)):
    """Endpoint para listar todos los vendedores (RF01)"""
    auth_manager = AutorizacionManager(db)
    vendedores = auth_manager.listar_vendedores()
    
    return ResponseDTO(
        success=True,
        message="Vendedores consultados",
        data={"vendedores": [
            {
                "id": v.id,
                "nombre": v.nombre,
                "email": v.email,
                "estado_autorizacion": v.estado_autorizacion
            } for v in vendedores
        ]}
    ) 