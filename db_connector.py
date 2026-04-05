# -*- coding: utf-8 -*-
"""
db_connector.py
连接 ProductDisplayWebManage 的数据库，读取分类和产品数据
"""
import os
import sys

# 添加 ProductDisplayWebManage 到路径
MANAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ProductDisplayWebManage')
sys.path.insert(0, MANAGE_DIR)

# 导入管理系统的数据库模型
try:
    from database import db
    from database.models import Category, Subcategory, Product
    from app import app as manage_app
    
    DB_AVAILABLE = True
except ImportError as e:
    print(f"警告: 无法导入管理系统数据库模块: {e}")
    DB_AVAILABLE = False


def get_categories_from_db():
    """从数据库获取所有分类和子分类数据"""
    if not DB_AVAILABLE:
        return None
    
    try:
        with manage_app.app_context():
            categories_data = []
            
            # 获取所有主分类
            categories = Category.query.all()
            
            for cat in categories:
                cat_data = {
                    "slug": cat.slug or slugify(cat.name),
                    "title": cat.name_en or cat.name,
                    "desc": cat.description or f"Professional {cat.name} sourcing from trusted factory partners.",
                    "icon": cat.icon or "fa-box",
                    "icon_type": cat.icon_type or "fontawesome",
                    "color": cat.color or "from-blue-600 to-blue-400",
                    "depth": 2,
                    "subs": []
                }
                
                # 获取该分类下的所有子分类
                for sub in cat.subcategories:
                    sub_data = {
                        "slug": sub.slug or slugify(sub.name),
                        "title": sub.name_en or sub.name,
                        "desc": sub.description or f"Quality {sub.name} products for wholesale and retail.",
                        "icon": sub.icon or "fa-tag",
                        "icon_type": sub.icon_type or "fontawesome",
                        "sku_prefix": sub.sku_prefix or "PR",
                        "products": []
                    }
                    
                    # 获取该子分类下的所有产品
                    for prod in sub.products:
                        # 解析标签
                        tags = prod.tags or "oem"
                        
                        # 获取产品价格
                        price_value = prod.get_current_price()
                        if price_value:
                            price_display = f"From ${float(price_value):.2f}/pc"
                        else:
                            price_display = "Contact for price"
                        
                        # 获取产品图片 - 从 image 字段提取文件名
                        image_filename = None
                        if prod.image:
                            # image 字段可能是完整路径，提取文件名
                            image_filename = os.path.basename(prod.image)
                        
                        # 获取产品图库 - 从 gallery 字段提取所有图片
                        gallery_images = []
                        if prod.gallery:
                            try:
                                import json
                                gallery_list = json.loads(prod.gallery)
                                gallery_images = [os.path.basename(url) for url in gallery_list if url]
                            except:
                                gallery_images = []
                        
                        # 获取产品特性
                        features = []
                        if prod.features:
                            try:
                                import json
                                features = json.loads(prod.features)
                            except:
                                features = []
                        
                        # 获取产品规格
                        specifications = {}
                        if prod.specifications:
                            try:
                                import json
                                specifications = json.loads(prod.specifications)
                            except:
                                specifications = {}
                        
                        prod_data = {
                            "name": prod.name,
                            "desc": prod.description or "High quality product from trusted suppliers.",
                            "price": price_display,
                            "moq": f"MOQ: {prod.moq}" if prod.moq else "MOQ: Flexible",
                            "tags": tags,
                            "image": image_filename,  # 添加主图片文件名
                            "gallery": gallery_images,  # 添加图库图片列表
                            "id": prod.id,  # 添加产品ID
                            "features": features,  # 添加产品特性
                            "specifications": specifications  # 添加产品规格
                        }
                        sub_data["products"].append(prod_data)
                    
                    cat_data["subs"].append(sub_data)
                
                categories_data.append(cat_data)
            
            return categories_data
            
    except Exception as e:
        print(f"从数据库读取数据失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def slugify(text):
    """将文本转换为URL友好的slug"""
    import re
    if not text:
        return "unknown"
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-') or "unknown"


def get_category_stats():
    """获取分类统计信息"""
    if not DB_AVAILABLE:
        return None
    
    try:
        with manage_app.app_context():
            return {
                "categories": Category.query.count(),
                "subcategories": Subcategory.query.count(),
                "products": Product.query.count()
            }
    except Exception as e:
        print(f"获取统计信息失败: {e}")
        return None


# 测试代码
if __name__ == "__main__":
    if DB_AVAILABLE:
        print("数据库连接成功!")
        stats = get_category_stats()
        if stats:
            print(f"统计: {stats['categories']} 主分类, {stats['subcategories']} 子分类, {stats['products']} 产品")
        
        data = get_categories_from_db()
        if data:
            print(f"\n成功读取 {len(data)} 个主分类:")
            for cat in data:
                print(f"  - {cat['title']}: {len(cat['subs'])} 个子分类")
        else:
            print("无法从数据库读取数据")
    else:
        print("数据库模块不可用")
