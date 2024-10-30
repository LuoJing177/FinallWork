import os
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from models import db, MenuItem, User, Cart, CartItem, OrderItem, Order  # 直接导入 models 模块
from flask import session  # 导入 session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/menu', methods=['GET'])
def get_menu():
    menu_items = MenuItem.query.all()
    return {
        'menu': [
            {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'stock': item.stock,
                'image': item.image
            } for item in menu_items
        ]
    }


# 用户注册
@api_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'error': 'Missing fields'}), 400

    # 检查用户是否已经存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    # 创建新用户
    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    # 返回成功的响应，包含 success 属性
    return jsonify({'success': True, 'message': 'User registered successfully!'}), 201


@api_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 查找用户
    user = User.query.filter_by(username=username, password=password).first()

    if user:
        # 创建 JWT token
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})

        # 存储用户 ID 在 session 中（可选）
        session['user_id'] = user.id
        print("User ID stored in session:", session['user_id'])  # 输出存储的用户 ID

        return jsonify({
            'message': 'Login successful!',
            'token': access_token,  # 返回 token
            'role': user.role  # 返回用户角色
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@api_bp.route('/api/cart/add', methods=['POST'])
@jwt_required()  # 添加此装饰器以确保验证 JWT
def add_to_cart():
    # 从 JWT 中获取当前用户的身份
    current_user = get_jwt_identity()
    user_id = current_user['id']  # 假设在 JWT 中存储了用户 ID
    print("User ID from JWT:", user_id)

    item_id = request.json.get('item_id')
    print("Item ID from request:", item_id)

    if not item_id:
        print("No item_id provided")
        return jsonify({'error': 'No item ID provided'}), 400

    # 获取或创建购物车
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
        print("Created new cart:", cart)

    # 检查商品是否已在购物车中
    existing_item = CartItem.query.filter_by(cart_id=cart.id, menu_item_id=item_id).first()
    if existing_item:
        print("Item already in cart:", existing_item)
        return jsonify({'error': 'Item already in cart'}), 400

    # 添加商品到购物车
    cart_item = CartItem(cart_id=cart.id, menu_item_id=item_id, quantity=1)
    db.session.add(cart_item)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Item added to cart successfully'})


@api_bp.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    # 获取当前用户的 ID
    user_id = get_jwt_identity()['id']

    # 查找用户的购物车
    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return jsonify({'error': 'Cart not found'}), 404

    # 获取购物车中的所有商品，并关联菜单项信息
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()

    # 构建返回数据
    cart_data = []
    for item in cart_items:
        cart_data.append({
            'id': item.id,
            'quantity': item.quantity,
            'menu_item': {
                'id': item.menu_item.id,
                'name': item.menu_item.name,
                'description': item.menu_item.description,
                'price': item.menu_item.price,
                'stock': item.menu_item.stock,
                'image': item.menu_item.image
            }
        })

    return jsonify({'cart_items': cart_data}), 200


@api_bp.route('/api/cart/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_cart_item(item_id):
    user_id = get_jwt_identity()['id']
    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return jsonify({'error': 'Cart not found'}), 404

    cart_item = CartItem.query.filter_by(cart_id=cart.id, id=item_id).first()

    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({'message': 'Item deleted successfully'}), 200


# 更新购物车中商品数量的接口
@api_bp.route('/api/cart/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    current_user = get_jwt_identity()  # 获取当前用户身份
    user_id = current_user['id']  # 获取用户ID
    cart = Cart.query.filter_by(user_id=user_id).first()  # 查找用户的购物车

    if not cart:
        return jsonify({'error': 'Cart not found'}), 404

    # 检查请求数据
    data = request.get_json()
    if 'quantity' not in data:
        return jsonify({'msg': '数量未提供'}), 400

    quantity = data['quantity']

    # 检查数量是否有效
    if quantity < 1:
        return jsonify({'msg': '数量必须大于0'}), 400

    # 查找购物车项目
    cart_item = CartItem.query.filter_by(cart_id=cart.id, id=item_id).first()

    if cart_item is None:
        return jsonify({'msg': '购物车项未找到'}), 404

    # 更新数量
    cart_item.quantity = quantity
    db.session.commit()

    return jsonify({'msg': '数量更新成功', 'cart_item': {
        'id': cart_item.id,
        'quantity': cart_item.quantity,
        'menu_item_id': cart_item.menu_item_id
    }}), 200


@api_bp.route('/api/order', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()['id']  # 获取当前用户的 ID
    data = request.json
    items = data.get('items', [])
    total_amount = data.get('total_amount', 0)

    # 创建订单
    new_order = Order(user_id=user_id, total_amount=total_amount)
    db.session.add(new_order)

    try:
        db.session.commit()  # 提交订单

        # 将商品转移到订单项并减少库存
        for item in items:
            menu_item = MenuItem.query.get(item['menu_item'].get('id'))
            if menu_item and menu_item.stock >= item['quantity']:  # 检查库存是否足够
                order_item = OrderItem(
                    order_id=new_order.id,
                    menu_item_id=menu_item.id,
                    quantity=item['quantity'],
                    price=item['menu_item'].get('price')  # 根据实际情况获取价格
                )
                db.session.add(order_item)

                # 更新库存
                menu_item.stock -= item['quantity']  # 减少库存
            else:
                db.session.rollback()  # 回滚事务
                return jsonify({'error': f'库存不足: {menu_item.name if menu_item else "商品未找到"}'}), 400

        db.session.commit()  # 提交订单项
        return jsonify({'order_id': new_order.id}), 201

    except IntegrityError:
        db.session.rollback()  # 回滚事务
        return jsonify({'error': 'Failed to create order'}), 400


@api_bp.route('/api/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    user_id = get_jwt_identity()['id']
    print(user_id)
    orders = Order.query.filter_by(user_id=user_id).all()
    print(orders)

    order_list = []
    for order in orders:
        order_items = OrderItem.query.filter_by(order_id=order.id).all()
        items = [{
            'id': item.menu_item.id,
            'name': item.menu_item.name,
            'quantity': item.quantity,
            'price': item.price
        } for item in order_items]

        order_list.append({
            'id': order.id,
            'total_amount': order.total_amount,
            'status': order.status,
            'created_at': order.created_at,
            'items': items
        })

    return jsonify(order_list), 200


@api_bp.route('/api/ordersadmin', methods=['GET'])
@jwt_required()
def get_admin_orders():
    # 获取管理员身份信息（这里可以添加角色检查，以确保只有管理员可以访问）
    user_identity = get_jwt_identity()  # 获取JWT身份信息
    print(user_identity)

    # 查询所有订单
    orders = Order.query.all()  # 如果需要，可以根据用户权限过滤

    order_list = []
    for order in orders:
        order_items = OrderItem.query.filter_by(order_id=order.id).all()  # 查询该订单下的所有订单项
        items = [{
            'id': item.menu_item.id,
            'name': item.menu_item.name,
            'quantity': item.quantity,
            'price': item.price
        } for item in order_items]

        order_list.append({
            'id': order.id,
            'total_amount': order.total_amount,
            'status': order.status,
            'created_at': order.created_at,
            'items': items  # 订单项
        })

    return jsonify(order_list), 200


@api_bp.route('/api/ordersadmin/<int:order_id>/complete', methods=['PUT'])
@jwt_required()
def mark_order_complete(order_id):
    try:
        # 获取订单
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # 更新订单状态
        order.status = '已完成'
        db.session.commit()

        return jsonify({'message': 'Order marked as complete'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 获取所有商品信息（库存显示）
@api_bp.route('/api/menu_items_show', methods=['GET'])
@jwt_required()
def get_all_menu_items():
    try:
        menu_items = MenuItem.query.all()
        result = [{
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'stock': item.stock,
            'image': item.image
        } for item in menu_items]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 更新商品库存
@api_bp.route('/api/menu_items/<int:menu_item_id>', methods=['PUT'])
@jwt_required()
def update_stock(menu_item_id):
    data = request.get_json()
    try:
        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item:
            return jsonify({'error': 'Menu item not found'}), 404

        menu_item.stock = data.get('stock', menu_item.stock)
        db.session.commit()

        return jsonify({'message': 'Stock updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 添加新商品
# 指定图片存储的文件夹
# 设置图片保存目录
# UPLOAD_FOLDER = 'E:/College/云计算/Coffee/frontend/coffee-order-frontend/public/images'
# 使用相对路径指向前端的图片保存目录
# 定义相对路径的图片上传文件夹
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'coffee-order-frontend', 'public', 'images')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api_bp.route('/api/menu_items_insert', methods=['POST'])
@jwt_required()
def add_new_menu_item():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        data = request.form
        item_name = data.get('name')
        item_price = data.get('price')  # 获取价格

        # 将价格转换为浮点数并验证
        try:
            price = float(item_price)
            if price < 0:
                return jsonify({'error': 'Price must be a non-negative number'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid price value'}), 400

        if file and allowed_file(file.filename) and item_name:
            # 确保目标目录存在
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            # 获取文件扩展名
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            # 将文件重命名为 商品名.扩展名
            filename = secure_filename(f"{item_name}.{file_extension}")
            # 使用 UPLOAD_FOLDER 来构建文件路径
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            print(file_path)
            file.save(file_path)

            # 检查是否重复提交
            print(f"Saving new item: {item_name}")

            # 存储商品信息到数据库
            new_item = MenuItem(
                name=item_name,
                description=data.get('description'),
                price=price,  # 使用转换后的浮点数价格
                stock=data.get('stock'),
                image=filename  # 存储图片名为商品名.扩展名
            )

            # 防止重复提交：检查数据库中是否已经存在相同商品（通过名称）
            existing_item = MenuItem.query.filter_by(name=item_name).first()
            if existing_item:
                return jsonify({'error': 'Item already exists'}), 400

            # 保存到数据库
            db.session.add(new_item)
            db.session.commit()

            return jsonify({'message': 'Menu item added successfully'}), 201

        else:
            return jsonify({'error': 'File type not allowed or missing item name'}), 400

    except Exception as e:
        db.session.rollback()  # 出现异常时回滚事务
        return jsonify({'error': str(e)}), 500


# 删除商品
@api_bp.route('/api/menu_items/<int:menu_item_id>', methods=['DELETE'])
@jwt_required()
def delete_menu_item(menu_item_id):
    try:
        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item:
            return jsonify({'error': 'Menu item not found'}), 404

        # 删除文件
        image_path = os.path.join(UPLOAD_FOLDER, menu_item.image)
        if os.path.exists(image_path):
            os.remove(image_path)  # 删除文件
            print(f"Deleted image file: {image_path}")

        # 从数据库中删除商品
        db.session.delete(menu_item)
        db.session.commit()

        return jsonify({'message': 'Menu item deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()  # 出现异常时回滚事务
        return jsonify({'error': str(e)}), 500


# 查询指定订单的状态
@api_bp.route('/api/orders/<int:order_id>/status', methods=['GET'])
@jwt_required()
def get_order_status(order_id):
    # 获取当前用户的ID
    user_id = get_jwt_identity()['id']

    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        # 查询数据库，找到对应的订单并检查是否属于当前用户
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()

        if not order:
            return jsonify({'error': 'Order not found or unauthorized'}), 404

        # 假设订单有一个 status 字段，表示订单的当前状态
        return jsonify({'status': order.status}), 200

    except Exception as e:
        print(f"Error fetching order status: {e}")
        return jsonify({'error': 'Error fetching order status'}), 500
