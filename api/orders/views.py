from flask_restx import Resource, Namespace

order_namespace = Namespace('orders', description='Namespace for orders')

@order_namespace.route('/orders')
class OrderGetCreate(Resource):
    """
    Order namespace
    """
    def get(self):
        """
        Get all orders
        """
        pass

    def post(self):
        """
        Place a new order
        """
        pass

@order_namespace.route('/order/<int:order_id>')
class OrderUpdateGetDelete(Resource):
    """
    Order update, get and delete namespace
    """

    def get(self, order_id):
        """
        Get a specific order by ID
        """
        pass

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