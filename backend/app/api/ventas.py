from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from ..models.database import get_db
from ..models.schemas import VentaCreate, ClienteCreate, ResponseDTO
from ..components.venta_manager import VentaManager, ClienteManager

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.post("/", response_model=ResponseDTO)
def crear_venta(venta_data: VentaCreate, db: Session = Depends(get_db)):
    """Endpoint para crear venta (RF02)"""
    venta_manager = VentaManager(db)
    venta = venta_manager.crear_venta(venta_data)
    
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creando venta - verificar disponibilidad de productos"
        )
    
    return ResponseDTO(
        success=True,
        message="Venta creada exitosamente",
        data={
            "venta_id": venta.id,
            "total": float(str(venta.total)),
            "fecha": venta.fecha.isoformat()
        }
    )

@router.get("/vendedor/{vendedor_id}", response_model=ResponseDTO)
def listar_ventas_por_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
    """Endpoint para listar ventas por vendedor (RF02)"""
    venta_manager = VentaManager(db)
    ventas = venta_manager.listar_ventas_por_vendedor(vendedor_id)
    
    return ResponseDTO(
        success=True,
        message="Ventas del vendedor consultadas",
        data={"ventas": [
            {
                "id": v.id,
                "cliente_id": v.cliente_id,
                "fecha": v.fecha.isoformat(),
                "total": float(str(v.total)),
                "estado": v.estado
            } for v in ventas
        ]}
    )

# Endpoints para clientes
@router.get("/clientes", response_model=ResponseDTO)
def listar_clientes(db: Session = Depends(get_db)):
    """Endpoint para listar clientes (RF02)"""
    cliente_manager = ClienteManager(db)
    clientes = cliente_manager.listar_clientes()
    
    return ResponseDTO(
        success=True,
        message="Clientes consultados",
        data={"clientes": [
            {
                "id": c.id,
                "nombre": c.nombre,
                "email": c.email,
                "tipo_cliente": c.tipo_cliente
            } for c in clientes
        ]}
    )

@router.get("/{venta_id}/total", response_model=ResponseDTO)
def calcular_total_venta(venta_id: int, db: Session = Depends(get_db)):
    """Endpoint para calcular total de venta (RF02)"""
    venta_manager = VentaManager(db)
    total = venta_manager.calcular_total_venta(venta_id)
    
    return ResponseDTO(
        success=True,
        message="Total calculado",
        data={"total": float(str(total))}
    )

@router.get("/{venta_id}", response_model=ResponseDTO)
def consultar_venta(venta_id: int, db: Session = Depends(get_db)):
    """Endpoint para consultar venta (RF02)"""
    venta_manager = VentaManager(db)
    venta = venta_manager.consultar_venta(venta_id)
    
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    
    return ResponseDTO(
        success=True,
        message="Venta consultada",
        data={
            "id": venta.id,
            "vendedor_id": venta.vendedor_id,
            "cliente_id": venta.cliente_id,
            "fecha": venta.fecha.isoformat(),
            "total": float(str(venta.total)),
            "estado": venta.estado
        }
    )

@router.get("/clientes/{cliente_id}", response_model=ResponseDTO)
def consultar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Endpoint para consultar cliente (RF02)"""
    cliente_manager = ClienteManager(db)
    cliente = cliente_manager.consultar_cliente(cliente_id)
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    return ResponseDTO(
        success=True,
        message="Cliente consultado",
        data={
            "id": cliente.id,
            "nombre": cliente.nombre,
            "email": cliente.email,
            "tipo_cliente": cliente.tipo_cliente
        }
    )

@router.post("/clientes", response_model=ResponseDTO)
def crear_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """Endpoint para crear cliente (RF02)"""
    cliente_manager = ClienteManager(db)
    cliente = cliente_manager.crear_cliente(cliente_data)
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creando cliente"
        )
    
    return ResponseDTO(
        success=True,
        message="Cliente creado exitosamente",
        data={"cliente_id": cliente.id}
    ) 