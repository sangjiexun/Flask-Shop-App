from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_mail import Mail
from flask_babel import Babel
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os

# 初始化Flask应用
app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 初始化登录管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 初始化邮件
mail = Mail(app)

# 初始化Babel
babel = Babel(app)

# 初始化文件上传
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)

# 数据库模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user')
    orders = db.relationship('Order', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=True)
    orders = db.relationship('OrderItem', backref='product', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# 登录管理器回调
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 路由
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        products = Product.query.filter(Product.name.contains(keyword) | Product.description.contains(keyword)).all()
        return render_template('search.html', products=products, keyword=keyword)
    return render_template('search.html')

@app.route('/product/<int:id>')
def product(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:id>', methods=['POST'])
@login_required
def add_to_cart(id):
    product = Product.query.get_or_404(id)
    quantity = int(request.form['quantity'])
    
    # 检查库存
    if product.stock < quantity:
        flash('Insufficient stock!')
        return redirect(url_for('product', id=id))
    
    # 检查购物车中是否已有该商品
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=current_user.id, product_id=id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Product added to cart!')
    return redirect(url_for('product', id=id))

@app.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout')
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty!')
        return redirect(url_for('index'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    # 创建订单
    order = Order(user_id=current_user.id, total=total)
    db.session.add(order)
    db.session.flush()
    
    # 添加订单项
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)
        
        # 减少库存
        item.product.stock -= item.quantity
    
    # 清空购物车
    Cart.query.filter_by(user_id=current_user.id).delete()
    
    db.session.commit()
    
    flash('Order placed successfully!')
    return redirect(url_for('orders'))

@app.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)

@app.route('/order/<int:id>')
@login_required
def order(id):
    order = Order.query.get_or_404(id)
    if order.user_id != current_user.id:
        flash('You do not have permission to view this order!')
        return redirect(url_for('orders'))
    return render_template('order.html', order=order)

@app.route('/pay/<int:id>')
@login_required
def pay(id):
    order = Order.query.get_or_404(id)
    if order.user_id != current_user.id:
        flash('You do not have permission to pay for this order!')
        return redirect(url_for('orders'))
    
    # 模拟支付
    order.status = 'paid'
    db.session.commit()
    
    flash('Payment successful!')
    return redirect(url_for('order', id=id))

@app.route('/sell')
@login_required
def sell():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page!')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    return render_template('sell.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page!')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        category = request.form['category']
        
        # 处理文件上传
        image = None
        if 'image' in request.files:
            filename = photos.save(request.files['image'])
            image = filename
        
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            image=image
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!')
        return redirect(url_for('sell'))
    
    return render_template('add_product.html')

# 登录和注册路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # 注意：实际应用中应该使用密码哈希
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!')
    
    return render_template('security/login_user.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            flash('Email already exists!')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, password=password)  # 注意：实际应用中应该使用密码哈希
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('security/register_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# 主函数
if __name__ == '__main__':
    # 创建数据库表
    with app.app_context():
        db.create_all()
        
        # 创建管理员用户（如果不存在）
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', password='admin123', role='admin')
            db.session.add(admin)
            db.session.commit()
        
        # 创建示例商品（如果不存在）
        if not Product.query.first():
            products = [
                Product(name='Laptop', description='High performance laptop', price=999.99, stock=50, category='Electronics', image='laptop.jpg'),
                Product(name='Smartphone', description='Latest smartphone', price=699.99, stock=100, category='Electronics', image='smartphone.jpg'),
                Product(name='Headphones', description='Noise canceling headphones', price=199.99, stock=200, category='Electronics', image='headphones.jpg'),
                Product(name='T-shirt', description='Cotton t-shirt', price=19.99, stock=500, category='Clothing', image='tshirt.jpg'),
                Product(name='Jeans', description='Denim jeans', price=49.99, stock=300, category='Clothing', image='jeans.jpg')
            ]
            for product in products:
                db.session.add(product)
            db.session.commit()
    
    app.run(debug=True)