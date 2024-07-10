from ..models.orders import Order
from unittest import TestCase
from flask_jwt_extended import create_access_token

from .. import create_app, db
from ..config.config import config_dict

class TestOrderQuantity(TestCase):
    def setUp(self):
        self.app = create_app(config_dict['test'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

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

    def test_get_all_orders(self):
        token = create_access_token(identity='testuser')
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get('/orders/orders', headers=headers)

        assert response.status_code == 200

    def test_create_order(self):
        token = create_access_token(identity='testuser')
        headers = {
            "Authorization": f"Bearer {token}"
        }
        data = {
            "quantity": 2,
            "flavour": "chocolate",
            "size": "SMALL",
        }
        response = self.client.post('/orders/orders', json=data, headers=headers)

        assert response.status_code == 201

