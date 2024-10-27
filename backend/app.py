from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db  # 直接导入 models 模块中的 db
from routes import api_bp  # 直接导入 routes 模块中的 api_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = '123456789'
CORS(app, supports_credentials=True)  # 允许跨域请求
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0000@localhost/coffe'  # MariaDB 连接字符串
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '123456789'  # 设置您的 JWT 密钥
jwt = JWTManager(app)  # 初始化 JWTManager



# 初始化数据库
db.init_app(app)

# 注册 API 路由
app.register_blueprint(api_bp)

# 创建数据库表（如果需要）
with app.app_context():
    db.create_all()

# 添加根路由处理
@app.route('/')
def index():
    return "Welcome to the Coffee API! Use /api/menu to get the menu."

if __name__ == '__main__':
    app.run(debug=True)

