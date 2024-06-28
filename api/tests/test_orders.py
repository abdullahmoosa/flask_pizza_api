from .. import create_app, db
from ..models.orders import Order
from unittest import TestCase

class TestOrderQuantity(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_order_quantity(self):
        # Create a new order with a quantity
        order = Order(quantity=5, flavour='chocolate', size='SMALL', order_status='PENDING')
        db.session.add(order)
        db.session.commit()

        # Retrieve the order and assert the quantity
        retrieved_order = Order.query.first()
        self.assertEqual(retrieved_order.quantity, 5)
