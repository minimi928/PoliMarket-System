import requests
import json
from datetime import date

class PoliMarketConsoleClient:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.session = requests.Session()
        self.auth_token = None
    
    def api_call(self, endpoint, method="GET", data=None):
        """Realizar llamada a la API"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            if method == "GET":
                response = self.session.get(url, headers=headers)
            elif method == "POST":
                response = self.session.post(url, headers=headers, json=data)
            elif method == "PUT":
                response = self.session.put(url, headers=headers, json=data)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la petición: {e}")
            return None
    
    def login(self, email, password):
        """Login de vendedor (RF01)"""
        data = {"email": email, "password": password}
        result = self.api_call("/auth/login", method="POST", data=data)
        
        if result and result.get("success"):
            self.auth_token = result["data"]["access_token"]
            print(f"✅ Login exitoso para: {result['data']['vendedor']['nombre']}")
            return True
        else:
            print("❌ Error en el login")
            return False
    
    def listar_productos(self):
        """Listar productos disponibles (RF03)"""
        result = self.api_call("/inventario/productos")
        
        if result and result.get("success"):
            print("\n📦 PRODUCTOS DISPONIBLES:")
            print("-" * 80)
            for producto in result["data"]["productos"]:
                print(f"ID: {producto['id']} | {producto['nombre']} | ${producto['precio']:,.0f} | {producto['categoria']}")
        else:
            print("❌ Error consultando productos")
    
    def consultar_inventario(self, producto_id):
        """Consultar inventario de un producto (RF03)"""
        result = self.api_call(f"/inventario/stock/{producto_id}")
        
        if result and result.get("success"):
            data = result["data"]
            print(f"\n📊 INVENTARIO DEL PRODUCTO {producto_id}:")
            print("-" * 50)
            print(f"Cantidad Disponible: {data['cantidad_disponible']}")
            print(f"Cantidad Mínima: {data['cantidad_minima']}")
            print(f"Ubicación: {data['ubicacion']}")
        else:
            print("❌ Error consultando inventario")
    
    def consultar_ventas_vendedor(self, vendedor_id):
        """Consultar ventas por vendedor (RF02)"""
        result = self.api_call(f"/ventas/vendedor/{vendedor_id}")
        
        if result and result.get("success"):
            ventas = result["data"]["ventas"]
            print(f"\n💰 VENTAS DEL VENDEDOR {vendedor_id}:")
            print("-" * 80)
            if ventas:
                for venta in ventas:
                    print(f"ID: {venta['id']} | Cliente: {venta['cliente_id']} | Fecha: {venta['fecha']} | Total: ${venta['total']:,.0f} | Estado: {venta['estado']}")
            else:
                print("No hay ventas registradas para este vendedor")
        else:
            print("❌ Error consultando ventas")
    
    def listar_entregas_pendientes(self):
        """Listar entregas pendientes (RF05)"""
        result = self.api_call("/entregas/pendientes")
        
        if result and result.get("success"):
            entregas = result["data"]["entregas"]
            print(f"\n🚚 ENTREGAS PENDIENTES:")
            print("-" * 80)
            if entregas:
                for entrega in entregas:
                    print(f"ID: {entrega['id']} | Venta: {entrega['venta_id']} | Fecha: {entrega['fecha_entrega']} | Estado: {entrega['estado']}")
            else:
                print("No hay entregas pendientes")
        else:
            print("❌ Error consultando entregas")
    
    def consultar_entregas_por_fecha(self, fecha):
        """Consultar entregas por fecha (RF05)"""
        result = self.api_call(f"/entregas/fecha/{fecha}")
        
        if result and result.get("success"):
            entregas = result["data"]["entregas"]
            print(f"\n📅 ENTREGAS DEL {fecha}:")
            print("-" * 80)
            if entregas:
                for entrega in entregas:
                    print(f"ID: {entrega['id']} | Venta: {entrega['venta_id']} | Fecha: {entrega['fecha_entrega']} | Estado: {entrega['estado']}")
            else:
                print("No hay entregas programadas para esta fecha")
        else:
            print("❌ Error consultando entregas por fecha")
    
    def listar_proveedores(self):
        """Listar proveedores (RF04)"""
        result = self.api_call("/proveedores/")
        
        if result and result.get("success"):
            proveedores = result["data"]["proveedores"]
            print(f"\n🏢 PROVEEDORES:")
            print("-" * 80)
            if proveedores:
                for proveedor in proveedores:
                    print(f"ID: {proveedor['id']} | {proveedor['nombre']} | {proveedor['documento']} | {proveedor['email'] or 'N/A'}")
            else:
                print("No hay proveedores registrados")
        else:
            print("❌ Error consultando proveedores")
    
    def buscar_proveedores(self, nombre):
        """Buscar proveedores por nombre (RF04)"""
        result = self.api_call(f"/proveedores/buscar/{nombre}")
        
        if result and result.get("success"):
            proveedores = result["data"]["proveedores"]
            print(f"\n🔍 RESULTADOS DE BÚSQUEDA PARA '{nombre}':")
            print("-" * 80)
            if proveedores:
                for proveedor in proveedores:
                    print(f"ID: {proveedor['id']} | {proveedor['nombre']} | {proveedor['documento']} | {proveedor['email'] or 'N/A'}")
            else:
                print("No se encontraron proveedores con ese nombre")
        else:
            print("❌ Error buscando proveedores")
    
    def listar_compras_pendientes(self):
        """Listar compras pendientes (RF04)"""
        result = self.api_call("/proveedores/compras/pendientes")
        
        if result and result.get("success"):
            compras = result["data"]["compras"]
            print(f"\n📋 COMPRAS PENDIENTES:")
            print("-" * 80)
            if compras:
                for compra in compras:
                    print(f"ID: {compra['id']} | Proveedor: {compra['proveedor_id']} | Fecha: {compra['fecha_compra']} | Total: ${compra['total']:,.0f} | Orden: {compra['numero_orden']}")
            else:
                print("No hay compras pendientes")
        else:
            print("❌ Error consultando compras")
    
    def consultar_compras_proveedor(self, proveedor_id):
        """Consultar compras por proveedor (RF04)"""
        result = self.api_call(f"/proveedores/compras/proveedor/{proveedor_id}")
        
        if result and result.get("success"):
            compras = result["data"]["compras"]
            print(f"\n📋 COMPRAS DEL PROVEEDOR {proveedor_id}:")
            print("-" * 80)
            if compras:
                for compra in compras:
                    print(f"ID: {compra['id']} | Fecha: {compra['fecha_compra']} | Total: ${compra['total']:,.0f} | Estado: {compra['estado']} | Orden: {compra['numero_orden']}")
            else:
                print("No hay compras registradas para este proveedor")
        else:
            print("❌ Error consultando compras del proveedor")
    
    def crear_venta(self, vendedor_id, cliente_id, productos):
        """Crear una venta (RF02)"""
        data = {
            "vendedor_id": vendedor_id,
            "cliente_id": cliente_id,
            "fecha": date.today().isoformat(),
            "detalles": productos
        }
        
        result = self.api_call("/ventas/", method="POST", data=data)
        
        if result and result.get("success"):
            print(f"✅ Venta creada exitosamente")
            print(f"ID de Venta: {result['data']['venta_id']}")
            print(f"Total: ${result['data']['total']:,.0f}")
        else:
            print("❌ Error creando venta")
    
    def mostrar_menu(self):
        """Mostrar menú principal"""
        print("\n" + "="*60)
        print("           POLIMARKET - CLIENTE DE CONSOLA")
        print("="*60)
        print("1. Login de Vendedor")
        print("2. Listar Productos")
        print("3. Consultar Inventario")
        print("4. Consultar Ventas por Vendedor")
        print("5. Listar Entregas Pendientes")
        print("6. Consultar Entregas por Fecha")
        print("7. Crear Venta")
        print("8. Listar Proveedores")
        print("9. Buscar Proveedores")
        print("10. Listar Compras Pendientes")
        print("11. Consultar Compras por Proveedor")
        print("12. Salir")
        print("-"*60)
    
    def ejecutar(self):
        """Ejecutar el cliente de consola"""
        print("🚀 Iniciando Cliente de Consola PoliMarket...")
        
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                email = input("Email: ").strip()
                password = input("Contraseña: ").strip()
                self.login(email, password)
            
            elif opcion == "2":
                self.listar_productos()
            
            elif opcion == "3":
                producto_id = input("ID del producto: ").strip()
                try:
                    self.consultar_inventario(int(producto_id))
                except ValueError:
                    print("❌ ID de producto inválido")
            
            elif opcion == "4":
                vendedor_id = input("ID del vendedor: ").strip()
                try:
                    self.consultar_ventas_vendedor(int(vendedor_id))
                except ValueError:
                    print("❌ ID de vendedor inválido")
            
            elif opcion == "5":
                self.listar_entregas_pendientes()
            
            elif opcion == "6":
                if not self.auth_token:
                    print("❌ Debe hacer login primero")
                    continue
                
                fecha = input("Fecha (YYYY-MM-DD): ").strip()
                try:
                    self.consultar_entregas_por_fecha(fecha)
                except ValueError:
                    print("❌ Formato de fecha inválido (YYYY-MM-DD)")
            
            elif opcion == "7":
                if not self.auth_token:
                    print("❌ Debe hacer login primero")
                    continue
                
                vendedor_id = input("ID del vendedor: ").strip()
                cliente_id = input("ID del cliente: ").strip()
                
                productos = []
                while True:
                    producto_id = input("ID del producto (o 'fin' para terminar): ").strip()
                    if producto_id.lower() == 'fin':
                        break
                    cantidad = input("Cantidad: ").strip()
                    try:
                        productos.append({
                            "producto_id": int(producto_id),
                            "cantidad": int(cantidad)
                        })
                    except ValueError:
                        print("❌ Valores inválidos")
                
                if productos:
                    try:
                        self.crear_venta(int(vendedor_id), int(cliente_id), productos)
                    except ValueError:
                        print("❌ IDs inválidos")
                else:
                    print("❌ No se especificaron productos")
            
            elif opcion == "8":
                self.listar_proveedores()
            
            elif opcion == "9":
                nombre = input("Nombre del proveedor: ").strip()
                if nombre:
                    self.buscar_proveedores(nombre)
                else:
                    print("❌ Debe ingresar un nombre")
            
            elif opcion == "10":
                self.listar_compras_pendientes()
            
            elif opcion == "11":
                proveedor_id = input("ID del proveedor: ").strip()
                try:
                    self.consultar_compras_proveedor(int(proveedor_id))
                except ValueError:
                    print("❌ ID de proveedor inválido")
            
            elif opcion == "12":
                print("👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción inválida")
            
            input("\nPresione Enter para continuar...")

def main():
    client = PoliMarketConsoleClient()
    
    # Verificar conexión
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Conectado al servidor PoliMarket")
        else:
            print("❌ Error conectando al servidor")
            return
    except:
        print("❌ No se pudo conectar al servidor. Asegúrate de que esté ejecutándose en http://localhost:8000")
        return
    
    client.ejecutar()

if __name__ == "__main__":
    main() 