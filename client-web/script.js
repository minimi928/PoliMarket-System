const API_BASE_URL = 'http://localhost:8000';

// Función para mostrar tabs
function showTab(tabName) {
    // Ocultar todos los tabs
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    // Desactivar todos los botones
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => btn.classList.remove('active'));
    
    // Mostrar tab seleccionado
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// Función para hacer peticiones a la API
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        displayApiOutput(data);
        
        if (!response.ok) {
            throw new Error(data.detail || 'Error en la petición');
        }
        
        return data;
    } catch (error) {
        console.error('Error:', error);
        displayApiOutput({ error: error.message });
        throw error;
    }
}

// Función para mostrar respuestas de la API
function displayApiOutput(data) {
    const output = document.getElementById('apiOutput');
    output.textContent = JSON.stringify(data, null, 2);
}

// Función para mostrar resultados en elementos específicos
function displayResult(elementId, data, isError = false) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div class="result ${isError ? 'error' : ''}">
                <strong>${isError ? 'Error:' : 'Resultado:'}</strong><br>
                ${typeof data === 'object' ? JSON.stringify(data, null, 2) : data}
            </div>
        `;
    }
}

// ===== RF01: AUTENTICACIÓN =====

// Login de vendedor
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const result = await apiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        if (result.success) {
            displayResult('loginResult', `Login exitoso para: ${result.data.vendedor.nombre}`);
            // Guardar token para uso posterior
            localStorage.setItem('authToken', result.data.access_token);
        }
    } catch (error) {
        displayResult('loginResult', error.message, true);
    }
});

// Listar vendedores
async function listarVendedores() {
    try {
        const result = await apiCall('/auth/vendedores');
        
        if (result.success && result.data.vendedores) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Email</th>
                            <th>Autorizado</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.vendedores.map(v => `
                            <tr>
                                <td>${v.id}</td>
                                <td>${v.nombre}</td>
                                <td>${v.email}</td>
                                <td>${v.estado_autorizacion ? 'Sí' : 'No'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('vendedoresResult', table);
        }
    } catch (error) {
        displayResult('vendedoresResult', error.message, true);
    }
}

// Consultar vendedores no autorizados
async function consultarVendedoresNoAutorizados() {
    try {
        const result = await apiCall('/auth/vendedores/no-autorizados');
        
        if (result.success && result.data.vendedores) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Email</th>
                            <th>Documento</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.vendedores.map(v => `
                            <tr>
                                <td>${v.id}</td>
                                <td>${v.nombre}</td>
                                <td>${v.email}</td>
                                <td>${v.documento}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('vendedoresResult', table);
        }
    } catch (error) {
        displayResult('vendedoresResult', error.message, true);
    }
}

// ===== RF02: VENTAS =====

// Consultar ventas por vendedor
async function consultarVentasPorVendedor() {
    const vendedorId = document.getElementById('vendedorId').value;
    
    try {
        const result = await apiCall(`/ventas/vendedor/${vendedorId}`);
        
        if (result.success && result.data.ventas) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Cliente ID</th>
                            <th>Fecha</th>
                            <th>Total</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.ventas.map(v => `
                            <tr>
                                <td>${v.id}</td>
                                <td>${v.cliente_id}</td>
                                <td>${v.fecha}</td>
                                <td>$${v.total.toLocaleString()}</td>
                                <td>${v.estado}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('ventasResult', table);
        }
    } catch (error) {
        displayResult('ventasResult', error.message, true);
    }
}

// Listar clientes
async function listarClientes() {
    try {
        const result = await apiCall('/ventas/clientes');
        
        if (result.success && result.data.clientes) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Email</th>
                            <th>Tipo</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.clientes.map(c => `
                            <tr>
                                <td>${c.id}</td>
                                <td>${c.nombre}</td>
                                <td>${c.email}</td>
                                <td>${c.tipo_cliente}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('clientesResult', table);
        }
    } catch (error) {
        displayResult('clientesResult', error.message, true);
    }
}

// ===== RF03: INVENTARIO =====

// Listar productos
async function listarProductos() {
    try {
        const result = await apiCall('/inventario/productos');
        
        if (result.success && result.data.productos) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Descripción</th>
                            <th>Precio</th>
                            <th>Categoría</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.productos.map(p => `
                            <tr>
                                <td>${p.id}</td>
                                <td>${p.nombre}</td>
                                <td>${p.descripcion || 'N/A'}</td>
                                <td>$${p.precio.toLocaleString()}</td>
                                <td>${p.categoria || 'N/A'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('productosResult', table);
        }
    } catch (error) {
        displayResult('productosResult', error.message, true);
    }
}

// Consultar inventario de un producto
async function consultarInventario() {
    const productoId = document.getElementById('productoId').value;
    
    try {
        const result = await apiCall(`/inventario/stock/${productoId}`);
        
        if (result.success && result.data) {
            const info = `
                <strong>Información del Inventario:</strong><br>
                Producto ID: ${result.data.producto_id}<br>
                Cantidad Disponible: ${result.data.cantidad_disponible}<br>
                Cantidad Mínima: ${result.data.cantidad_minima}<br>
                Ubicación: ${result.data.ubicacion || 'N/A'}
            `;
            displayResult('inventarioResult', info);
        }
    } catch (error) {
        displayResult('inventarioResult', error.message, true);
    }
}

// Consultar productos bajo stock
async function consultarProductosBajoStock() {
    try {
        const result = await apiCall('/inventario/bajo-stock');
        
        if (result.success && result.data.productos_bajo_stock) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Producto ID</th>
                            <th>Cantidad Disponible</th>
                            <th>Cantidad Mínima</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.productos_bajo_stock.map(p => `
                            <tr>
                                <td>${p.producto_id}</td>
                                <td>${p.cantidad_disponible}</td>
                                <td>${p.cantidad_minima}</td>
                                <td>${p.cantidad_disponible <= p.cantidad_minima ? 'CRÍTICO' : 'BAJO'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('inventarioResult', table);
        }
    } catch (error) {
        displayResult('inventarioResult', error.message, true);
    }
}

// ===== RF05: ENTREGAS =====

// Listar entregas pendientes
async function listarEntregasPendientes() {
    try {
        const result = await apiCall('/entregas/pendientes');
        
        if (result.success && result.data.entregas) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Venta ID</th>
                            <th>Fecha Entrega</th>
                            <th>Dirección</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.entregas.map(e => `
                            <tr>
                                <td>${e.id}</td>
                                <td>${e.venta_id}</td>
                                <td>${e.fecha_entrega}</td>
                                <td>${e.direccion}</td>
                                <td>${e.estado}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('entregasResult', table);
        }
    } catch (error) {
        displayResult('entregasResult', error.message, true);
    }
}

// Consultar entregas por fecha
async function consultarEntregasPorFecha() {
    const fecha = document.getElementById('fechaEntrega').value;
    
    if (!fecha) {
        displayResult('entregasFechaResult', 'Por favor seleccione una fecha', true);
        return;
    }
    
    try {
        const result = await apiCall(`/entregas/fecha/${fecha}`);
        
        if (result.success && result.data.entregas) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Venta ID</th>
                            <th>Fecha Entrega</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.entregas.map(e => `
                            <tr>
                                <td>${e.id}</td>
                                <td>${e.venta_id}</td>
                                <td>${e.fecha_entrega}</td>
                                <td>${e.estado}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('entregasFechaResult', table);
        } else {
            displayResult('entregasFechaResult', 'No hay entregas programadas para esta fecha');
        }
    } catch (error) {
        displayResult('entregasFechaResult', error.message, true);
    }
}

// ===== RF04: PROVEEDORES =====

// Listar proveedores
async function listarProveedores() {
    try {
        const result = await apiCall('/proveedores/');
        
        if (result.success && result.data.proveedores) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Documento</th>
                            <th>Email</th>
                            <th>Teléfono</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.proveedores.map(p => `
                            <tr>
                                <td>${p.id}</td>
                                <td>${p.nombre}</td>
                                <td>${p.documento}</td>
                                <td>${p.email || 'N/A'}</td>
                                <td>${p.telefono || 'N/A'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('proveedoresResult', table);
        }
    } catch (error) {
        displayResult('proveedoresResult', error.message, true);
    }
}

// Buscar proveedores por nombre
async function buscarProveedores() {
    const nombre = document.getElementById('nombreProveedor').value;
    
    if (!nombre) {
        displayResult('proveedoresResult', 'Por favor ingrese un nombre para buscar', true);
        return;
    }
    
    try {
        const result = await apiCall(`/proveedores/buscar/${nombre}`);
        
        if (result.success && result.data.proveedores) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Documento</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.proveedores.map(p => `
                            <tr>
                                <td>${p.id}</td>
                                <td>${p.nombre}</td>
                                <td>${p.documento}</td>
                                <td>${p.email || 'N/A'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('proveedoresResult', table);
        }
    } catch (error) {
        displayResult('proveedoresResult', error.message, true);
    }
}

// Listar compras pendientes
async function listarComprasPendientes() {
    try {
        const result = await apiCall('/proveedores/compras/pendientes');
        
        if (result.success && result.data.compras) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Proveedor ID</th>
                            <th>Fecha Compra</th>
                            <th>Fecha Entrega</th>
                            <th>Total</th>
                            <th>Número Orden</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.compras.map(c => `
                            <tr>
                                <td>${c.id}</td>
                                <td>${c.proveedor_id}</td>
                                <td>${c.fecha_compra}</td>
                                <td>${c.fecha_entrega}</td>
                                <td>$${c.total.toLocaleString()}</td>
                                <td>${c.numero_orden}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('comprasResult', table);
        }
    } catch (error) {
        displayResult('comprasResult', error.message, true);
    }
}

// Consultar compras por proveedor
async function consultarComprasPorProveedor() {
    const proveedorId = document.getElementById('proveedorIdCompras').value;
    
    try {
        const result = await apiCall(`/proveedores/compras/proveedor/${proveedorId}`);
        
        if (result.success && result.data.compras) {
            const table = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Fecha Compra</th>
                            <th>Fecha Entrega</th>
                            <th>Total</th>
                            <th>Estado</th>
                            <th>Número Orden</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.data.compras.map(c => `
                            <tr>
                                <td>${c.id}</td>
                                <td>${c.fecha_compra}</td>
                                <td>${c.fecha_entrega}</td>
                                <td>$${c.total.toLocaleString()}</td>
                                <td>${c.estado}</td>
                                <td>${c.numero_orden}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            displayResult('comprasResult', table);
        }
    } catch (error) {
        displayResult('comprasResult', error.message, true);
    }
}

// Verificar conexión al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Establecer fecha actual como valor por defecto
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('fechaEntrega').value = today;
    
    // Verificar conexión con el servidor
    apiCall('/health')
        .then(result => {
            if (result && result.status === 'healthy') {
                console.log('✅ Conectado al servidor PoliMarket');
            }
        })
        .catch(error => {
            console.log('❌ Error conectando al servidor:', error.message);
        });
}); 