from app import create_app, db
from app.models import Category, MenuItem, Order, OrderItem

app = create_app()

def run_seed():
    with app.app_context():
        print("Reset de la base de donnees...")
        db.drop_all()
        db.create_all()

        burgers = Category(name="Burgers", slug="burgers", icon="burger")
        pizzas = Category(name="Pizzas", slug="pizzas", icon="pizza-slice")
        boissons = Category(name="Boissons", slug="boissons", icon="wine-glass")
        desserts = Category(name="Desserts", slug="desserts", icon="cookie")

        db.session.add_all([burgers, pizzas, boissons, desserts])
        db.session.commit()

        items = [
            MenuItem(
                category_id=burgers.id,
                name="Quick Cheese Supreme",
                description="Double steak hache 100% pur boeuf, cheddar fondu, sauce maison, cornichons et salade.",
                price=11.90,
                image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&auto=format&fit=crop&q=80"
            ),
            MenuItem(
                category_id=burgers.id,
                name="Smokey Bacon BBQ",
                description="Steak boeuf fume, bacon croustillant, oignons confits et sauce BBQ.",
                price=13.50,
                image_url="https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=500&auto=format&fit=crop&q=80"
            ),
            MenuItem(
                category_id=burgers.id,
                name="Crispy Chicken Spicy",
                description="Filet de poulet pane croustillant, jalapenos, mayo spicy et salade.",
                price=10.90,
                image_url="https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?w=500&auto=format&fit=crop&q=80"
            ),
            MenuItem(
                category_id=pizzas.id,
                name="Pizza Margherita Royale",
                description="Sauce tomate San Marzano, mozzarella fior di latte, basilic frais.",
                price=12.00,
                image_url="https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=500&auto=format&fit=crop&q=80"
            ),
            MenuItem(
                category_id=pizzas.id,
                name="Pizza Pepperoni Inferno",
                description="Mozzarella, pepperoni piquant, origan et miel pimente.",
                price=14.50,
                image_url="https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?w=500&auto=format&fit=crop&q=80"
            ),
            MenuItem(
                category_id=pizzas.id,
                name="Pizza 4 Fromages Gourmet",
                description="Creme fraiche, mozzarella, gorgonzola AOP, chevre et parmesan.",
                price=14.00,
                image_url="https://images.unsplash.com/photo-1573821663912-569905455b1c?w=500&auto=format&fit=crop&q=80"
            ),
            MenuItem(
                category_id=boissons.id,
                name="Coca-Cola Zero 33cl",
                description="Boisson rafraichissante aux extraits de vegetaux, 33cl.",
                price=3.00,
                image_url="https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&auto=format&fit=crop&q=80"
            ),
            MenuItem(
                category_id=boissons.id,
                name="Limonade Artisanale 50cl",
                description="Citrons presses bio, menthe fraiche et eau petillante.",
                price=4.50,
                image_url="https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500&auto=format&fit=crop&q=80"
            ),
            MenuItem(
                category_id=desserts.id,
                name="Tiramisu Speculoos",
                description="Mascarpone onctueux, biscuits speculoos et cacao noir.",
                price=5.50,
                image_url="https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=500&auto=format&fit=crop&q=80"
            ),
            MenuItem(
                category_id=desserts.id,
                name="Fondant au Chocolat",
                description="Chocolat noir 70% et sa boule de glace vanille.",
                price=6.00,
                image_url="https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500&auto=format&fit=crop&q=80"
            )
        ]

        db.session.add_all(items)
        db.session.commit()

        # Commande test
        demo_order = Order(
            customer_name="Alice Martin",
            customer_email="alice@example.com",
            customer_phone="0611223344",
            order_type="takeaway",
            status="preparing",
            total_amount=26.40
        )
        db.session.add(demo_order)
        db.session.flush()

        it1 = OrderItem(order_id=demo_order.id, menu_item_id=items[0].id, quantity=1, unit_price=11.90)
        it2 = OrderItem(order_id=demo_order.id, menu_item_id=items[4].id, quantity=1, unit_price=14.50)
        db.session.add_all([it1, it2])

        db.session.commit()
        print("Base de donnees initialisee avec succes.")

if __name__ == '__main__':
    run_seed()
