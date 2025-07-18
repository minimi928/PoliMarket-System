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
        print("6. Crear Venta")
        print("7. Salir")
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
                
                try:
                    vendedor_id = int(input("ID del vendedor: ").strip())
                    cliente_id = int(input("ID del cliente: ").strip())
                    
                    productos = []
                    while True:
                        producto_id = input("ID del producto (0 para terminar): ").strip()
                        if producto_id == "0":
                            break
                        
                        cantidad = int(input("Cantidad: ").strip())
                        productos.append({
                            "producto_id": int(producto_id),
                            "cantidad": cantidad
                        })
                    
                    if productos:
                        self.crear_venta(vendedor_id, cliente_id, productos)
                    else:
                        print("❌ Debe agregar al menos un producto")
                        
                except ValueError:
                    print("❌ Datos inválidos")
            
            elif opcion == "7":
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