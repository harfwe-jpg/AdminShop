/*
 * Sistema POS - JavaScript Principal
 * Maneja ventas, búsqueda de productos, carrito y más
 */

// ==================== VARIABLES GLOBALES ====================
let cart = [];
let currentPaymentMethod = 'efectivo';
let lastSearchResults = []; // Almacena temporalmente los resultados de búsqueda para evitar conflictos con comillas

// ==================== INICIALIZACIÓN ====================
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.sales-page')) {
        initSalesPage();
    }

    if (document.querySelector('.products-page')) {
        initProductsPage();
    }

    initMobileMenu();
});

// ==================== MENÚ MÓVIL ====================
function initMobileMenu() {
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (menuBtn && navLinks) {
        menuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
}

// ==================== PÁGINA DE VENTAS ====================
function initSalesPage() {
    const productSearch = document.getElementById('product-search');
    const barcodeSearch = document.getElementById('barcode-search');
    const completeSaleBtn = document.getElementById('complete-sale-btn');

    if (productSearch) {
        productSearch.addEventListener('input', debounce(function() {
            searchProducts(this.value);
        }, 300));
    }

    if (barcodeSearch) {
        barcodeSearch.addEventListener('input', debounce(function() {
            searchProducts(this.value);
        }, 300));

        barcodeSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && this.value.trim()) {
                searchProducts(this.value, true);
                this.value = '';
            }
        });
    }

    document.querySelectorAll('.bill-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const value = parseFloat(this.dataset.value);
            const cashInput = document.getElementById('cash-received');
            const currentValue = parseFloat(cashInput.value) || 0;
            cashInput.value = (currentValue + value).toFixed(2);
            updateChange();
        });
    });

    const cashInput = document.getElementById('cash-received');
    if (cashInput) {
        cashInput.addEventListener('input', updateChange);
    }

    document.querySelectorAll('.payment-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.payment-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentPaymentMethod = this.dataset.method;

            const calculator = document.getElementById('cash-calculator');
            if (currentPaymentMethod === 'efectivo') {
                calculator.style.display = 'block';
            } else {
                calculator.style.display = 'none';
            }
        });
    });

    if (completeSaleBtn) {
        completeSaleBtn.addEventListener('click', completeSale);
    }
}

// Búsqueda de productos
async function searchProducts(query, autoAdd = false) {
    if (!query.trim()) {
        document.getElementById('search-results').innerHTML = '';
        lastSearchResults = [];
        return;
    }

    try {
        const response = await fetch(`/api/products/search?q=${encodeURIComponent(query)}`);
        const products = await response.json();
        
        lastSearchResults = products; // Guardamos en memoria de forma segura
        const resultsDiv = document.getElementById('search-results');

        if (products.length === 0) {
            resultsDiv.innerHTML = '<div class="empty-state">No se encontraron productos</div>';
            return;
        }

        // Renderizamos usando el índice del arreglo para evitar errores de sintaxis por comillas en nombres
        resultsDiv.innerHTML = products.map((product, index) => `
            <div class="search-result-item" onclick="addByIndex(${index}, ${autoAdd})">
                <div>
                    <strong>${product.name}</strong>
                    <div class="cart-item-details">Stock: ${product.stock} ${product.type}(s) | $${product.price.toFixed(2)}</div>
                </div>
                <span class="btn btn-sm btn-primary">Agregar</span>
            </div>
        `).join('');

        if (autoAdd && products.length === 1) {
            addByIndex(0, true);
        }
    } catch (error) {
        console.error('Error al buscar productos:', error);
    }
}

// Función para agregar al carrito de forma segura usando el índice de la búsqueda
function addByIndex(index, autoAdd = false) {
    const product = lastSearchResults[index];
    if (product) {
        addToCart(product.id, product.name, product.price, product.stock, product.type, autoAdd);
    }
}

// Agregar al carrito
function addToCart(productId, productName, price, stock, type, autoAdd = false) {
    const existingItem = cart.find(item => item.product_id === productId);
    const currentQty = existingItem ? existingItem.quantity : 0;

    if (currentQty + 1 > stock) {
        alert('No hay suficiente stock disponible');
        return;
    }

    if (existingItem) {
        existingItem.quantity++;
        existingItem.subtotal = existingItem.quantity * existingItem.price;
    } else {
        cart.push({
            product_id: productId, // <--- Clave correcta requerida por app.py
            name: productName,
            price: price,
            type: type,
            quantity: 1,
            subtotal: price
        });
    }

    updateCart();

    if (autoAdd) {
        document.getElementById('barcode-search').value = '';
        document.getElementById('search-results').innerHTML = '';
        lastSearchResults = [];
    }
}

// Actualizar carrito
function updateCart() {
    const cartItemsDiv = document.getElementById('cart-items');
    const totalAmountSpan = document.getElementById('cart-total-amount');
    const paymentTotalSpan = document.getElementById('payment-total');

    if (cart.length === 0) {
        cartItemsDiv.innerHTML = '<p class="empty-cart">El carrito está vacío</p>';
        totalAmountSpan.textContent = '$0.00';
        paymentTotalSpan.textContent = '$0.00';
        updateChange();
        return;
    }

    cartItemsDiv.innerHTML = cart.map((item, index) => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-details">
                    ${item.quantity} ${item.type}(s) × $${item.price.toFixed(2)}
                </div>
            </div>
            <div>
                <span>$${item.subtotal.toFixed(2)}</span>
                <button class="cart-item-remove" onclick="removeFromCart(${index})">🗑️</button>
            </div>
        </div>
    `).join('');

    const total = cart.reduce((sum, item) => sum + item.subtotal, 0);
    totalAmountSpan.textContent = `$${total.toFixed(2)}`;
    paymentTotalSpan.textContent = `$${total.toFixed(2)}`;
    updateChange();
}

// Eliminar del carrito
function removeFromCart(index) {
    cart.splice(index, 1);
    updateCart();
}

// Actualizar cambio
function updateChange() {
    const total = cart.reduce((sum, item) => sum + item.subtotal, 0);
    const cashReceived = parseFloat(document.getElementById('cash-received')?.value) || 0;
    const changeDisplay = document.getElementById('change-display');
    const changeAmount = document.getElementById('change-amount');

    if (currentPaymentMethod === 'efectivo' && cashReceived > 0) {
        const change = cashReceived - total;
        if (change >= 0) {
            changeDisplay.style.display = 'block';
            changeAmount.textContent = `$${change.toFixed(2)}`;
        } else {
            changeDisplay.style.display = 'none';
        }
    } else {
        changeDisplay.style.display = 'none';
    }
}

// Completar venta
async function completeSale() {
    if (cart.length === 0) {
        alert('El carrito está vacío');
        return;
    }

    const total = cart.reduce((sum, item) => sum + item.subtotal, 0);
    let cashReceived = 0;

    if (currentPaymentMethod === 'efectivo') {
        cashReceived = parseFloat(document.getElementById('cash-received')?.value) || 0;
        if (cashReceived < total) {
            alert('La cantidad recibida es menor al total');
            return;
        }
    }

    try {
        const response = await fetch('/api/sales', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                items: cart,
                payment_method: currentPaymentMethod,
                cash_received: cashReceived
            })
        });

        const result = await response.json();

        if (result.success) {
            document.getElementById('modal-total').textContent = `$${result.total.toFixed(2)}`;

            const changeRow = document.getElementById('modal-change-row');
            if (result.change > 0) {
                changeRow.style.display = 'block';
                document.getElementById('modal-change').textContent = `$${result.change.toFixed(2)}`;
            } else {
                changeRow.style.display = 'none';
            }

            document.getElementById('sale-modal').style.display = 'flex';

            cart = [];
            updateCart();
            document.getElementById('cash-received').value = '';
        } else {
            alert('Error al realizar la venta: ' + (result.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión. Intenta nuevamente.');
    }
}

// Cerrar modal de venta
function closeSaleModal() {
    document.getElementById('sale-modal').style.display = 'none';
}

// ==================== PÁGINA DE PRODUCTOS ====================
function initProductsPage() {
    const publicPriceInput = document.getElementById('public_price');
    const supplierPriceInput = document.getElementById('supplier_price');
    const profitMarginSpan = document.getElementById('profit-margin');

    if (publicPriceInput && supplierPriceInput && profitMarginSpan) {
        [publicPriceInput, supplierPriceInput].forEach(input => {
            input.addEventListener('input', function() {
                const publicPrice = parseFloat(publicPriceInput.value) || 0;
                const supplierPrice = parseFloat(supplierPriceInput.value) || 0;

                if (supplierPrice > 0) {
                    const margin = ((publicPrice - supplierPrice) / supplierPrice) * 100;
                    profitMarginSpan.textContent = `Margen: ${margin.toFixed(1)}%`;

                    if (margin < 0) {
                        profitMarginSpan.style.color = 'var(--danger-color)';
                    } else if (margin < 20) {
                        profitMarginSpan.style.color = 'var(--warning-color)';
                    } else {
                        profitMarginSpan.style.color = 'var(--success-color)';
                    }
                } else {
                    profitMarginSpan.textContent = 'Margen: --%';
                    profitMarginSpan.style.color = 'var(--text-muted)';
                }
            });
        });
    }
}

// Editar producto
async function editProduct(productId) {
    try {
        const response = await fetch(`/api/products/${productId}`);
        const product = await response.json();

        document.getElementById('product-id').value = product.id;
        document.getElementById('barcode').value = product.barcode;
        document.getElementById('name').value = product.name;
        document.getElementById('product_type').value = product.product_type;
        document.getElementById('stock').value = product.stock;
        document.getElementById('public_price').value = product.public_price;
        document.getElementById('supplier_price').value = product.supplier_price;

        document.getElementById('form-title').textContent = '✏️ Editar Producto';
        document.getElementById('save-btn').textContent = 'Actualizar Producto';
        document.getElementById('cancel-btn').style.display = 'inline-block';

        document.getElementById('product-form').scrollIntoView({ behavior: 'smooth' });

        const profitMarginSpan = document.getElementById('profit-margin');
        if (profitMarginSpan && product.supplier_price > 0) {
            const margin = ((product.public_price - product.supplier_price) / product.supplier_price) * 100;
            profitMarginSpan.textContent = `Margen: ${margin.toFixed(1)}%`;
        }
    } catch (error) {
        console.error('Error al cargar producto:', error);
        alert('Error al cargar producto');
    }
}

// Cancelar edición
document.getElementById('cancel-btn')?.addEventListener('click', function() {
    document.getElementById('product-form').reset();
    document.getElementById('product-id').value = '';
    document.getElementById('form-title').textContent = '📦 Agregar Producto';
    document.getElementById('save-btn').textContent = 'Guardar Producto';
    this.style.display = 'none';
    document.getElementById('profit-margin').textContent = 'Margen: --%';
});

// ==================== RESPALDO DE BASE DE DATOS ====================
async function createBackup() {
    try {
        const response = await fetch('/api/backup', {
            method: 'POST'
        });

        const result = await response.json();

        if (result.success) {
            alert('✅ Respaldo creado exitosamente en la carpeta backups/');
        } else {
            alert('❌ Error al crear respaldo: ' + (result.message || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión al crear respaldo');
    }
}

// ==================== UTILIDADES ====================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ==================== API CALLS ====================
async function getLowStockProducts() {
    try {
        const response = await fetch('/api/products/low-stock');
        const products = await response.json();
        return products;
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}
