let cart = JSON.parse(localStorage.getItem('wallpaper_cart')) || [];

function saveCart() {
    localStorage.setItem('wallpaper_cart', JSON.stringify(cart));
    updateCartCount();
}

function updateCartCount() {
    const countElement = document.getElementById('cart-count');
    if (countElement) {
        countElement.innerText = cart.length;
    }
}

function addToCart(id, type, price, name) {
    // Check if already in cart
    const existing = cart.find(item => item.id === id && item.type === type);
    if (!existing) {
        cart.push({ id, type, price, name });
        saveCart();
        alert(`${name} added to cart!`);
    } else {
        alert(`${name} is already in your cart.`);
    }
}

function removeFromCart(id, type) {
    cart = cart.filter(item => !(item.id === id && item.type === type));
    saveCart();
    renderCart(); // for cart page
}

function renderCart() {
    const container = document.getElementById('cart-container');
    const totalEl = document.getElementById('cart-total');
    const cartDataInput = document.getElementById('cart_data_input');
    const cartTotalInput = document.getElementById('cart_total_input');
    
    if (!container) return;

    if (cart.length === 0) {
        container.innerHTML = '<p>Your cart is empty.</p>';
        if (totalEl) totalEl.innerText = '0.00';
        if (cartDataInput) cartDataInput.value = '';
        if (cartTotalInput) cartTotalInput.value = '0';
        return;
    }

    let html = '<div class="cart-items">';
    let total = 0;

    cart.forEach(item => {
        total += item.price;
        html += `
            <div class="cart-item" style="display: flex; justify-content: space-between; padding: 1.5rem; border-bottom: 1px solid var(--glass-border); align-items: center;">
                <div>
                    <h4 style="color: var(--text-primary); font-size: 1.1rem; margin-bottom: 0.2rem;">${item.name}</h4>
                    <small style="color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; font-size: 0.8rem;">${item.type === 'single' ? 'Wallpaper' : 'Pack'}</small>
                </div>
                <div style="text-align: right; display: flex; align-items: center; gap: 1.5rem;">
                    <div style="font-weight: bold; color: var(--accent-green); font-size: 1.1rem;">₹${item.price}</div>
                    <button class="btn" style="background: rgba(220, 53, 69, 0.2); color: #fecdd3; padding: 0.5rem 1rem; font-size: 0.9rem;" onclick="removeFromCart(${item.id}, '${item.type}')">Remove</button>
                </div>
            </div>
        `;
    });

    html += '</div>';
    container.innerHTML = html;
    
    if (totalEl) totalEl.innerText = total.toFixed(2);
    
    // Update hidden inputs for checkout
    if (cartDataInput) cartDataInput.value = JSON.stringify(cart);
    if (cartTotalInput) cartTotalInput.value = total;
}

document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
    renderCart();
});
