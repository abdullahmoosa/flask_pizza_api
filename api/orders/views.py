from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from ..models.orders import Order, OrderStatus
from ..models.users import User
from ..utils import db


order_namespace = Namespace('orders', description='Namespace for orders')

order_model = order_namespace.model(
    'Order',
    {
        'id': fields.Integer(description='Order ID'),
        'size': fields.String(description='Size of order', required=True, enum=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']),
        'order_status': fields.String(description="The status of the Order", required=True, enum=['PENDING', 'IN_TRANSIT', 'DELIVERED']),
        'flavour': fields.String(description='Flavour of the order', required=True),
        'quantity': fields.Integer(description='Quantity of the order', required=True),
    }
)

order_status_model = order_namespace.model(
    'OrderStatus',{
        'order_status': fields.String(description="The status of the Order", required=True, enum=['PENDING', 'IN_TRANSIT', 'DELIVERED'])
    }
)

@order_namespace.route('/orders') 
class OrderGetCreate(Resource):
    """
    Order namespace
    """
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self):
        """
        Get all orders
        """
        orders =  Order.query.all()

        return orders, HTTPStatus.OK
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
        Place a new order
        """
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        data = order_namespace.payload
        new_order = Order(
            size = data['size'],
            quantity = data['quantity'],
            flavour = data['flavour'],
        )

        new_order.user = current_user.id

        new_order.save()
        return  new_order, HTTPStatus.CREATED

@order_namespace.route('/order/<int:order_id>')
class OrderUpdateGetDelete(Resource):
    """
    Order update, get and delete namespace
    """
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, order_id):
        """
        Get a specific order by ID
        """
        order = Order.get_by_id(order_id)

        return order, HTTPStatus.OK
    
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def put(self, order_id):
        """
        Update a specific order by ID
        """

        order_to_update = Order.get_by_id(order_id)

        data = order_namespace.payload
        order_to_update.size = data['size']
        order_to_update.quantity = data['quantity']
        order_to_update.flavour = data['flavour']

        db.session.commit()

        return order_to_update, HTTPStatus.OK
    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def delete(self, order_id):
        """
        Delete a specific order by ID
        """
        order_to_delete = Order.get_by_id(order_id)
        order_to_delete.delete()
        return order_to_delete, HTTPStatus.NO_CONTENT

@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    """
    Get a specific order by user ID namespace
    """
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, user_id, order_id):
        """
        Get a specific order by user ID and order ID
        """

        user = User.get_by_id(user_id)

        order =Order.query.filter_by(id=order_id).filter_by(user=user.id).first()
        return order, HTTPStatus.OK

@order_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):
    """
    Get all orders for a specific user namespace
    """
    @order_namespace.marshal_list_with(order_model)
    @jwt_required()
    def get(self, user_id):
        """
        Get all orders for a specific user by ID
        """
        user = User.get_by_id(user_id)
        orders = user.orders 
        return orders, HTTPStatus.OK


@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    """
    Update an order status
    """
    @order_namespace.expect(order_status_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def patch(self, order_id):
        """
        Update the status of a specific order by ID
        """

        data = order_namespace.payload
        order_to_update = Order.get_by_id(order_id)
        order_to_update.order_status = data['order_status']

        db.session.commit()

        return order_to_update, HTTPStatus.OK