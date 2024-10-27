from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=True)


# 定义用户模型
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum('customer', 'admin'), default='customer')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Cart(db.Model):
    __tablename__ = 'carts'  # 添加表名

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 修正外键引用
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class CartItem(db.Model):
    __tablename__ = 'cart_items'  # 添加表名

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)  # 修正外键引用
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)  # 修正外键引用
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # 添加关系
    menu_item = db.relationship('MenuItem', backref='cart_items')

    db.UniqueConstraint('cart_id', 'menu_item_id', name='unique_cart_item')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='制作中')  # 新增状态列
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='orders')  # 反向关系


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    price = db.Column(db.Float, nullable=False)

    order = db.relationship('Order', backref='order_items')  # 反向关系
    menu_item = db.relationship('MenuItem', backref='order_items')  # 反向关系
