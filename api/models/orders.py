from ..utils import db
from enum import Enum
from datetime import datetime
# Enum classes
class Sizes:
    SMALL = 'small',
    MEDIUM = 'medium',
    LARGE = 'large',
    EXTRA_LARGE = 'extra_large'

class OrderStatus:
    PENDING='pending',
    IN_TRANSIT='in_transit',
    DELIVERED='delivered'  
class Order(db.Model):
    __tablename__ = 'orders'

    # id, user_id, date, total, status, items
    id = db.Column(db.Integer(), primary_key=True)
    size = db.Column(db.Enum(Sizes), default=Sizes.MEDIUM)
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    flavour = db.Column(db.String(),nulable=False)
    date_created = db.Column(db.DateTime(timezone=True), server_default=datetime.utcnow()) 
    user = db.Column(db.Integer(), db.ForeignKey('users.id'))
    def __repr__(self) -> str:
        return f"<Order {self.id}>"