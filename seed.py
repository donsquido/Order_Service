from app import create_app
from app.models import db, Customer, Order, OrderItem

app = create_app()
app.app_context().push()

def seed_data():
    # Customer 1
    from app import create_app
from app.models import db, Customer, Order, OrderItem

app = create_app()
app.app_context().push()

def seed_data():
    # Customer 1
    if not Customer.query.filter_by(email="demo1@example.com").first():
        customer1 = Customer(email="demo1@example.com", phone="1111111111", name="Alice")
        db.session.add(customer1)
        db.session.flush()

        order1 = Order(order_id="ORD001", customer_id=customer1.id, total_amount=1500, status="completed")
        db.session.add(order1)
        db.session.flush()

        item1a = OrderItem(order_id=order1.id, product_name="Laptop", quantity=1, price=1500)
        db.session.add(item1a)

    # Customer 2
    if not Customer.query.filter_by(email="demo2@example.com").first():
        customer2 = Customer(email="demo2@example.com", phone="2222222222", name="Bob")
        db.session.add(customer2)
        db.session.flush()

        order2 = Order(order_id="ORD002", customer_id=customer2.id, total_amount=500, status="pending")
        db.session.add(order2)
        db.session.flush()

        item2a = OrderItem(order_id=order2.id, product_name="Mouse", quantity=2, price=250)
        db.session.add(item2a)

    # Customer 3
    if not Customer.query.filter_by(email="demo3@example.com").first():
        customer3 = Customer(email="demo3@example.com", phone="3333333333", name="Charlie")
        db.session.add(customer3)
        db.session.flush()

        order3 = Order(order_id="ORD003", customer_id=customer3.id, total_amount=750, status="shipped")
        db.session.add(order3)
        db.session.flush()

        item3a = OrderItem(order_id=order3.id, product_name="Keyboard", quantity=1, price=300)
        item3b = OrderItem(order_id=order3.id, product_name="Headphones", quantity=1, price=450)
        db.session.add(item3a)
        db.session.add(item3b)

    db.session.commit()
    print("✅ Seed data inserted successfully")

if __name__ == "__main__":
    seed_data()

