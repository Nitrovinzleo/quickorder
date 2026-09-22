from flask import Blueprint, render_template, request, jsonify
from . import db
from .models import Category, MenuItem, Order, OrderItem

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@bp.route('/checkout')
def checkout():
    return render_template('checkout.html')

@bp.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('confirmation.html', order=order)

@bp.route('/admin')
def admin():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin.html', orders=orders)

# API
@bp.route('/api/categories')
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])

@bp.route('/api/items')
def get_items():
    items = MenuItem.query.filter_by(is_available=True).all()
    return jsonify([i.to_dict() for i in items])

@bp.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])

@bp.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json() or {}

    name = data.get('customer_name', '').strip()
    email = data.get('customer_email', '').strip()
    phone = data.get('customer_phone', '').strip()
    order_type = data.get('order_type', 'takeaway')
    cart_items = data.get('cart', [])

    if not name or not email or not phone or not cart_items:
        return jsonify({'error': 'Veuillez remplir tous les champs du formulaire.'}), 400

    order = Order(
        customer_name=name,
        customer_email=email,
        customer_phone=phone,
        order_type=order_type,
        status='pending',
        total_amount=0.0
    )
    db.session.add(order)
    db.session.flush()

    total = 0.0
    for item in cart_items:
        menu_item = MenuItem.query.get(item.get('id'))
        if not menu_item or not menu_item.is_available:
            continue
        
        qty = int(item.get('quantity', 1))
        total += menu_item.price * qty

        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=qty,
            unit_price=menu_item.price
        )
        db.session.add(order_item)

    order.total_amount = round(total, 2)
    db.session.commit()

    return jsonify({'order_id': order.id, 'message': 'Commande valide'}), 201

@bp.route('/api/orders/<int:order_id>/status', methods=['PATCH'])
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json() or {}
    new_status = data.get('status')

    if new_status in ['pending', 'preparing', 'ready', 'completed', 'cancelled']:
        order.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'status': order.status})

    return jsonify({'error': 'Statut invalide'}), 400
