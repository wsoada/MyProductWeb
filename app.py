# -*- coding: utf-8 -*-
"""
ProductDisplayWebpage - 动态网站
直接从 ProductDisplayWebManage 数据库读取数据
"""
import os
import sys

# 添加管理系统路径
MANAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ProductDisplayWebManage')
sys.path.insert(0, MANAGE_DIR)

from flask import Flask, render_template, jsonify

try:
    from database import db
    from database.models import Category, Subcategory, Product
    from app import app as manage_app
    DB_AVAILABLE = True
except ImportError as e:
    print(f"警告: 无法导入管理系统数据库模块: {e}")
    DB_AVAILABLE = False

app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = 'your-secret-key-here'


def slugify(text):
    """将文本转换为URL友好的slug"""
    import re
    if not text:
        return "unknown"
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-') or "unknown"


def get_categories_data():
    """从数据库获取所有分类数据"""
    if not DB_AVAILABLE:
        return []
    
    try:
        with manage_app.app_context():
            categories_data = []
            
            for cat in Category.query.all():
                cat_data = {
                    "slug": cat.slug or slugify(cat.name),
                    "title": cat.name_en or cat.name,
                    "desc": cat.description or f"Professional {cat.name} sourcing from trusted factory partners.",
                    "icon": cat.icon or "fa-box",
                    "color": cat.color or "from-blue-600 to-blue-400",
                    "subs": []
                }
                
                for sub in cat.subcategories:
                    sub_data = {
                        "slug": sub.slug or slugify(sub.name),
                        "title": sub.name_en or sub.name,
                        "desc": sub.description or f"Quality {sub.name} products for wholesale and retail.",
                        "icon": sub.icon or "fa-tag",
                        "sku_prefix": sub.sku_prefix or "PR",
                        "products": []
                    }
                    
                    for prod in sub.products:
                        price_value = prod.get_current_price()
                        price_display = f"From ${float(price_value):.2f}/pc" if price_value else "Contact for price"
                        
                        prod_data = {
                            "id": prod.id,
                            "name": prod.name,
                            "desc": prod.description or "High quality product from trusted suppliers.",
                            "price": price_display,
                            "moq": f"MOQ: {prod.moq}" if prod.moq else "MOQ: Flexible",
                            "tags": prod.tags or "oem",
                            "image": prod.image
                        }
                        sub_data["products"].append(prod_data)
                    
                    cat_data["subs"].append(sub_data)
                
                categories_data.append(cat_data)
            
            return categories_data
            
    except Exception as e:
        print(f"从数据库读取数据失败: {e}")
        import traceback
        traceback.print_exc()
        return []


# 静态文件路由 - 直接服务生成的静态页面
@app.route('/')
def index():
    """首页"""
    return app.send_static_file('index.html')


@app.route('/products/<path:path>')
def products(path):
    """产品页面"""
    file_path = os.path.join('products', path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return app.send_static_file(file_path)
    return "Page not found", 404


# API 路由 - 动态获取数据
@app.route('/api/categories')
def api_categories():
    """获取所有分类数据"""
    data = get_categories_data()
    return jsonify({
        'success': True,
        'data': data
    })


@app.route('/api/category/<slug>')
def api_category(slug):
    """获取单个分类数据"""
    data = get_categories_data()
    for cat in data:
        if cat['slug'] == slug:
            return jsonify({
                'success': True,
                'data': cat
            })
    return jsonify({
        'success': False,
        'message': 'Category not found'
    }), 404


@app.route('/api/subcategory/<cat_slug>/<sub_slug>')
def api_subcategory(cat_slug, sub_slug):
    """获取子分类数据"""
    data = get_categories_data()
    for cat in data:
        if cat['slug'] == cat_slug:
            for sub in cat['subs']:
                if sub['slug'] == sub_slug:
                    return jsonify({
                        'success': True,
                        'data': sub
                    })
    return jsonify({
        'success': False,
        'message': 'Subcategory not found'
    }), 404


@app.route('/api/products')
def api_products():
    """获取所有产品"""
    products = []
    data = get_categories_data()
    for cat in data:
        for sub in cat['subs']:
            for prod in sub['products']:
                prod['category'] = cat['title']
                prod['subcategory'] = sub['title']
                products.append(prod)
    
    return jsonify({
        'success': True,
        'count': len(products),
        'data': products
    })


if __name__ == '__main__':
    print(f"数据库可用: {DB_AVAILABLE}")
    if DB_AVAILABLE:
        print("启动动态网站服务器...")
        print("访问 http://localhost:5001 查看网站")
    else:
        print("警告: 数据库不可用，将使用静态文件")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
