from ..utils import db
from enum import Enum
from datetime import datetime
# Enum classes
class Sizes(Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'

class OrderStatus(Enum):
    PENDING='pending'
    IN_TRANSIT='in_transit'
    DELIVERED='delivered'  

class Order(db.Model):
    __tablename__ = 'orders'

    # id, user_id, date, total, status, items
    id = db.Column(db.Integer(), primary_key=True)
    size = db.Column(db.Enum(Sizes), default=Sizes.MEDIUM)
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    flavour = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    quantity = db.Column(db.Integer(), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'size': self.size.value,
            'order_status': self.order_status.value,
            'flavour': self.flavour,
            'date_created': self.date_created.isoformat(),
            'quantity': self.quantity,
            'user_id': self.user
        }
    def save(self):
        db.session.add(self)
        db.session.commit()
    def __repr__(self) -> str:
        return f"<Order {self.id}>"
