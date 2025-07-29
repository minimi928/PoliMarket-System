from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.schemas import ProveedorCreate, CompraCreate, ResponseDTO
from ..components.proveedor_manager import ProveedorManager, CompraManager

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

# ==================== ENDPOINTS DE PROVEEDORES ====================

@router.post("/", response_model=ResponseDTO)
def crear_proveedor(proveedor_data: ProveedorCreate, db: Session = Depends(get_db)):
    """Endpoint para crear proveedor (RF04)"""
    proveedor_manager = ProveedorManager(db)
    proveedor = proveedor_manager.crear_proveedor(proveedor_data)
    
    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creando proveedor"
        )
    
    return ResponseDTO(
        success=True,
        message="Proveedor creado exitosamente",
        data={"proveedor_id": proveedor.id}
    )

@router.get("/{proveedor_id}", response_model=ResponseDTO)
def consultar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    """Endpoint para consultar proveedor (RF04)"""
    proveedor_manager = ProveedorManager(db)
    proveedor = proveedor_manager.consultar_proveedor(proveedor_id)
    
    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado"
        )
    
    return ResponseDTO(
        success=True,
        message="Proveedor consultado",
        data={
            "id": proveedor.id,
            "tipo_documento": proveedor.tipo_documento,
            "documento": proveedor.documento,
            "nombre": proveedor.nombre,
            "contacto": proveedor.contacto,
            "email": proveedor.email,
            "telefono": proveedor.telefono,
            "direccion": proveedor.direccion
        }
    )

@router.get("/", response_model=ResponseDTO)
def listar_proveedores(db: Session = Depends(get_db)):
    """Endpoint para listar proveedores (RF04)"""
    proveedor_manager = ProveedorManager(db)
    proveedores = proveedor_manager.listar_proveedores()
    
    return ResponseDTO(
        success=True,
        message="Proveedores consultados",
        data={"proveedores": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "documento": p.documento,
                "email": p.email,
                "telefono": p.telefono
            } for p in proveedores
        ]}
    )

@router.put("/{proveedor_id}", response_model=ResponseDTO)
def actualizar_proveedor(proveedor_id: int, proveedor_data: ProveedorCreate, db: Session = Depends(get_db)):
    """Endpoint para actualizar proveedor (RF04)"""
    proveedor_manager = ProveedorManager(db)
    success = proveedor_manager.actualizar_proveedor(proveedor_id, proveedor_data)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado"
        )
    
    return ResponseDTO(
        success=True,
        message="Proveedor actualizado exitosamente"
    )

@router.delete("/{proveedor_id}", response_model=ResponseDTO)
def eliminar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    """Endpoint para eliminar proveedor (RF04)"""
    proveedor_manager = ProveedorManager(db)
    success = proveedor_manager.eliminar_proveedor(proveedor_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el proveedor (tiene productos asociados o no existe)"
        )
    
    return ResponseDTO(
        success=True,
        message="Proveedor eliminado exitosamente"
    )

@router.get("/buscar/{nombre}", response_model=ResponseDTO)
def buscar_proveedores(nombre: str, db: Session = Depends(get_db)):
    """Endpoint para buscar proveedores por nombre (RF04)"""
    proveedor_manager = ProveedorManager(db)
    proveedores = proveedor_manager.buscar_proveedores_por_nombre(nombre)
    
    return ResponseDTO(
        success=True,
        message="Búsqueda de proveedores completada",
        data={"proveedores": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "documento": p.documento,
                "email": p.email
            } for p in proveedores
        ]}
    )

# ==================== ENDPOINTS DE COMPRAS ====================

@router.post("/compras/", response_model=ResponseDTO)
def registrar_compra(compra_data: CompraCreate, db: Session = Depends(get_db)):
    """Endpoint para registrar compra (RF04)"""
    compra_manager = CompraManager(db)
    compra = compra_manager.registrar_compra(compra_data)
    
    if not compra:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error registrando compra"
        )
    
    return ResponseDTO(
        success=True,
        message="Compra registrada exitosamente",
        data={"compra_id": compra.id, "total": float(compra.total)}
    )

@router.get("/compras/pendientes", response_model=ResponseDTO)
def listar_compras_pendientes(db: Session = Depends(get_db)):
    """Endpoint para listar compras pendientes (RF04)"""
    compra_manager = CompraManager(db)
    compras = compra_manager.listar_compras_pendientes()
    
    return ResponseDTO(
        success=True,
        message="Compras pendientes consultadas",
        data={"compras": [
            {
                "id": c.id,
                "proveedor_id": c.proveedor_id,
                "fecha_compra": c.fecha_compra,
                "fecha_entrega": c.fecha_entrega,
                "total": float(c.total),
                "numero_orden": c.numero_orden
            } for c in compras
        ]}
    )

@router.get("/compras/proveedor/{proveedor_id}", response_model=ResponseDTO)
def listar_compras_por_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    """Endpoint para listar compras por proveedor (RF04)"""
    compra_manager = CompraManager(db)
    compras = compra_manager.listar_compras_por_proveedor(proveedor_id)
    
    return ResponseDTO(
        success=True,
        message="Compras por proveedor consultadas",
        data={"compras": [
            {
                "id": c.id,
                "fecha_compra": c.fecha_compra,
                "fecha_entrega": c.fecha_entrega,
                "total": float(c.total),
                "estado": c.estado,
                "numero_orden": c.numero_orden
            } for c in compras
        ]}
    )

@router.get("/compras/{compra_id}", response_model=ResponseDTO)
def consultar_compra(compra_id: int, db: Session = Depends(get_db)):
    """Endpoint para consultar compra (RF04)"""
    compra_manager = CompraManager(db)
    compra = compra_manager.consultar_compra(compra_id)
    
    if not compra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compra no encontrada"
        )
    
    return ResponseDTO(
        success=True,
        message="Compra consultada",
        data={
            "id": compra.id,
            "proveedor_id": compra.proveedor_id,
            "fecha_compra": compra.fecha_compra,
            "fecha_entrega": compra.fecha_entrega,
            "total": float(compra.total),
            "estado": compra.estado,
            "numero_orden": compra.numero_orden
        }
    )

@router.put("/compras/{compra_id}/estado", response_model=ResponseDTO)
def actualizar_estado_compra(compra_id: int, estado: str, db: Session = Depends(get_db)):
    """Endpoint para actualizar estado de compra (RF04)"""
    compra_manager = CompraManager(db)
    success = compra_manager.actualizar_estado_compra(compra_id, estado)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compra no encontrada"
        )
    
    return ResponseDTO(
        success=True,
        message=f"Estado de compra actualizado a {estado}"
    )

@router.get("/compras/{compra_id}/total", response_model=ResponseDTO)
def calcular_total_compra(compra_id: int, db: Session = Depends(get_db)):
    """Endpoint para calcular total de compra (RF04)"""
    compra_manager = CompraManager(db)
    total = compra_manager.calcular_total_compra(compra_id)
    
    return ResponseDTO(
        success=True,
        message="Total de compra calculado",
        data={"total": float(total)}
    ) 