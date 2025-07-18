from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.schemas import ProductoCreate, InventarioCreate, ResponseDTO
from ..components.inventario_manager import InventarioManager, ProductoManager

router = APIRouter(prefix="/inventario", tags=["Inventario"])

@router.get("/productos", response_model=ResponseDTO)
def listar_productos(db: Session = Depends(get_db)):
    """Endpoint para listar productos disponibles (RF03)"""
    producto_manager = ProductoManager(db)
    productos = producto_manager.listar_productos()
    
    return ResponseDTO(
        success=True,
        message="Productos consultados",
        data={"productos": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "descripcion": p.descripcion,
                "precio": float(p.precio),
                "categoria": p.categoria
            } for p in productos
        ]}
    )

@router.get("/productos/{producto_id}", response_model=ResponseDTO)
def consultar_producto(producto_id: int, db: Session = Depends(get_db)):
    """Endpoint para consultar producto específico (RF03)"""
    producto_manager = ProductoManager(db)
    producto = producto_manager.consultar_producto(producto_id)
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    return ResponseDTO(
        success=True,
        message="Producto consultado",
        data={
            "id": producto.id,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": float(producto.precio),
            "categoria": producto.categoria
        }
    )

@router.get("/productos/categoria/{categoria}", response_model=ResponseDTO)
def buscar_productos_por_categoria(categoria: str, db: Session = Depends(get_db)):
    """Endpoint para buscar productos por categoría (RF03)"""
    producto_manager = ProductoManager(db)
    productos = producto_manager.buscar_productos_por_categoria(categoria)
    
    return ResponseDTO(
        success=True,
        message=f"Productos de categoría {categoria} consultados",
        data={"productos": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "precio": float(p.precio),
                "categoria": p.categoria
            } for p in productos
        ]}
    )

@router.get("/disponibilidad/{producto_id}/{cantidad}", response_model=ResponseDTO)
def verificar_disponibilidad(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    """Endpoint para verificar disponibilidad de producto (RF03)"""
    inventario_manager = InventarioManager(db)
    disponible = inventario_manager.verificar_disponibilidad(producto_id, cantidad)
    
    return ResponseDTO(
        success=True,
        message="Disponibilidad verificada",
        data={
            "producto_id": producto_id,
            "cantidad_solicitada": cantidad,
            "disponible": disponible
        }
    )

@router.get("/stock/{producto_id}", response_model=ResponseDTO)
def consultar_inventario_producto(producto_id: int, db: Session = Depends(get_db)):
    """Endpoint para consultar inventario de un producto (RF03)"""
    inventario_manager = InventarioManager(db)
    inventario = inventario_manager.consultar_inventario(producto_id)
    
    if not inventario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventario no encontrado para este producto"
        )
    
    return ResponseDTO(
        success=True,
        message="Inventario consultado",
        data={
            "producto_id": inventario.producto_id,
            "cantidad_disponible": inventario.cantidad_disponible,
            "cantidad_minima": inventario.cantidad_minima,
            "ubicacion": inventario.ubicacion
        }
    )

@router.get("/bajo-stock", response_model=ResponseDTO)
def consultar_productos_bajo_stock(db: Session = Depends(get_db)):
    """Endpoint para consultar productos con stock bajo (RF03)"""
    inventario_manager = InventarioManager(db)
    productos_bajo_stock = inventario_manager.consultar_productos_bajo_stock()
    
    return ResponseDTO(
        success=True,
        message="Productos con stock bajo consultados",
        data={"productos_bajo_stock": [
            {
                "producto_id": inv.producto_id,
                "cantidad_disponible": inv.cantidad_disponible,
                "cantidad_minima": inv.cantidad_minima
            } for inv in productos_bajo_stock
        ]}
    )

@router.post("/productos", response_model=ResponseDTO)
def crear_producto(producto_data: ProductoCreate, db: Session = Depends(get_db)):
    """Endpoint para crear producto (RF03)"""
    producto_manager = ProductoManager(db)
    producto = producto_manager.crear_producto(producto_data)
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creando producto"
        )
    
    return ResponseDTO(
        success=True,
        message="Producto creado exitosamente",
        data={"producto_id": producto.id}
    )

@router.post("/stock/{producto_id}", response_model=ResponseDTO)
def actualizar_stock(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    """Endpoint para actualizar stock de un producto (RF03)"""
    inventario_manager = InventarioManager(db)
    success = inventario_manager.actualizar_stock(producto_id, cantidad)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error actualizando stock"
        )
    
    return ResponseDTO(
        success=True,
        message="Stock actualizado exitosamente",
        data={
            "producto_id": producto_id,
            "cantidad_agregada": cantidad
        }
    ) 