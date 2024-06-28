from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus

order_namespace = Namespace('orders', description='Namespace for orders')

order_model = order_namespace.model(
    'Order',
    {
        'id': fields.Integer(description='Order ID'),
        'size': fields.String(description='Size of order', required=True, enum=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']),
        'order_status': fields.String(description="The status of the Order", required=True, enum=['PENDING', 'IN_TRANSIT', 'DELIVERED']),
        'flavour' : fields.String(description='Flavour of the order', required=True),
        'quantity': fields.Integer(description='Quantity of the order', required=True),
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

    def put(self, order_id):
        """
        Update a specific order by ID
        """
        pass

    def delete(self, order_id):
        """
        Delete a specific order by ID
        """
        pass

@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    """
    Get a specific order by user ID namespace
    """

    def get(self, user_id, order_id):
        """
        Get a specific order by user ID and order ID
        """
        pass

@order_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):
    """
    Get all orders for a specific user namespace
    """

    def get(self, user_id):
        """
        Get all orders for a specific user by ID
        """
        pass

@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    """
    Update an order status namespace
    """

    def patch(self, order_id):
        """
        Update the status of a specific order by ID
        """
        pass 