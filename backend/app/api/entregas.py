from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from ..models.database import get_db
from ..models.schemas import EntregaCreate, ResponseDTO
from ..components.entrega_manager import EntregaManager, LogisticaManager

router = APIRouter(prefix="/entregas", tags=["Entregas"])

@router.post("/{venta_id}", response_model=ResponseDTO)
def programar_entrega(venta_id: int, entrega_data: EntregaCreate, db: Session = Depends(get_db)):
    """Endpoint para programar entrega (RF05)"""
    entrega_manager = EntregaManager(db)
    entrega = entrega_manager.programar_entrega(venta_id, entrega_data)
    
    if not entrega:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error programando entrega - verificar que la venta existe y no tiene entrega previa"
        )
    
    return ResponseDTO(
        success=True,
        message="Entrega programada exitosamente",
        data={
            "entrega_id": entrega.id,
            "venta_id": entrega.venta_id,
            "fecha_entrega": entrega.fecha_entrega.isoformat(),
            "estado": entrega.estado
        }
    )

@router.get("/pendientes", response_model=ResponseDTO)
def listar_entregas_pendientes(db: Session = Depends(get_db)):
    """Endpoint para listar entregas pendientes (RF05)"""
    entrega_manager = EntregaManager(db)
    entregas = entrega_manager.listar_entregas_pendientes()
    
    return ResponseDTO(
        success=True,
        message="Entregas pendientes consultadas",
        data={"entregas": [
            {
                "id": e.id,
                "venta_id": e.venta_id,
                "fecha_entrega": e.fecha_entrega.isoformat(),
                "direccion": e.direccion,
                "estado": e.estado
            } for e in entregas
        ]}
    )

@router.get("/{entrega_id}", response_model=ResponseDTO)
def consultar_entrega(entrega_id: int, db: Session = Depends(get_db)):
    """Endpoint para consultar entrega (RF05)"""
    entrega_manager = EntregaManager(db)
    entrega = entrega_manager.consultar_entrega(entrega_id)
    
    if not entrega:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrega no encontrada"
        )
    
    return ResponseDTO(
        success=True,
        message="Entrega consultada",
        data={
            "id": entrega.id,
            "venta_id": entrega.venta_id,
            "fecha_entrega": entrega.fecha_entrega.isoformat(),
            "direccion": entrega.direccion,
            "estado": entrega.estado,
            "transportista": entrega.transportista
        }
    )

@router.put("/{entrega_id}/estado", response_model=ResponseDTO)
def actualizar_estado_entrega(entrega_id: int, estado: str, db: Session = Depends(get_db)):
    """Endpoint para actualizar estado de entrega (RF05)"""
    entrega_manager = EntregaManager(db)
    success = entrega_manager.actualizar_estado_entrega(entrega_id, estado)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error actualizando estado de entrega"
        )
    
    return ResponseDTO(
        success=True,
        message="Estado de entrega actualizado exitosamente",
        data={
            "entrega_id": entrega_id,
            "nuevo_estado": estado
        }
    )

@router.post("/{entrega_id}/confirmar", response_model=ResponseDTO)
def confirmar_entrega(entrega_id: int, db: Session = Depends(get_db)):
    """Endpoint para confirmar entrega (RF05)"""
    logistica_manager = LogisticaManager(db)
    success = logistica_manager.confirmar_entrega(entrega_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error confirmando entrega"
        )
    
    return ResponseDTO(
        success=True,
        message="Entrega confirmada exitosamente",
        data={"entrega_id": entrega_id}
    )

@router.get("/fecha/{fecha}", response_model=ResponseDTO)
def consultar_entregas_por_fecha(fecha: date, db: Session = Depends(get_db)):
    """Endpoint para consultar entregas por fecha (RF05)"""
    logistica_manager = LogisticaManager(db)
    entregas = logistica_manager.consultar_entregas_por_fecha(fecha)
    
    return ResponseDTO(
        success=True,
        message=f"Entregas del {fecha} consultadas",
        data={"entregas": [
            {
                "id": e.id,
                "venta_id": e.venta_id,
                "fecha_entrega": e.fecha_entrega.isoformat(),
                "estado": e.estado
            } for e in entregas
        ]}
    ) 