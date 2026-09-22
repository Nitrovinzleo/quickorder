let cart = JSON.parse(localStorage.getItem('cart')) || [];

document.addEventListener('DOMContentLoaded', () => {
    updateUI();
    setupCartDrawer();
    setupFilters();
    setupCheckout();
    setupAdmin();
});

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateUI();
}

function addToCart(id, name, price) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.quantity += 1;
    } else {
        cart.push({ id: id, name: name, price: parseFloat(price), quantity: 1 });
    }
    saveCart();
    toggleCart(true);
}

function changeQuantity(id, delta) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.quantity += delta;
        if (item.quantity <= 0) {
            cart = cart.filter(i => i.id !== id);
        }
    }
    saveCart();
}

function updateUI() {
    const badge = document.getElementById('cart-badge');
    const container = document.getElementById('cart-items-container');
    const totalEl = document.getElementById('cart-total-price');
    const btn = document.getElementById('cart-checkout-btn');

    const totalCount = cart.reduce((acc, i) => acc + i.quantity, 0);
    const totalPrice = cart.reduce((acc, i) => acc + (i.price * i.quantity), 0);

    if (badge) badge.textContent = totalCount;
    if (totalEl) totalEl.textContent = totalPrice.toFixed(2) + ' €';

    if (container) {
        if (cart.length === 0) {
            container.innerHTML = '<p class="text-muted" style="text-align:center; padding: 2rem 0;">Votre panier est vide.</p>';
            if (btn) btn.style.opacity = '0.5';
            if (btn) btn.style.pointerEvents = 'none';
        } else {
            if (btn) btn.style.opacity = '1';
            if (btn) btn.style.pointerEvents = 'auto';

            container.innerHTML = cart.map(item => `
                <div class="cart-item">
                    <div class="cart-item-info">
                        <h4>${escapeHtml(item.name)}</h4>
                        <span>${item.price.toFixed(2)} €</span>
                    </div>
                    <div class="cart-qty-ctrl">
                        <button class="qty-btn" onclick="changeQuantity(${item.id}, -1)">-</button>
                        <span>${item.quantity}</span>
                        <button class="qty-btn" onclick="changeQuantity(${item.id}, 1)">+</button>
                    </div>
                </div>
            `).join('');
        }
    }

    const summary = document.getElementById('checkout-summary-items');
    const checkTotal = document.getElementById('checkout-total-price');
    if (summary) {
        if (cart.length === 0) {
            summary.innerHTML = '<p class="text-muted">Aucun article dans le panier.</p>';
        } else {
            summary.innerHTML = cart.map(item => `
                <div style="display:flex; justify-between: space-between; margin-bottom:0.5rem;">
                    <span>${item.quantity}x ${escapeHtml(item.name)}</span>
                    <strong>${(item.price * item.quantity).toFixed(2)} €</strong>
                </div>
            `).join('');
        }
    }
    if (checkTotal) checkTotal.textContent = totalPrice.toFixed(2) + ' €';
}

function setupCartDrawer() {
    const openBtn = document.getElementById('open-cart-btn');
    const closeBtn = document.getElementById('close-cart-btn');
    const overlay = document.getElementById('cart-overlay');

    if (openBtn) openBtn.onclick = () => toggleCart(true);
    if (closeBtn) closeBtn.onclick = () => toggleCart(false);
    if (overlay) overlay.onclick = () => toggleCart(false);
}

function toggleCart(open) {
    const drawer = document.getElementById('cart-drawer');
    const overlay = document.getElementById('cart-overlay');
    if (drawer && overlay) {
        drawer.classList.toggle('open', open);
        overlay.classList.toggle('open', open);
    }
}

function setupFilters() {
    const btns = document.querySelectorAll('.pill-btn');
    const cards = document.querySelectorAll('.menu-card');

    btns.forEach(b => {
        b.addEventListener('click', () => {
            btns.forEach(x => x.classList.remove('active'));
            b.classList.add('active');

            const cat = b.dataset.category;
            cards.forEach(card => {
                if (cat === 'all' || card.dataset.category === cat) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

function setupCheckout() {
    const form = document.getElementById('checkout-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (cart.length === 0) {
            alert('Votre panier est vide');
            return;
        }

        const payload = {
            customer_name: document.getElementById('customer_name').value,
            customer_email: document.getElementById('customer_email').value,
            customer_phone: document.getElementById('customer_phone').value,
            order_type: document.getElementById('order_type').value,
            cart: cart
        };

        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;

        try {
            const res = await fetch('/api/orders', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            if (res.ok) {
                cart = [];
                localStorage.removeItem('cart');
                window.location.href = `/confirmation/${data.order_id}`;
            } else {
                alert(data.error || 'Erreur lors de la commande');
                submitBtn.disabled = false;
            }
        } catch (err) {
            alert('Erreur réseau');
            submitBtn.disabled = false;
        }
    });
}

function setupAdmin() {
    document.querySelectorAll('.admin-status-select').forEach(select => {
        select.addEventListener('change', async () => {
            const id = select.dataset.orderId;
            const status = select.value;

            try {
                const res = await fetch(`/api/orders/${id}/status`, {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status })
                });
                if (res.ok) location.reload();
            } catch (e) {
                console.error(e);
            }
        });
    });
}

function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
