# Flask-Shop

## 项目简介
Flask-Shop是一个基于Flask框架开发的电子商务平台，提供完整的购物流程，包括商品浏览、搜索、购物车、订单管理和支付功能。

## 技术架构

### 后端技术
- **Flask**: Python Web框架
- **Flask-SQLAlchemy**: ORM数据库工具
- **Flask-Login**: 用户认证管理
- **Flask-Migrate**: 数据库迁移工具
- **Flask-Security**: 安全功能扩展
- **Flask-Mail**: 邮件发送功能
- **Flask-Babel**: 国际化支持
- **SQLite/PostgreSQL**: 数据库系统

### 前端技术
- **HTML5/CSS3/JavaScript**: 前端基础
- **Jinja2**: 模板引擎
- **Bootstrap**: 响应式UI框架

### 项目结构
```
Flask-Shop/
├── flask_shop.py          # 主应用文件
├── requirements.txt       # 依赖列表
├── static/                # 静态文件
│   └── login.css          # 登录页面样式
└── templates/             # 模板文件
    ├── layout.html        # 基础布局
    ├── search.html        # 搜索页面
    ├── sell.html          # 卖家页面
    ├── product.html       # 商品详情
    ├── order.html         # 订单详情
    ├── orders.html        # 订单列表
    ├── pay.html           # 支付页面
    └── security/          # 安全相关模板
        ├── login_user.html    # 登录页面
        └── register_user.html # 注册页面
```

## 核心功能

### 用户管理
- 用户注册与登录
- 密码重置
- 用户权限管理

### 商品管理
- 商品列表与详情
- 商品搜索
- 商品分类

### 购物流程
- 购物车管理
- 订单创建与管理
- 支付处理

### 卖家功能
- 商品发布
- 库存管理
- 订单处理

## 安装与运行

### 环境要求
- Python 3.6+
- pip包管理器

### 安装步骤
1. 克隆仓库
   ```bash
   git clone https://github.com/sangjiexun/Flask-Shop-App.git
   cd Flask-Shop-App
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 初始化数据库
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. 运行应用
   ```bash
   flask run
   ```

5. 访问应用
   打开浏览器访问 http://localhost:5000

## 配置说明

### 数据库配置
默认使用SQLite数据库，可在`flask_shop.py`中修改为PostgreSQL：

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
```

### 邮件配置
用于密码重置等功能：

```python
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
```

## 安全措施
- 密码哈希存储
- CSRF保护
- 权限控制
- 输入验证

## 国际化支持
- 多语言支持（英文、中文）
- 时区处理

## 部署建议
- 使用Gunicorn作为WSGI服务器
- 使用Nginx作为反向代理
- 配置HTTPS
- 数据库定期备份

## 贡献指南
欢迎提交Issue和Pull Request来改进这个项目。

## 许可证
MIT License

---

# Flask-Shop

## Project Introduction
Flask-Shop is an e-commerce platform developed based on the Flask framework, providing a complete shopping process including product browsing, search, shopping cart, order management, and payment functions.

## Technical Architecture

### Backend Technology
- **Flask**: Python Web framework
- **Flask-SQLAlchemy**: ORM database tool
- **Flask-Login**: User authentication management
- **Flask-Migrate**: Database migration tool
- **Flask-Security**: Security feature extension
- **Flask-Mail**: Email sending functionality
- **Flask-Babel**: Internationalization support
- **SQLite/PostgreSQL**: Database system

### Frontend Technology
- **HTML5/CSS3/JavaScript**: Frontend basics
- **Jinja2**: Template engine
- **Bootstrap**: Responsive UI framework

### Project Structure
```
Flask-Shop/
├── flask_shop.py          # Main application file
├── requirements.txt       # Dependency list
├── static/                # Static files
│   └── login.css          # Login page styles
└── templates/             # Template files
    ├── layout.html        # Base layout
    ├── search.html        # Search page
    ├── sell.html          # Seller page
    ├── product.html       # Product details
    ├── order.html         # Order details
    ├── orders.html        # Order list
    ├── pay.html           # Payment page
    └── security/          # Security-related templates
        ├── login_user.html    # Login page
        └── register_user.html # Registration page
```

## Core Features

### User Management
- User registration and login
- Password reset
- User permission management

### Product Management
- Product list and details
- Product search
- Product categories

### Shopping Process
- Shopping cart management
- Order creation and management
- Payment processing

### Seller Features
- Product publishing
- Inventory management
- Order processing

## Installation and Running

### Environment Requirements
- Python 3.6+
- pip package manager

### Installation Steps
1. Clone the repository
   ```bash
   git clone https://github.com/sangjiexun/Flask-Shop-App.git
   cd Flask-Shop-App
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. Run the application
   ```bash
   flask run
   ```

5. Access the application
   Open a browser and visit http://localhost:5000

## Configuration Instructions

### Database Configuration
SQLite is used by default, which can be changed to PostgreSQL in `flask_shop.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
```

### Email Configuration
For password reset and other functions:

```python
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
```

## Security Measures
- Password hash storage
- CSRF protection
- Permission control
- Input validation

## Internationalization Support
- Multi-language support (English, Chinese)
- Time zone handling

## Deployment Recommendations
- Use Gunicorn as WSGI server
- Use Nginx as reverse proxy
- Configure HTTPS
- Regular database backups

## Contribution Guide
Welcome to submit Issues and Pull Requests to improve this project.

## License
MIT License