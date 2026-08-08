# -*- coding: utf-8 -*-
"""
generate_pages.py
批量生成 SourceSure 网站所有子分类产品页 + 分类汇总页
运行: python generate_pages.py
"""
import os, textwrap

# 导入数据库连接器
try:
    from db_connector import get_categories_from_db, DB_AVAILABLE
except ImportError as e:
    print(f"[WARN] 无法导入 db_connector: {e}")
    DB_AVAILABLE = False

BASE   = os.path.dirname(os.path.abspath(__file__))
WA     = "8618735731692"
EMAIL  = "18735731692@163.com"
BRAND  = "SourceSure"
COMPANY= "Yiwu Juncheng Co., Ltd."
SLOGAN = "One-Stop Sourcing Service in China"

# 图标基础URL（用于图片类型图标）
ICON_BASE_URL = "../.."  # 相对路径，根据页面深度调整

def render_icon(icon_data, icon_type='fontawesome', size='md', extra_class='', root=''):
    """
    渲染图标 - 支持 FontAwesome 和图片
    size: 'sm'(w-6 h-6), 'md'(w-10 h-10), 'lg'(w-14 h-14), 'xl'(w-16 h-16)
    root: 相对根路径，用于图片图标路径转换
    """
    size_classes = {
        'sm': 'w-6 h-6',
        'md': 'w-10 h-10',
        'lg': 'w-14 h-14',
        'xl': 'w-16 h-16'
    }
    img_size = size_classes.get(size, 'w-10 h-10')
    
    # 判断图标类型
    is_image = icon_type == 'image' or (icon_data and icon_data.startswith('/static') or icon_data.startswith('http'))
    
    if is_image and icon_data:
        # 图片图标 - 转换 /static 路径为相对路径
        if icon_data.startswith('/static'):
            # 移除开头的 /static，添加 root 前缀
            icon_path = icon_data[1:]  # 移除开头的 /
            icon_src = f"{root}{icon_path}" if root else icon_data
        else:
            icon_src = icon_data
        return f'<img src="{icon_src}" alt="" class="{img_size} object-contain {extra_class}">'
    elif icon_data:
        # FontAwesome 图标 - 使用 fa-solid 前缀（FontAwesome 6 兼容）
        if icon_data.startswith('fa-'):
            icon_class = icon_data
        else:
            icon_class = f'fa-{icon_data}'
        icon_size_class = {
            'sm': 'text-sm',
            'md': 'text-xl',
            'lg': 'text-2xl',
            'xl': 'text-3xl'
        }.get(size, 'text-xl')
        return f'<i class="fa-solid {icon_class} {icon_size_class} {extra_class}"></i>'
    else:
        # 默认图标
        return f'<i class="fa-solid fa-box text-xl {extra_class}"></i>'

# ─────────────────────────────────────────────────────────────
# DATA: 从数据库读取，如果失败则使用默认数据
# ─────────────────────────────────────────────────────────────

def get_categories():
    """获取分类数据，优先从数据库读取"""
    if DB_AVAILABLE:
        print("正在从数据库读取数据...")
        db_data = get_categories_from_db()
        if db_data:
            print(f"成功从数据库读取 {len(db_data)} 个分类")
            return db_data
        else:
            print("数据库读取失败，使用默认数据")
    else:
        print("数据库模块不可用，使用默认数据")
    
    # 默认数据（硬编码）
    return get_default_categories()


def get_default_categories():
    """默认分类数据（当数据库不可用时使用）"""
    return [
  {
    "slug": "home-daily",
    "title": "Home & Daily Essentials",
    "desc": "From kitchenware to storage solutions — everyday essentials sourced through trusted factory partners.",
    "icon": "fa-house",
    "color": "from-blue-600 to-blue-400",
    "depth": 2,   # products/home-daily/
    "subs": [
      {
        "slug": "kitchenware",
        "title": "Kitchenware",
        "desc": "Professional-grade kitchen tools for retail, hotel, and wholesale. BPA-free, CE/FDA certified.",
        "icon": "fa-utensils",
        "sku_prefix": "KW",
        "products": [
          {"name":"Premium 3-Piece Kitchen Cooking Set","desc":"BPA-free, heat resistant 230°C. Spatula, ladle, slotted spoon. Dishwasher safe.","price":"From $2.80/pc","moq":"MOQ: 200pcs","tags":"hot oem"},
          {"name":"5-Piece Stainless Steel Cookware Set","desc":"304 stainless, induction compatible, tempered glass lids. Hotel & restaurant grade.","price":"From $18.50/set","moq":"MOQ: 50sets","tags":"new oem"},
          {"name":"Non-stick Baking Tray Set (3pcs)","desc":"Carbon steel, PFOA-free coating. Even heat distribution. FDA certified.","price":"From $6.20/set","moq":"MOQ: 100sets","tags":"hot"},
          {"name":"12-Piece Silicone Kitchen Tool Set","desc":"Food-grade silicone, heat resistant 230°C. Custom color & logo. Retail-ready packaging.","price":"From $7.90/set","moq":"MOQ: 100sets","tags":"oem"},
        ]
      },
      {
        "slug": "bedding",
        "title": "Bedding",
        "desc": "Hotel-grade duvets, pillowcases and mattress protectors. OEKO-TEX certified.",
        "icon": "fa-bed",
        "sku_prefix": "BD",
        "products": [
          {"name":"Hotel 4-Piece Bedding Set (300TC)","desc":"100% cotton 300TC. OEKO-TEX certified. 8 sizes. Custom embroidery available.","price":"From $8.50/set","moq":"MOQ: 50sets","tags":"hot oem"},
          {"name":"Microfiber Duvet Insert (All Seasons)","desc":"280gsm, anti-allergenic. Corner loops, machine washable. Hotel & retail grade.","price":"From $12.00/pc","moq":"MOQ: 30pcs","tags":"new"},
          {"name":"Bamboo Cooling Pillow","desc":"Shredded memory foam + bamboo cover. Adjustable loft, cooling effect. CE certified.","price":"From $9.80/pc","moq":"MOQ: 50pcs","tags":"hot oem"},
          {"name":"Waterproof Mattress Protector","desc":"TPU laminated, noiseless, breathable. Fits 35cm depth. Machine washable 60°C.","price":"From $4.20/pc","moq":"MOQ: 100pcs","tags":"oem"},
        ]
      },
      {
        "slug": "bathroom-supplies",
        "title": "Bathroom Supplies",
        "desc": "Premium bath towels, shower accessories, spa-grade organizers. OEKO-TEX certified.",
        "icon": "fa-bath",
        "sku_prefix": "BA",
        "products": [
          {"name":"Egyptian Cotton Bath Towel Set (6pcs)","desc":"600gsm combed cotton. Ultra-absorbent, quick-dry. 12 colours. Hotel grade.","price":"From $6.80/set","moq":"MOQ: 50sets","tags":"hot oem"},
          {"name":"Bamboo Shower Caddy Organizer","desc":"Rust-proof bamboo + stainless frame. 4 shelves, tension pole. No drilling.","price":"From $11.50/pc","moq":"MOQ: 30pcs","tags":"new"},
          {"name":"Liquid Soap Dispenser Set (3pcs)","desc":"Borosilicate glass, stainless pump. 300ml. Matching tray included.","price":"From $4.50/set","moq":"MOQ: 100sets","tags":"hot oem"},
          {"name":"Memory Foam Bath Mat","desc":"Non-slip, machine washable, anti-mold. 50×80cm. 15 colour options.","price":"From $3.90/pc","moq":"MOQ: 100pcs","tags":"oem"},
        ]
      },
      {
        "slug": "cleaning-products",
        "title": "Cleaning Products",
        "desc": "Microfiber, biodegradable cleaning tools for home and professional use.",
        "icon": "fa-spray-can-sparkles",
        "sku_prefix": "CL",
        "products": [
          {"name":"Microfiber Cleaning Cloth Set (12pcs)","desc":"320gsm ultra-fine fibers, scratch-free. Machine washable 500+ times. Color-coded.","price":"From $0.45/pc","moq":"MOQ: 500pcs","tags":"hot"},
          {"name":"Spin Mop with Bucket System","desc":"360° rotating head, stainless wringer, no-touch operation. Replacement heads available.","price":"From $8.90/set","moq":"MOQ: 50sets","tags":"new oem"},
          {"name":"Silicone Scrubbing Brush Set (5pcs)","desc":"Food-grade silicone, anti-bacterial. Bottle, pot, dish brushes. BPA-free.","price":"From $3.20/set","moq":"MOQ: 100sets","tags":"hot oem"},
          {"name":"Telescopic Window Cleaning Kit","desc":"Extends 1–3m. Squeegee + microfiber sleeve. Residential and commercial use.","price":"From $5.60/pc","moq":"MOQ: 50pcs","tags":"oem"},
        ]
      },
      {
        "slug": "storage-solutions",
        "title": "Storage Solutions",
        "desc": "Collapsible, stackable home organizers for closet, kitchen, and bedroom.",
        "icon": "fa-box-open",
        "sku_prefix": "SS",
        "products": [
          {"name":"Collapsible Fabric Storage Box (6pcs)","desc":"Oxford fabric + bamboo frame. Foldable flat. Lids included. 4 sizes. Custom print.","price":"From $2.80/pc","moq":"MOQ: 200pcs","tags":"hot"},
          {"name":"Vacuum Compression Bag Set (8pcs)","desc":"PA+PE material, 80% space saving. Hand pump included. Travel & home use.","price":"From $4.50/set","moq":"MOQ: 100sets","tags":"new oem"},
          {"name":"Acrylic Drawer Organizer Set (10pcs)","desc":"Crystal clear, modular, stackable. Fits standard dresser drawers. Retail-packaged.","price":"From $6.20/set","moq":"MOQ: 50sets","tags":"oem"},
          {"name":"Over-Door Storage Organizer (16 Pockets)","desc":"Non-woven fabric, door hook. 15kg capacity. Pantry, bedroom, bathroom. OEM logo.","price":"From $3.40/pc","moq":"MOQ: 100pcs","tags":"hot oem"},
        ]
      },
    ]
  },
  {
    "slug": "pet-daily",
    "title": "Pet Daily Needs",
    "desc": "Premium pet care from food accessories to orthopedic beds — OEM & private label ready.",
    "icon": "fa-paw",
    "color": "from-emerald-600 to-teal-400",
    "depth": 2,
    "subs": [
      {
        "slug": "food-treats",
        "title": "Food & Treats",
        "desc": "Healthy, natural pet snacks and feeding accessories. FDA, LFGB certified.",
        "icon": "fa-bone",
        "sku_prefix": "FT",
        "products": [
          {"name":"Natural Freeze-Dried Dog Treats (Chicken)","desc":"100% real chicken, no additives. Freeze-dried for maximum nutrition. Resealable bag.","price":"From $3.20/bag","moq":"MOQ: 200bags","tags":"hot oem"},
          {"name":"Stainless Steel Pet Bowl Set (2pcs)","desc":"304 stainless, non-slip rubber base, dishwasher safe. S/M/L sizes. Custom logo engraving.","price":"From $2.50/set","moq":"MOQ: 100sets","tags":"hot"},
          {"name":"Slow Feeder Dog Bowl (Anti-Gulp)","desc":"BPA-free PP maze design. Reduces eating speed by 10x. 4 colours. OEM available.","price":"From $3.80/pc","moq":"MOQ: 100pcs","tags":"new oem"},
          {"name":"Automatic Pet Water Fountain (2L)","desc":"Ultra-quiet pump, triple filtration, LED indicator. For cats & small dogs. CE certified.","price":"From $8.50/pc","moq":"MOQ: 50pcs","tags":"hot oem"},
        ]
      },
      {
        "slug": "grooming-tools",
        "title": "Grooming Tools",
        "desc": "Professional pet grooming kits for dogs and cats. CE certified, ergonomic design.",
        "icon": "fa-scissors",
        "sku_prefix": "GT",
        "products": [
          {"name":"Professional Pet Grooming Kit (7pcs)","desc":"Stainless steel, ergonomic handle. Scissors, comb, nail clipper. CE certified. Retail-ready.","price":"From $4.20/set","moq":"MOQ: 100sets","tags":"hot oem"},
          {"name":"Self-Cleaning Slicker Brush","desc":"Fine stainless pins, one-click fur release button. For long & short coats.","price":"From $2.80/pc","moq":"MOQ: 200pcs","tags":"hot"},
          {"name":"Pet Nail Grinder (USB Rechargeable)","desc":"Ultra-quiet motor <45dB. 2-speed. LED light. Suitable dogs & cats. CE/RoHS.","price":"From $5.60/pc","moq":"MOQ: 100pcs","tags":"new oem"},
          {"name":"Dog Bathing Brush & Shampoo Dispenser","desc":"Silicone massage bristles, integrated soap dispenser. Connects to any showerhead.","price":"From $3.90/pc","moq":"MOQ: 100pcs","tags":"oem"},
        ]
      },
      {
        "slug": "toys",
        "title": "Toys",
        "desc": "Interactive, durable pet toys. Non-toxic materials, safety tested for global markets.",
        "icon": "fa-shapes",
        "sku_prefix": "PT",
        "products": [
          {"name":"Interactive Puzzle Feeder Toy (Level 2)","desc":"ABS non-toxic plastic. 3 compartments, adjustable difficulty. Mental stimulation for dogs.","price":"From $3.50/pc","moq":"MOQ: 100pcs","tags":"hot"},
          {"name":"Catnip Plush Toy Set (6pcs)","desc":"100% organic catnip filling, cotton fabric. Assorted shapes. Machine washable. Safety tested.","price":"From $0.80/pc","moq":"MOQ: 500pcs","tags":"hot oem"},
          {"name":"Rope Chew Toy (Large Breed)","desc":"100% natural cotton rope. Promotes dental health. Available in 5 shapes. OEM packaging.","price":"From $1.50/pc","moq":"MOQ: 200pcs","tags":"new"},
          {"name":"Electronic Laser & Feather Wand Cat Toy","desc":"Auto-rotating, 3-speed, USB rechargeable. Feather + laser modes. CE certified.","price":"From $6.80/pc","moq":"MOQ: 50pcs","tags":"new oem"},
        ]
      },
      {
        "slug": "beds-furniture",
        "title": "Beds & Furniture",
        "desc": "Orthopedic pet beds, cat trees, and kennels. Washable covers, OEM branding available.",
        "icon": "fa-couch",
        "sku_prefix": "PB",
        "products": [
          {"name":"Luxury Orthopedic Dog Bed (Memory Foam)","desc":"Memory foam base, waterproof liner, removable washable cover. S/M/L/XL. OEM logo.","price":"From $6.90/pc","moq":"MOQ: 50pcs","tags":"hot oem"},
          {"name":"Cat Tree Tower (5-Level)","desc":"Sisal rope scratching posts, plush platforms, dangling toys. 160cm height. Easy assembly.","price":"From $22.00/pc","moq":"MOQ: 20pcs","tags":"new"},
          {"name":"Foldable Dog Crate (Soft-Sided)","desc":"Oxford fabric, wire frame, top & side doors. S/M/L/XL. Carry bag included.","price":"From $12.50/pc","moq":"MOQ: 30pcs","tags":"hot oem"},
          {"name":"Elevated Pet Cooling Bed","desc":"Breathable mesh, powder-coated steel frame. Off-ground design. S/M/L. No inflation needed.","price":"From $8.20/pc","moq":"MOQ: 50pcs","tags":"oem"},
        ]
      },
      {
        "slug": "health-care",
        "title": "Health Care",
        "desc": "Pet wellness products: vitamins, dental care, eye wipes and safety gear.",
        "icon": "fa-heart-pulse",
        "sku_prefix": "PH",
        "products": [
          {"name":"Pet Dental Chew Sticks (30pcs/bag)","desc":"Enzymatic formula, fights plaque & tartar. Chicken flavour. For dogs 10kg+. LFGB certified.","price":"From $2.80/bag","moq":"MOQ: 200bags","tags":"hot oem"},
          {"name":"Pet Eye & Ear Cleaning Wipes (100pcs)","desc":"Fragrance-free, aloe vera formula. Pre-moistened, individually wrapped. Safe for daily use.","price":"From $1.90/pack","moq":"MOQ: 200packs","tags":"hot"},
          {"name":"Adjustable Pet Reflective Safety Vest","desc":"High-vis neon fabric, reflective strips. XS-XL. For walking in low-light conditions.","price":"From $2.60/pc","moq":"MOQ: 100pcs","tags":"new oem"},
          {"name":"Pet First Aid Kit (14-piece)","desc":"Bandages, antiseptic wipes, tweezers, thermometer. Compact zippered case. Retail-ready.","price":"From $5.50/kit","moq":"MOQ: 100kits","tags":"oem"},
        ]
      },
    ]
  },
  {
    "slug": "beauty-care",
    "title": "Beauty & Personal Care",
    "desc": "Skincare, haircare, and cosmetics — paraben-free formulas, private label ready.",
    "icon": "fa-spa",
    "color": "from-pink-500 to-rose-400",
    "depth": 2,
    "subs": [
      {
        "slug": "skincare",
        "title": "Skincare",
        "desc": "Dermatologist-tested formulas. Paraben-free, cruelty-free. Private label MOQ 200 sets.",
        "icon": "fa-droplet",
        "sku_prefix": "SK",
        "products": [
          {"name":"Vitamin C Brightening Serum (30ml)","desc":"20% Vit-C + hyaluronic acid. Paraben-free, dermatologist tested. Private label MOQ 200pcs.","price":"From $3.50/pc","moq":"MOQ: 200pcs","tags":"hot oem"},
          {"name":"Niacinamide Moisturizer (50ml)","desc":"10% niacinamide, pore-minimizing. All skin types. OEM formula & packaging available.","price":"From $4.20/pc","moq":"MOQ: 200pcs","tags":"new oem"},
          {"name":"Retinol Night Cream (50ml)","desc":"0.5% encapsulated retinol, anti-aging. Fragrance-free. FDA-compliant formulation.","price":"From $5.80/pc","moq":"MOQ: 200pcs","tags":"hot"},
          {"name":"Hydrating Sheet Mask Box (20pcs)","desc":"Korean-style bio-cellulose mask. Hyaluronic acid + peptides. OEM printing on box.","price":"From $0.45/pc","moq":"MOQ: 1000pcs","tags":"hot oem"},
        ]
      },
      {
        "slug": "haircare",
        "title": "Haircare",
        "desc": "Sulfate-free salon-grade shampoo, conditioner and treatment. Custom fragrance options.",
        "icon": "fa-wind",
        "sku_prefix": "HC",
        "products": [
          {"name":"Keratin Repair Shampoo (500ml)","desc":"Sulfate-free, keratin-infused. For damaged & color-treated hair. Custom fragrance OEM.","price":"From $3.80/bottle","moq":"MOQ: 200bottles","tags":"hot oem"},
          {"name":"Argan Oil Hair Mask (250ml)","desc":"Deep conditioning, frizz control. 5-minute treatment. Salon & retail grade.","price":"From $4.50/jar","moq":"MOQ: 200jars","tags":"new oem"},
          {"name":"Biotin Scalp Serum (100ml)","desc":"Biotin + caffeine formula. Anti-hair loss, promotes growth. Dropper bottle.","price":"From $5.20/pc","moq":"MOQ: 200pcs","tags":"hot"},
          {"name":"Ionic Hair Dryer (2200W)","desc":"Negative ion technology, 3 heat/2 speed settings. CE/RoHS. Diffuser attachment included.","price":"From $12.50/pc","moq":"MOQ: 50pcs","tags":"oem"},
        ]
      },
      {
        "slug": "makeup",
        "title": "Makeup",
        "desc": "Long-wear, cruelty-free cosmetics. OEM formula development and custom packaging.",
        "icon": "fa-wand-sparkles",
        "sku_prefix": "MK",
        "products": [
          {"name":"Matte Liquid Lipstick (24 shades)","desc":"24-hour wear, transfer-proof. Vegan, cruelty-free. Slim bullet packaging. OEM shades.","price":"From $1.80/pc","moq":"MOQ: 300pcs","tags":"hot oem"},
          {"name":"Full Coverage Foundation (30ml)","desc":"SPF 30, buildable coverage. 40 shades. Pump bottle. Vegan, fragrance-free formula.","price":"From $3.50/pc","moq":"MOQ: 200pcs","tags":"new oem"},
          {"name":"Eyeshadow Palette (18 colors)","desc":"Matte & shimmer finish. Highly pigmented. Vegan. Custom shade curation available.","price":"From $4.80/palette","moq":"MOQ: 100pcs","tags":"hot"},
          {"name":"Waterproof Mascara (Black)","desc":"Volumizing brush, long-lasting 12-hour formula. Vitamin E enriched. CE certified.","price":"From $1.50/pc","moq":"MOQ: 300pcs","tags":"oem"},
        ]
      },
      {
        "slug": "bath-body",
        "title": "Bath & Body",
        "desc": "Luxurious bath bombs, body scrubs, and shower gels. Natural ingredients, gift-set packaging.",
        "icon": "fa-soap",
        "sku_prefix": "BB",
        "products": [
          {"name":"Fizzing Bath Bomb Set (12pcs)","desc":"Essential oil scented, skin-softening shea butter core. Gift box packaging. OEM label.","price":"From $0.90/pc","moq":"MOQ: 500pcs","tags":"hot oem"},
          {"name":"Coffee Body Scrub (200g)","desc":"Natural coffee grounds + coconut oil. Exfoliating, anti-cellulite. Kraft jar. Vegan.","price":"From $3.20/jar","moq":"MOQ: 200jars","tags":"new oem"},
          {"name":"Vitamin E Body Lotion (400ml)","desc":"Fast-absorbing, 48-hour moisture. Fragrance-free option. Pump bottle. OEM available.","price":"From $2.80/bottle","moq":"MOQ: 200bottles","tags":"hot"},
          {"name":"Shower Gel Gift Set (3pcs)","desc":"3 x 100ml travel sizes. Bamboo charcoal, rose, and citrus scents. Ribbon-tied gift box.","price":"From $4.50/set","moq":"MOQ: 100sets","tags":"oem"},
        ]
      },
      {
        "slug": "fragrances",
        "title": "Fragrances",
        "desc": "Eau de Parfum, reed diffusers, and car fresheners. Custom scent development available.",
        "icon": "fa-bottle-droplet",
        "sku_prefix": "FR",
        "products": [
          {"name":"Eau de Parfum (50ml) — Custom Scent","desc":"Long-lasting 8-hour fragrance. Custom scent development, unique bottle design. OEM/ODM.","price":"From $6.50/bottle","moq":"MOQ: 200bottles","tags":"hot oem"},
          {"name":"Reed Diffuser Set (200ml + 8 sticks)","desc":"Premium fragrance oil, natural rattan reeds. 60+ day diffusion. 20 scent options.","price":"From $4.20/set","moq":"MOQ: 100sets","tags":"new oem"},
          {"name":"Car Air Freshener (Vent Clip)","desc":"Refillable, 4-week long-lasting. 15 scents. Compact, anti-spill design. Display box available.","price":"From $0.80/pc","moq":"MOQ: 500pcs","tags":"hot"},
          {"name":"Scented Candle Tin (200g)","desc":"Soy wax, cotton wick, 45-hour burn time. 20 fragrance options. Custom label printing.","price":"From $3.50/pc","moq":"MOQ: 200pcs","tags":"oem"},
        ]
      },
    ]
  },
  {
    "slug": "craft-decor",
    "title": "Craft & Decor",
    "desc": "Home decor, DIY supplies, art materials, and party decorations — trend-led, retail-ready.",
    "icon": "fa-palette",
    "color": "from-purple-600 to-violet-400",
    "depth": 2,
    "subs": [
      {
        "slug": "home-decor",
        "title": "Home Decor",
        "desc": "Boho, Scandinavian, and contemporary decor. 100% natural materials, gift-box packaging.",
        "icon": "fa-house-chimney",
        "sku_prefix": "HD",
        "products": [
          {"name":"Boho Macrame Wall Hanging","desc":"100% natural cotton rope, handcrafted. Driftwood rod included. Gift-box ready. Trending globally.","price":"From $1.90/pc","moq":"MOQ: 100pcs","tags":"hot oem"},
          {"name":"Geometric Terracotta Planter Set (3pcs)","desc":"Hand-painted terracotta, drainage hole with plug. S/M/L nested set. 8 colour combos.","price":"From $5.60/set","moq":"MOQ: 50sets","tags":"new"},
          {"name":"Scented Pillar Candle Set (3pcs)","desc":"Soy-paraffin blend, cotton wick, 60hr burn time. 10 scents. OEM label printing.","price":"From $3.80/set","moq":"MOQ: 100sets","tags":"hot oem"},
          {"name":"Rattan Photo Frame Set (5pcs)","desc":"Natural rattan + MDF. 4x6, 5x7, 8x10 sizes. Tabletop & wall hanging. OEM packaging.","price":"From $4.20/set","moq":"MOQ: 50sets","tags":"oem"},
        ]
      },
      {
        "slug": "diy-supplies",
        "title": "DIY Supplies",
        "desc": "Craft kits, tools and materials for hobbyists and professional crafters worldwide.",
        "icon": "fa-screwdriver-wrench",
        "sku_prefix": "DI",
        "products": [
          {"name":"Resin Art Starter Kit","desc":"500g crystal clear epoxy resin + hardener, pigments, molds. Beginner-friendly instructions.","price":"From $8.50/kit","moq":"MOQ: 50kits","tags":"hot oem"},
          {"name":"Diamond Painting Kit (40×50cm)","desc":"5D round drill, pre-printed canvas, light pad included. 200+ designs available.","price":"From $4.80/kit","moq":"MOQ: 100kits","tags":"hot"},
          {"name":"Knitting & Crochet Starter Set","desc":"Bamboo hooks (10 sizes) + 5 skeins merino blend yarn + stitch markers. Gift-box packed.","price":"From $6.20/set","moq":"MOQ: 50sets","tags":"new oem"},
          {"name":"Wooden Letter & Shape Cutouts (50pcs)","desc":"Unfinished birch plywood, laser cut, 3mm thickness. 26 alphabet + numbers + symbols.","price":"From $2.50/set","moq":"MOQ: 100sets","tags":"oem"},
        ]
      },
      {
        "slug": "art-materials",
        "title": "Art Materials",
        "desc": "Professional and student-grade paints, brushes, and drawing tools for global markets.",
        "icon": "fa-paintbrush",
        "sku_prefix": "AM",
        "products": [
          {"name":"Professional Acrylic Paint Set (24 colors)","desc":"48ml tubes, lightfast, non-toxic. Artists & students grade. AP certified.","price":"From $6.80/set","moq":"MOQ: 100sets","tags":"hot oem"},
          {"name":"Artist Brush Set (15pcs)","desc":"Hand-tied, synthetic/natural mix, wooden handles. Assorted sizes. Velvet roll pouch.","price":"From $4.50/set","moq":"MOQ: 100sets","tags":"new oem"},
          {"name":"Watercolor Field Sketch Set","desc":"24 pan watercolors, mixing tray, 2 brushes, water brush. Compact tin case. Travel-ready.","price":"From $5.20/set","moq":"MOQ: 50sets","tags":"hot"},
          {"name":"Sketch Pencil Set (24pcs, 6H-8B)","desc":"Cedar wood, break-resistant graphite. 6H to 8B range. Tin case. AP certified.","price":"From $3.80/set","moq":"MOQ: 100sets","tags":"oem"},
        ]
      },
      {
        "slug": "party-decorations",
        "title": "Party Decorations",
        "desc": "Balloons, banners, tableware and thematic kits. Custom print for events and retail.",
        "icon": "fa-champagne-glasses",
        "sku_prefix": "PD",
        "products": [
          {"name":"Balloon Arch Garland Kit (120pcs)","desc":"Latex & foil mix, assorted sizes and colours. Strip, dots, pump included. 1 arch set.","price":"From $4.50/kit","moq":"MOQ: 100kits","tags":"hot oem"},
          {"name":"Custom Printed Party Banner","desc":"Personalized text & design. 300cm length, glitter card or banner fabric. MOQ 50pcs.","price":"From $1.20/pc","moq":"MOQ: 50pcs","tags":"new oem"},
          {"name":"Disposable Party Tableware Set (60pcs)","desc":"Plates, cups, napkins for 10 guests. 5 themed designs. Biodegradable options available.","price":"From $3.80/set","moq":"MOQ: 100sets","tags":"hot"},
          {"name":"LED Fairy String Lights (10m, 100 LEDs)","desc":"USB + AA battery dual power. 8 flash modes. Indoor/outdoor IP44. OEM packaging.","price":"From $2.20/pc","moq":"MOQ: 200pcs","tags":"oem"},
        ]
      },
      {
        "slug": "handicrafts",
        "title": "Handicrafts",
        "desc": "Handmade baskets, ceramics, woven textiles — unique ethnic crafts for global boutiques.",
        "icon": "fa-hands",
        "sku_prefix": "HN",
        "products": [
          {"name":"Handwoven Seagrass Storage Basket Set (3)","desc":"Natural seagrass, leather handles. S/M/L nested. Nursery & living room. OEM label.","price":"From $7.50/set","moq":"MOQ: 30sets","tags":"hot oem"},
          {"name":"Hand-Painted Ceramic Mug (350ml)","desc":"Stoneware, dishwasher safe, lead-free glaze. 20 designs or custom artwork. OEM available.","price":"From $3.20/pc","moq":"MOQ: 100pcs","tags":"new oem"},
          {"name":"Bamboo Woven Placemats (Set of 4)","desc":"100% natural bamboo, heat-resistant. 30×45cm. 6 weave patterns. Retail-packaged.","price":"From $2.80/set","moq":"MOQ: 100sets","tags":"hot"},
          {"name":"Macrame Cotton Coaster Set (6pcs)","desc":"Handknotted, natural cotton rope. 10cm diameter. Gift-box packed. OEM packaging.","price":"From $3.50/set","moq":"MOQ: 100sets","tags":"oem"},
        ]
      },
    ]
  },
  {
    "slug": "other-supplies",
    "title": "Other Supplies",
    "desc": "Stationery, electronics accessories, travel gear, and sports equipment for global buyers.",
    "icon": "fa-boxes-stacked",
    "color": "from-orange-500 to-amber-400",
    "depth": 2,
    "subs": [
      {
        "slug": "stationery",
        "title": "Stationery",
        "desc": "Office and school stationery — pens, notebooks, planners. Custom branding available.",
        "icon": "fa-pen-to-square",
        "sku_prefix": "SN",
        "products": [
          {"name":"Gel Pen Set (48pcs, Assorted Colors)","desc":"0.5mm tip, quick-dry ink. For journal, bullet planner, sketch. OEM barrel printing.","price":"From $0.18/pc","moq":"MOQ: 1000pcs","tags":"hot oem"},
          {"name":"A5 Hardcover Dot-Grid Notebook","desc":"160 pages, 100gsm paper, lay-flat binding. 6 cover colours. Custom deboss logo.","price":"From $2.80/pc","moq":"MOQ: 200pcs","tags":"new oem"},
          {"name":"Desk Organizer Set (6pcs, Acrylic)","desc":"Clear acrylic, modular layout. Pen holder, tray, file stand. Office & retail grade.","price":"From $5.50/set","moq":"MOQ: 100sets","tags":"hot"},
          {"name":"Washi Tape Collection (20 rolls)","desc":"20 assorted designs, 15mm wide, 10m per roll. For planners, scrapbooking, packaging.","price":"From $3.20/set","moq":"MOQ: 100sets","tags":"oem"},
        ]
      },
      {
        "slug": "electronics-accessories",
        "title": "Electronics Accessories",
        "desc": "Phone cases, charging cables, power banks and laptop accessories. CE/RoHS certified.",
        "icon": "fa-plug-circle-bolt",
        "sku_prefix": "EA",
        "products": [
          {"name":"65W GaN USB-C Charger (3-Port)","desc":"65W total output, PD 3.0 + QC 4.0. Foldable plug. CE/FCC/RoHS certified. OEM logo.","price":"From $8.50/pc","moq":"MOQ: 100pcs","tags":"hot oem"},
          {"name":"Braided USB-C to USB-C Cable (2m)","desc":"100W fast charge, 10Gbps data. Nylon braided, zinc alloy connectors. OEM packaging.","price":"From $1.80/pc","moq":"MOQ: 500pcs","tags":"new"},
          {"name":"10000mAh Slim Power Bank","desc":"22.5W fast charge, dual output, LED indicator. 12mm slim. Airline approved. OEM print.","price":"From $9.20/pc","moq":"MOQ: 50pcs","tags":"hot oem"},
          {"name":"Laptop Stand (Adjustable, Aluminium)","desc":"6 angle adjustments, foldable, 10–17 inch compatible. 1kg max load. Anti-slip pads.","price":"From $7.80/pc","moq":"MOQ: 50pcs","tags":"oem"},
        ]
      },
      {
        "slug": "travel-gear",
        "title": "Travel Gear",
        "desc": "Packing cubes, toiletry bags and travel organizers — Amazon FBA-ready packaging.",
        "icon": "fa-suitcase-rolling",
        "sku_prefix": "TG",
        "products": [
          {"name":"6-Piece Travel Packing Cube Set","desc":"Waterproof Oxford fabric, zip compression. S/M/L/XL + shoe bag + laundry bag.","price":"From $3.20/set","moq":"MOQ: 100sets","tags":"hot oem"},
          {"name":"Hanging Toiletry Organizer Bag","desc":"Oxford fabric, waterproof lining, hook. 6 compartments. 4 colours. OEM logo.","price":"From $4.50/pc","moq":"MOQ: 100pcs","tags":"new oem"},
          {"name":"Portable Luggage Scale (Digital)","desc":"Up to 50kg, 0.1g precision. Auto-off. Foldable handle. CE certified. Retail box.","price":"From $3.80/pc","moq":"MOQ: 100pcs","tags":"hot"},
          {"name":"Travel Neck Pillow (Memory Foam)","desc":"Ergonomic contour, machine-washable velour cover. Snap buckle. Carry pouch included.","price":"From $4.20/pc","moq":"MOQ: 100pcs","tags":"oem"},
        ]
      },
      {
        "slug": "sports-equipment",
        "title": "Sports Equipment",
        "desc": "Fitness, outdoor and yoga equipment. Safety certified, Amazon and retail-ready.",
        "icon": "fa-dumbbell",
        "sku_prefix": "SE",
        "products": [
          {"name":"TPE Yoga Mat (6mm, Non-slip)","desc":"Eco-friendly TPE, 183×61cm, 6mm cushion. Alignment lines. Carry strap. OEM print.","price":"From $5.80/pc","moq":"MOQ: 50pcs","tags":"hot oem"},
          {"name":"Resistance Band Set (5 levels)","desc":"Natural latex, door anchor + handles included. 10–50lb resistance. OEM packaging.","price":"From $3.50/set","moq":"MOQ: 100sets","tags":"new oem"},
          {"name":"Adjustable Dumbbell Set (2×5kg)","desc":"Rubber-coated cast iron. Knurled grip handle. Weight plates: 0.5/1/1.5/2kg. Pair.","price":"From $14.50/pair","moq":"MOQ: 20pairs","tags":"hot"},
          {"name":"Foam Roller (60cm, High Density)","desc":"High-density EVA foam. 30cm/45cm/60cm options. Smooth & textured surface. OEM label.","price":"From $4.20/pc","moq":"MOQ: 50pcs","tags":"oem"},
        ]
      },
    ]
  },
  ]


# 获取分类数据
CATEGORIES = get_categories()

# ─────────────────────────────────────────────────────────────
# HTML BUILDERS
# ─────────────────────────────────────────────────────────────

NAVBAR_LOGO_SVG = """<svg class="w-5 h-5 fill-white" viewBox="0 0 24 24"><path d="M12 2a4 4 0 1 1 0 8 4 4 0 0 1 0-8zm0 2a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm-1 6.07V11H7a1 1 0 1 0 0 2h4v7.93A9.01 9.01 0 0 1 3.05 13H5a1 1 0 1 0 0-2H3.05A9.01 9.01 0 0 1 11 3.07V11h2V3.07A9.01 9.01 0 0 1 20.95 11H19a1 1 0 1 0 0 2h1.95A9.01 9.01 0 0 1 13 20.93V13h4a1 1 0 1 0 0-2h-4v-2.93z"/></svg>"""

WA_SVG = """<svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.570-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.570-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>"""

WA_SVG_SM = """<svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.570-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.570-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>"""

WA_FLOAT = f"""<a href="https://wa.me/{WA}" target="_blank" class="fixed bottom-6 right-6 w-14 h-14 bg-[#25D366] rounded-full flex items-center justify-center shadow-xl z-50 hover:scale-110 transition-transform" aria-label="WhatsApp">{WA_SVG}</a>"""

JS_MODAL = (
"<script>\n"
"function filterProd(tag,btn){\n"
"  document.querySelectorAll('.filter-btn').forEach(b=>{b.classList.remove('active');});\n"
"  btn.classList.add('active');\n"
"  document.querySelectorAll('#prod-grid .prod-card').forEach(c=>{\n"
"    c.style.display=(tag==='all'||c.dataset.tag.includes(tag))?'':'none';\n"
"  });\n"
"}\n"
"function openDetail(card){\n"
"  const img=card.querySelector('img');\n"
"  const imgSrc=img?img.getAttribute('src'):'';\n"
"  const folder=imgSrc.replace(/main\\.jpg.*/,'');\n"
"  const name=card.querySelector('h3').textContent;\n"
"  const ps=card.querySelectorAll('p');\n"
"  const desc=ps[1]?ps[1].textContent:'';\n"
"  const price=card.querySelector('.text-brand').textContent;\n"
"  const moqEl=card.querySelector('.text-gray-400:last-child');\n"
"  const moq=moqEl?moqEl.textContent.replace('MOQ: ',''):'';\n"
"  const sku=ps[0]?ps[0].textContent:'';\n"
"  const galleryData=card.dataset.gallery;\n"
"  document.getElementById('modal-name').textContent=name;\n"
"  document.getElementById('modal-desc').textContent=desc;\n"
"  document.getElementById('modal-price').textContent=price;\n"
"  document.getElementById('modal-moq').textContent=moq;\n"
"  document.getElementById('modal-sku').textContent=sku;\n"
"  document.getElementById('modal-main-img').src=imgSrc;\n"
"  document.getElementById('modal-main-img').alt=name;\n"
"  const tw=document.getElementById('modal-thumbs');\n"
"  tw.innerHTML='';\n"
"  let imageList=[imgSrc];\n"
"  if(galleryData){\n"
"    try{const gallery=JSON.parse(galleryData);if(Array.isArray(gallery)&&gallery.length>0){imageList=imageList.concat(gallery);}}catch(e){}\n"
"  }\n"
"  if(imageList.length===1){\n"
"    [folder+'detail1.jpg',folder+'detail2.jpg',folder+'detail3.jpg',folder+'detail4.jpg'].forEach(src=>{imageList.push(src);});\n"
"  }\n"
"  imageList.forEach((src,i)=>{\n"
"    const im=document.createElement('img');\n"
"    im.src=src;im.className='thumb w-full h-12 object-cover rounded-lg'+(i===0?' active':'');\n"
"    im.onerror=function(){this.remove();};\n"
"    im.onclick=function(e){\n"
"      e.stopPropagation();\n"
"      document.getElementById('modal-main-img').src=this.src;\n"
"      tw.querySelectorAll('.thumb').forEach(t=>t.classList.remove('active'));\n"
"      this.classList.add('active');\n"
"    };\n"
"    tw.appendChild(im);\n"
"  });\n"
"  document.getElementById('modal-wa').href='https://wa.me/8618735731692?text='+encodeURIComponent('Hi! I am interested in: '+name+' ('+sku+'). Please send pricing and availability.');\n"
"  document.getElementById('detail-modal').classList.remove('hidden');\n"
"  document.body.style.overflow='hidden';\n"
"}\n"
"function closeDetail(){\n"
"  document.getElementById('detail-modal').classList.add('hidden');\n"
"  document.body.style.overflow='';\n"
"}\n"
"document.getElementById('detail-modal').addEventListener('click',function(e){if(e.target===this)closeDetail();});\n"
"document.addEventListener('keydown',e=>{if(e.key==='Escape')closeDetail();});\n"
"<" + "/script>\n"
)

def modal_html(root):
    return f"""
<div id="detail-modal" class="hidden fixed inset-0 bg-black/60 z-[999] overflow-y-auto">
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-3xl w-full shadow-2xl relative">
      <button onclick="closeDetail()" class="absolute top-4 right-4 w-9 h-9 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center z-10"><i class="fa-solid fa-times text-gray-600"></i></button>
      <div class="grid md:grid-cols-2 gap-0">
        <div class="p-6 border-r border-gray-100">
          <div class="rounded-xl overflow-hidden bg-accent h-64 mb-3"><img id="modal-main-img" src="" alt="" class="w-full h-full object-contain"/></div>
          <div id="modal-thumbs" class="grid grid-cols-5 gap-1.5"></div>
        </div>
        <div class="p-6">
          <p id="modal-sku" class="text-xs text-gray-400 mb-1"></p>
          <h3 id="modal-name" class="text-xl font-bold mb-3"></h3>
          <p id="modal-desc" class="text-sm text-gray-500 leading-relaxed mb-4"></p>
          <div class="bg-accent rounded-xl p-4 mb-4">
            <div class="flex justify-between text-sm mb-2"><span class="text-gray-500">Unit Price</span><span id="modal-price" class="font-bold text-brand"></span></div>
            <div class="flex justify-between text-sm"><span class="text-gray-500">MOQ</span><span id="modal-moq" class="font-medium text-gray-700"></span></div>
          </div>
          <a id="modal-wa" href="https://wa.me/{WA}" target="_blank"
             class="flex items-center justify-center gap-2 w-full bg-[#25D366] text-white font-bold py-3 rounded-xl mb-2 hover:opacity-90 text-sm">
            {WA_SVG} Chat on WhatsApp
          </a>
          <a href="{root}index.html#contact" class="flex items-center justify-center gap-2 w-full border-2 border-brand text-brand font-semibold py-2.5 rounded-xl hover:bg-accent text-sm">
            <i class="fa-solid fa-envelope"></i> Send Email Inquiry
          </a>
        </div>
      </div>
    </div>
  </div>
</div>"""

def navbar_html(root, parent_title, parent_path, current_title):
    return f"""
<div class="bg-brand text-white text-xs py-2 px-4 text-center">
  🚢 Factory Direct · Global Shipping · MOQ Flexible —
  <a href="mailto:{EMAIL}" class="underline ml-1">{EMAIL}</a>
  <a href="https://wa.me/{WA}" target="_blank" class="ml-3 underline">WhatsApp: +86 18735731692</a>
</div>
<nav class="bg-white shadow-sm sticky top-0 z-50">
  <div class="max-w-screen-xl mx-auto px-4 lg:px-8 flex items-center justify-between h-16">
    <a href="{root}index.html" class="flex items-center gap-2">
      <img src="{root}images/logo/logo.png" alt="{BRAND} Logo" class="h-9 w-auto"
           onerror="this.style.display='none';document.getElementById('lt').style.display='flex'"/>
      <div id="lt" class="hidden items-center gap-2">
        <div class="w-9 h-9 rounded-lg bg-brand flex items-center justify-center">{NAVBAR_LOGO_SVG}</div>
        <div class="leading-none">
          <div class="font-extrabold text-base text-brand">{BRAND}</div>
          <div class="text-[9px] text-gray-400 font-medium tracking-wide">{SLOGAN.upper()}</div>
        </div>
      </div>
    </a>
    <div class="hidden md:flex items-center gap-2 text-sm text-gray-500">
      <a href="{root}index.html" class="hover:text-brand">Home</a>
      <i class="fa-solid fa-chevron-right text-[10px]"></i>
      <a href="{parent_path}" class="hover:text-brand">{parent_title}</a>
      <i class="fa-solid fa-chevron-right text-[10px]"></i>
      <span class="text-brand font-medium">{current_title}</span>
    </div>
    <div class="flex items-center gap-3">
      <a href="https://wa.me/{WA}" target="_blank" class="hidden sm:flex items-center gap-1.5 text-[#25D366] text-sm font-medium hover:opacity-80">
        {WA_SVG} Chat Now
      </a>
      <a href="{root}index.html#contact" class="bg-brand text-white text-sm font-semibold px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">Get Quote</a>
    </div>
  </div>
</nav>"""

def head_html(title):
    script_open = "<script"
    script_close = "<" + "/script>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title} — {BRAND} | {COMPANY}</title>
  {script_open} src="https://cdn.tailwindcss.com">{script_close}
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
  {script_open}>tailwind.config={{theme:{{extend:{{colors:{{brand:{{DEFAULT:'#165DFF',dark:'#0E3ECC'}},accent:'#F0F7FF'}},fontFamily:{{sans:['Inter','sans-serif']}}}}}}}}{script_close}
  <style>
    body{{font-family:'Inter',sans-serif;color:#333}}
    .thumb{{cursor:pointer;border:2px solid transparent;border-radius:8px;transition:border-color 0.2s}}
    .thumb.active,.thumb:hover{{border-color:#165DFF}}
    .prod-card{{transition:transform 0.2s,box-shadow 0.2s}}
    .prod-card:hover{{transform:translateY(-5px);box-shadow:0 16px 40px rgba(22,93,255,0.15)}}
    .img-placeholder{{background:linear-gradient(135deg,#e8f0fe,#c7d8fd);border:2px dashed #93b4fb;border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#165DFF;padding:1rem;text-align:center}}
    .filter-btn.active{{background:#165DFF;color:#fff;border-color:#165DFF}}
  </style>
  <!-- Vercel Web Analytics -->
  {script_open}>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments);}};{script_close}
  {script_open} defer src="/_vercel/insights/script.js">{script_close}
</head>
<body class="bg-gray-50">"""

def product_cards_html(products, sku_prefix):
    cards = ""
    for i, p in enumerate(products, 1):
        sku = f"{sku_prefix}{i:03d}"
        tags = p["tags"]
        badges = ""
        if "hot" in tags:
            badges += '<span class="absolute top-2 left-2 bg-orange-500 text-white text-[10px] font-bold px-2 py-0.5 rounded">HOT</span>'
        if "new" in tags:
            badges += '<span class="absolute top-2 left-2 bg-brand text-white text-[10px] font-bold px-2 py-0.5 rounded">NEW</span>'
        if "oem" in tags:
            badges += '<span class="absolute top-2 right-2 bg-indigo-500 text-white text-[10px] font-bold px-2 py-0.5 rounded">OEM</span>'
        name_escaped = p['name'].replace('"', '&quot;')
        
        # 构建图库数据（用于弹窗显示多张图片）
        # 图库图片已同步为 detail1.jpg, detail2.jpg 等
        gallery_data = ""
        if p.get('gallery') and len(p['gallery']) > 0:
            import json
            # 构建图库图片URL列表 (detail1.jpg, detail2.jpg, ...)
            gallery_urls = []
            for i in range(len(p['gallery'])):
                gallery_urls.append(f"{sku}/detail{i+1}.jpg")
            gallery_data = f' data-gallery=\'{json.dumps(gallery_urls)}\''
        
        cards += f"""
    <div class="prod-card bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-100 cursor-pointer" data-tag="{tags}"{gallery_data} onclick="openDetail(this)">
      <div class="relative h-48 overflow-hidden bg-accent">
        <img src="{sku}/main.jpg" alt="{name_escaped}" class="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
             onerror="this.parentElement.innerHTML='&lt;div class=&quot;img-placeholder w-full h-full&quot;&gt;&lt;i class=&quot;fa-solid fa-image text-3xl mb-2 opacity-30&quot;&gt;&lt;/i&gt;&lt;span class=&quot;text-xs font-medium&quot;&gt;{sku}/main.jpg&lt;/span&gt;&lt;/div&gt;'"/>
        {badges}
      </div>
      <div class="p-4">
        <p class="text-[10px] text-gray-400 mb-0.5">SKU: {sku}</p>
        <h3 class="font-semibold text-sm leading-snug mb-1">{p['name']}</h3>
        <p class="text-[11px] text-gray-500 mb-3 line-clamp-2">{p['desc']}</p>
        <div class="flex items-center justify-between">
          <span class="text-brand font-bold text-sm">{p['price']}</span>
          <span class="text-[10px] text-gray-400">{p['moq']}</span>
        </div>
      </div>
    </div>"""
    return cards

def sub_page_html(cat, sub, root):
    from urllib.parse import quote
    wa_msg = quote(f"Hi! I am interested in your {sub['title']} products. Please send catalog and pricing.")
    wa_empty_msg = quote(f"Hi! I'm interested in your {sub['title']} products. This category is empty on your site — can you share your latest catalog and pricing?")
    
    has_products = len(sub["products"]) > 0
    
    if has_products:
        cards = product_cards_html(sub["products"], sub["sku_prefix"])
        product_section = f"""
  <div class="flex flex-wrap items-center justify-between gap-4 mb-8">
    <p class="text-sm text-gray-500"><span class="font-semibold text-gray-800">{sub['title']}</span> — All Products</p>
    <div class="flex gap-2 flex-wrap">
      <button onclick="filterProd('all',this)" class="filter-btn active text-xs px-4 py-1.5 rounded-full border-2 border-brand bg-brand text-white font-medium">All</button>
      <button onclick="filterProd('new',this)" class="filter-btn text-xs px-4 py-1.5 rounded-full border-2 border-gray-200 text-gray-500 font-medium hover:border-brand hover:text-brand">New Arrivals</button>
      <button onclick="filterProd('hot',this)" class="filter-btn text-xs px-4 py-1.5 rounded-full border-2 border-gray-200 text-gray-500 font-medium hover:border-brand hover:text-brand">Best Sellers</button>
      <button onclick="filterProd('oem',this)" class="filter-btn text-xs px-4 py-1.5 rounded-full border-2 border-gray-200 text-gray-500 font-medium hover:border-brand hover:text-brand">OEM Available</button>
    </div>
  </div>
  <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5" id="prod-grid">
    {cards}
  </div>"""
    else:
        product_section = f"""
  <div class="max-w-md mx-auto bg-white rounded-2xl shadow-sm border border-gray-100 px-8 py-10 text-center">
    <div class="w-16 h-16 rounded-full bg-accent flex items-center justify-center mx-auto mb-5">
      <i class="fa-solid fa-box-open text-2xl text-brand"></i>
    </div>
    <h2 class="text-lg font-bold text-gray-800 mb-2">No products listed yet</h2>
    <p class="text-sm text-gray-500 mb-6 leading-relaxed">
      This category is being prepared. Send us your requirements — our team will get back to you within 2 hours with the right options.
    </p>
    <a href="https://wa.me/{WA}?text={wa_empty_msg}" target="_blank"
       class="inline-flex items-center gap-2 bg-[#25D366] text-white font-semibold px-5 py-2.5 rounded-xl text-sm hover:opacity-90 shadow-sm transition-all">
      {WA_SVG_SM} Chat on WhatsApp
    </a>
  </div>"""

    return f"""{head_html(sub['title'])}
{navbar_html(root, cat['title'], f"{root}products/{cat['slug']}/index.html", sub['title'])}
<section class="bg-gradient-to-r from-brand to-blue-500 text-white py-12 px-4">
  <div class="max-w-screen-xl mx-auto">
    <div class="flex items-center gap-3 mb-3">
      <div class="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center">
        {render_icon(sub.get('icon'), sub.get('icon_type', 'fontawesome'), 'md', '', root)}
      </div>
      <h1 class="text-3xl md:text-4xl font-extrabold">{sub['title']}</h1>
    </div>
    <p class="text-white/80 text-sm max-w-xl">{sub['desc']}</p>
    <div class="flex flex-wrap gap-3 mt-5 text-xs">
      <span class="bg-white/20 px-3 py-1.5 rounded-full">✓ ISO 9001 Certified</span>
      <span class="bg-white/20 px-3 py-1.5 rounded-full">✓ OEM / Private Label</span>
      <span class="bg-white/20 px-3 py-1.5 rounded-full">✓ MOQ Flexible</span>
      <span class="bg-white/20 px-3 py-1.5 rounded-full">✓ Global Shipping</span>
    </div>
  </div>
</section>
<main class="max-w-screen-xl mx-auto px-4 lg:px-8 py-12">
  {product_section}
  <div class="mt-12 bg-accent rounded-2xl p-8 flex flex-col md:flex-row items-center justify-between gap-5">
    <div>
      <h3 class="font-bold text-lg mb-1">Need a Custom {sub['title']} Solution?</h3>
      <p class="text-gray-500 text-sm">OEM, ODM, private label — send us your requirements and we will handle the rest.</p>
    </div>
    <div class="flex gap-3 flex-shrink-0">
      <a href="https://wa.me/{WA}?text={wa_msg}" target="_blank"
         class="flex items-center gap-2 bg-[#25D366] text-white font-semibold px-5 py-2.5 rounded-xl text-sm hover:opacity-90">
        {WA_SVG_SM} WhatsApp
      </a>
      <a href="{root}index.html#contact" class="bg-brand text-white font-semibold px-5 py-2.5 rounded-xl text-sm hover:bg-blue-700 transition-colors">Email Inquiry</a>
    </div>
  </div>
</main>
{modal_html(root)}
{WA_FLOAT}
{JS_MODAL}
</body></html>"""

def cat_index_html(cat, root):
    sub_cards = ""
    for sub in cat["subs"]:
        sub_cards += f"""
    <a href="{sub['slug']}/index.html"
       class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-200 flex flex-col items-center text-center gap-3">
      <div class="w-14 h-14 rounded-2xl bg-accent flex items-center justify-center">
        {render_icon(sub.get('icon'), sub.get('icon_type', 'fontawesome'), 'lg', 'text-brand', root)}
      </div>
      <h3 class="font-bold text-base">{sub['title']}</h3>
      <p class="text-xs text-gray-500 line-clamp-2">{sub['desc']}</p>
      <span class="text-brand text-xs font-semibold mt-auto flex items-center gap-1">
        View Products <i class="fa-solid fa-arrow-right text-[10px]"></i>
      </span>
    </a>"""
    from urllib.parse import quote
    wa_msg = quote(f"Hi! I am interested in your {cat['title']} products. Please send catalog.")
    return f"""{head_html(cat['title'])}
<div class="bg-brand text-white text-xs py-2 px-4 text-center">
  🚢 Trusted Factory Network · Global Shipping · MOQ Flexible
</div>
<nav class="bg-white shadow-sm sticky top-0 z-50">
  <div class="max-w-screen-xl mx-auto px-4 lg:px-8 flex items-center justify-between h-16">
    <a href="{root}index.html" class="flex items-center gap-2">
      <img src="{root}images/logo/logo.png" alt="{BRAND} Logo" class="h-9 w-auto"
           onerror="this.style.display='none';document.getElementById('lt').style.display='flex'"/>
      <div id="lt" class="hidden items-center gap-2">
        <div class="w-9 h-9 rounded-lg bg-brand flex items-center justify-center">{NAVBAR_LOGO_SVG}</div>
        <div class="leading-none">
          <div class="font-extrabold text-base text-brand">{BRAND}</div>
          <div class="text-[9px] text-gray-400 font-medium tracking-wide">{SLOGAN.upper()}</div>
        </div>
      </div>
    </a>
    <div class="hidden md:flex items-center gap-2 text-sm text-gray-500">
      <a href="{root}index.html" class="hover:text-brand">Home</a>
      <i class="fa-solid fa-chevron-right text-[10px]"></i>
      <span class="text-brand font-medium">{cat['title']}</span>
    </div>
    <a href="{root}index.html#contact" class="bg-brand text-white text-sm font-semibold px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">Send Inquiry</a>
  </div>
</nav>

<section class="bg-gradient-to-r {cat['color']} text-white py-14 px-4">
  <div class="max-w-screen-xl mx-auto text-center">
    <div class="w-16 h-16 rounded-2xl bg-white/20 flex items-center justify-center mx-auto mb-4">
      {render_icon(cat.get('icon'), cat.get('icon_type', 'fontawesome'), 'xl', '', root)}
    </div>
    <h1 class="text-4xl font-extrabold mb-3">{cat['title']}</h1>
    <p class="text-white/80 max-w-xl mx-auto text-sm">{cat['desc']}</p>
  </div>
</section>
<main class="max-w-screen-xl mx-auto px-4 lg:px-8 py-14">
  <div class="text-center mb-10">
    <span class="inline-block bg-accent text-brand text-xs font-semibold px-4 py-1.5 rounded-full mb-3 uppercase tracking-widest">Select a Sub-Category</span>
    <h2 class="text-2xl font-extrabold">Browse <span class="text-brand">{cat['title']}</span></h2>
    <div class="w-12 h-1 bg-brand rounded-full mx-auto mt-3"></div>
  </div>
  <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-5">
    {sub_cards}
  </div>
  <div class="mt-14 bg-accent rounded-2xl p-8 flex flex-col md:flex-row items-center justify-between gap-5">
    <div>
      <h3 class="font-bold text-lg mb-1">Looking for {cat['title']} at wholesale prices?</h3>
      <p class="text-gray-500 text-sm">Contact us now — we reply within 2 hours during business hours.</p>
    </div>
    <div class="flex gap-3 flex-shrink-0">
      <a href="https://wa.me/{WA}?text={wa_msg}" target="_blank"
         class="flex items-center gap-2 bg-[#25D366] text-white font-semibold px-5 py-2.5 rounded-xl text-sm hover:opacity-90">
        {WA_SVG_SM} WhatsApp Now
      </a>
      <a href="{root}index.html#contact" class="bg-brand text-white font-semibold px-5 py-2.5 rounded-xl text-sm hover:bg-blue-700 transition-colors">Send Inquiry</a>
    </div>
  </div>
</main>
{WA_FLOAT}
</body></html>"""

# ─────────────────────────────────────────────────────────────
# MAIN: generate all files
# ─────────────────────────────────────────────────────────────
generated = []

for cat in CATEGORIES:
    cat_dir = os.path.join(BASE, "products", cat["slug"])
    os.makedirs(cat_dir, exist_ok=True)

    # Category index page
    cat_index_path = os.path.join(cat_dir, "index.html")
    with open(cat_index_path, "w", encoding="utf-8") as f:
        f.write(cat_index_html(cat, "../../"))
    generated.append(f"products/{cat['slug']}/index.html")

    for sub in cat["subs"]:
        sub_dir = os.path.join(cat_dir, sub["slug"])
        os.makedirs(sub_dir, exist_ok=True)

        # Product dirs inside each sub
        for i, p in enumerate(sub["products"], 1):
            sku = f"{sub['sku_prefix']}{i:03d}"
            prod_dir = os.path.join(sub_dir, sku)
            os.makedirs(prod_dir, exist_ok=True)
            # placeholder README
            readme = os.path.join(prod_dir, "README.txt")
            with open(readme, "w", encoding="utf-8") as f:
                f.write(f"Product: {p['name']}\nSKU: {sku}\n\nImage files to add:\n  main.jpg       - Primary product photo (recommended: 800x800px)\n  detail1.jpg    - Front view\n  detail2.jpg    - Side/back view\n  detail3.jpg    - Packaging photo\n  detail4.jpg    - Size/detail shot\n  detail5.jpg    - In-use / lifestyle photo\n\nAll images will automatically appear in the product gallery on the website.\n")

        # Sub-category page (skip kitchenware - already created manually)
        if sub["slug"] == "kitchenware":
            # Regenerate it properly too
            pass
        sub_index_path = os.path.join(sub_dir, "index.html")
        with open(sub_index_path, "w", encoding="utf-8") as f:
            f.write(sub_page_html(cat, sub, "../../../"))
        generated.append(f"products/{cat['slug']}/{sub['slug']}/index.html")

# ─────────────────────────────────────────────────────────────
# Update index.html navigation with database data
# ─────────────────────────────────────────────────────────────
print("\n[OK] Updating index.html navigation...")

def update_index_navigation():
    """更新 index.html 的导航菜单"""
    index_path = os.path.join(BASE, "index.html")
    if not os.path.exists(index_path):
        print("  [SKIP] index.html not found")
        return False
    
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 生成桌面端导航菜单
    desktop_nav_items = []
    for cat in CATEGORIES:
        cat_link = f"products/{cat['slug']}/index.html"
        # 子分类链接
        sub_links = []
        for sub in cat["subs"]:
            sub_link = f"products/{cat['slug']}/{sub['slug']}/index.html"
            sub_icon = sub.get('icon', '')
            sub_icon_type = sub.get('icon_type', 'fontawesome')
            sub_icon_html = ''
            if sub_icon:
                # 检查是否是图片路径（包含 / 或 .jpg/.png/.svg 等扩展名）
                is_image_path = '/' in sub_icon or any(sub_icon.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.svg', '.gif', '.webp'])
                if is_image_path:
                    # 图片路径在静态页面中不可用，使用默认 FontAwesome 图标
                    sub_icon_html = f'<i class="fa-solid fa-tag mr-2 text-brand flex-shrink-0"></i>'
                elif sub_icon.startswith('fa-'):
                    sub_icon_html = f'<i class="fa-solid {sub_icon} mr-2 text-brand flex-shrink-0"></i>'
                else:
                    # 使用 FontAwesome 图标
                    icon_class = f'fa-{sub_icon}'
                    sub_icon_html = f'<i class="fa-solid {icon_class} mr-2 text-brand flex-shrink-0"></i>'
            else:
                # 默认使用小圆点
                sub_icon_html = f'<i class="fa-solid fa-circle text-[6px] mr-2 text-brand/60 flex-shrink-0"></i>'
            sub_links.append(f'<a href="{sub_link}">{sub_icon_html}{sub["title"]}</a>')
        
        # 生成分类图标HTML
        cat_icon = cat.get('icon', '')
        cat_icon_type = cat.get('icon_type', 'fontawesome')
        cat_icon_html = ''
        if cat_icon:
            # 检查是否是图片路径（包含 / 或 .jpg/.png/.svg 等扩展名）
            is_image_path = '/' in cat_icon or any(cat_icon.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.svg', '.gif', '.webp'])
            if is_image_path:
                # 图片路径在静态页面中不可用，使用默认 FontAwesome 图标
                cat_icon_html = f'<i class="fa-solid fa-box mr-1.5 text-brand flex-shrink-0"></i>'
            elif cat_icon.startswith('fa-'):
                cat_icon_html = f'<i class="fa-solid {cat_icon} mr-1.5 text-brand flex-shrink-0"></i>'
            else:
                # 使用 FontAwesome 图标
                icon_class = f'fa-{cat_icon}'
                cat_icon_html = f'<i class="fa-solid {icon_class} mr-1.5 text-brand flex-shrink-0"></i>'
        else:
            # 默认使用文件夹图标
            cat_icon_html = f'<i class="fa-solid fa-folder mr-1.5 text-brand flex-shrink-0"></i>'
        
        newline = "\n          "
        nav_item = f'''<li class="nav-item shrink-0">
        <a href="{cat_link}" class="flex items-center gap-1 px-2 xl:px-3 py-2 rounded-lg hover:bg-accent hover:text-brand transition-colors duration-150 text-body whitespace-nowrap">
          {cat_icon_html}<span class="whitespace-nowrap">{cat["title"]}</span>
          <i class="fa-solid fa-chevron-down text-[10px] opacity-60 ml-1 flex-shrink-0"></i>
        </a>
        <div class="dropdown-menu">
          {newline.join(sub_links)}
        </div>
      </li>'''
        desktop_nav_items.append(nav_item)
    
    desktop_nav_html = "\n      ".join(desktop_nav_items)
    
    # 生成移动端导航菜单
    mobile_nav_items = []
    for cat in CATEGORIES:
        cat_link = f"products/{cat['slug']}/index.html"
        
        # 生成分类图标HTML
        cat_icon = cat.get('icon', '')
        cat_icon_type = cat.get('icon_type', 'fontawesome')
        cat_icon_html = ''
        if cat_icon:
            # 检查是否是图片路径（包含 / 或 .jpg/.png/.svg 等扩展名）
            is_image_path = '/' in cat_icon or any(cat_icon.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.svg', '.gif', '.webp'])
            if is_image_path:
                # 图片路径在静态页面中不可用，使用默认 FontAwesome 图标
                cat_icon_html = f'<i class="fa-solid fa-box mr-2 text-brand flex-shrink-0"></i>'
            elif cat_icon.startswith('fa-'):
                cat_icon_html = f'<i class="fa-solid {cat_icon} mr-2 text-brand flex-shrink-0"></i>'
            else:
                icon_class = f'fa-{cat_icon}'
                cat_icon_html = f'<i class="fa-solid {icon_class} mr-2 text-brand flex-shrink-0"></i>'
        else:
            cat_icon_html = f'<i class="fa-solid fa-folder mr-2 text-brand flex-shrink-0"></i>'
        
        sub_links = []
        for sub in cat["subs"]:
            sub_link = f"products/{cat['slug']}/{sub['slug']}/index.html"
            sub_icon = sub.get('icon', '')
            sub_icon_type = sub.get('icon_type', 'fontawesome')
            sub_icon_html = ''
            if sub_icon:
                # 检查是否是图片路径
                is_image_path = '/' in sub_icon or any(sub_icon.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.svg', '.gif', '.webp'])
                if is_image_path:
                    # 图片路径在静态页面中不可用，使用默认 FontAwesome 图标
                    sub_icon_html = f'<i class="fa-solid fa-tag mr-2 text-brand flex-shrink-0"></i>'
                elif sub_icon.startswith('fa-'):
                    sub_icon_html = f'<i class="fa-solid {sub_icon} mr-2 text-brand flex-shrink-0"></i>'
                else:
                    icon_class = f'fa-{sub_icon}'
                    sub_icon_html = f'<i class="fa-solid {icon_class} mr-2 text-brand flex-shrink-0"></i>'
            else:
                sub_icon_html = f'<i class="fa-solid fa-circle text-[6px] mr-2 text-brand/60 flex-shrink-0"></i>'
            sub_links.append(f'<a href="{sub_link}" class="flex items-center py-1.5 text-sm text-gray-600 hover:text-brand">{sub_icon_html}{sub["title"]}</a>')
        
        newline = "\n          "
        mobile_item = f'''<div class="mobile-nav-group">
        <button class="mobile-toggle w-full flex justify-between items-center py-2.5 text-sm font-semibold text-body">
          <span class="flex items-center">{cat_icon_html}{cat["title"]}</span> <i class="fa-solid fa-chevron-down text-[10px] text-brand flex-shrink-0"></i>
        </button>
        <div class="mobile-sub pl-4 space-y-1 pb-2">
          {newline.join(sub_links)}
        </div>
      </div>'''
        mobile_nav_items.append(mobile_item)
    
    mobile_nav_html = "\n      ".join(mobile_nav_items)
    
    # 替换桌面端导航 (找到 <ul id="desktop-nav"> 和 </ul> 之间的内容)
    import re
    
    # 替换桌面导航 - 使用 id="desktop-nav" 作为标记（支持 justify-start 和 overflow-x-auto 新样式）
    desktop_pattern = r'(<ul class="hidden lg:flex flex-1 items-center justify-[^"]* gap-0 text-xs xl:gap-1 xl:text-sm font-medium min-w-0[^"]*" id="desktop-nav">)[\s\S]*?(</ul>)'
    desktop_replacement = f'\\1\n      {desktop_nav_html}\n    \\2'
    content_new = re.sub(desktop_pattern, desktop_replacement, content, count=1)
    
    # 替换移动端导航 - 使用 id="mobile-nav-items" 作为标记
    mobile_pattern = r'(<div class="space-y-1" id="mobile-nav-items">)[\s\S]*?(</div>\s*<div class="mt-4 pt-4 border-t border-gray-100 grid grid-cols-2 gap-3">)'
    mobile_replacement = f'\\1\n      {mobile_nav_html}\n    \\2'
    content_new = re.sub(mobile_pattern, mobile_replacement, content_new, count=1)
    
    # 更新页脚链接
    for cat in CATEGORIES:
        old_slug = cat['slug'].replace('home-daily-essentials', 'home-daily').replace('pet-daily-needs', 'pet-daily').replace('beauty-personal-care', 'beauty-care')
        new_slug = cat['slug']
        # 替换页脚中的链接
        content_new = content_new.replace(f'products/{old_slug}/index.html', f'products/{new_slug}/index.html')
    
    # 更新产品展示区域 - 从数据库读取产品数据
    print("  [OK] Updating product grid...")
    
    # 获取所有产品数据
    products_data = []
    for cat in CATEGORIES:
        cat_code = cat['slug'].split('-')[0]  # home, pet, beauty, craft, other
        for sub in cat['subs']:
            for prod in sub['products']:
                products_data.append({
                    'name': prod['name'],
                    'desc': prod['desc'],
                    'price': prod['price'],
                    'tags': prod['tags'],
                    'category': cat_code,
                    'cat_slug': cat['slug'],
                    'sub_slug': sub['slug'],
                    'image': prod.get('image'),  # 从数据库获取的图片文件名
                    'features': prod.get('features', []),  # 产品特性
                    'specifications': prod.get('specifications', {})  # 产品规格
                })
    
    # 排序：有实际图片的产品优先显示
    products_data.sort(key=lambda x: (x.get('image') == 'main.jpg' or x.get('image') is None, x['name']))
    
    # 生成产品卡片 HTML (最多显示8个)
    product_cards = []
    for i, prod in enumerate(products_data[:8]):
        # 根据标签确定 badge
        badge = ""
        if 'new' in prod['tags'].lower():
            badge = '<span class="badge-new absolute top-3 left-3 px-2 py-0.5 rounded font-semibold">NEW</span>'
        elif 'hot' in prod['tags'].lower():
            badge = '<span class="badge-hot absolute top-3 left-3 px-2 py-0.5 rounded font-semibold">HOT</span>'
        
        # 生成图片路径 - 优先使用数据库中的图片文件名
        if 'image' in prod and prod['image'] and prod['image'] != 'main.jpg':
            # 使用数据库中的图片文件名（如 product_25_f2d3aa1c.jpg）
            img_src = f"images/products/{prod['image']}"
        else:
            # 回退到默认路径
            img_src = f"images/products/{prod['cat_slug']}/{prod['sub_slug']}/main.jpg"
        
        # 生成特性和规格HTML
        features_html = ""
        if prod.get('features') and len(prod['features']) > 0:
            features_list = ', '.join(prod['features'][:3])  # 最多显示3个特性
            features_html = f'<p class="text-xs text-green-600 mb-1"><i class="fas fa-check mr-1"></i>{features_list}</p>'
        
        specs_html = ""
        if prod.get('specifications') and len(prod['specifications']) > 0:
            specs_items = list(prod['specifications'].items())[:2]  # 最多显示2个规格
            specs_list = ', '.join([f"{k}: {v}" for k, v in specs_items])
            specs_html = f'<p class="text-xs text-blue-600 mb-1">{specs_list}</p>'
        
        # 构建图库数据属性（用于弹窗显示多张图片）
        # 图库图片已同步为 detail1.jpg, detail2.jpg 等
        gallery_attr = ""
        if prod.get('gallery') and len(prod['gallery']) > 0:
            import json
            # 构建图库图片URL列表 (使用 products/{cat_slug}/{sub_slug}/{sku}/detailN.jpg 路径)
            gallery_urls = []
            for i in range(len(prod['gallery'])):
                gallery_urls.append(f"products/{prod['cat_slug']}/{prod['sub_slug']}/{sku}/detail{i+1}.jpg")
            gallery_attr = f" data-gallery='{json.dumps(gallery_urls)}'"
        
        card = f'''<!-- Product {i+1} -->
      <div class="product-card bg-white border border-gray-100 shadow-sm" data-cat="{prod['category']}"{gallery_attr} onclick="openProductModal(this)">
        <div class="img-wrap relative">
          <img src="{img_src}" alt="{prod['name']}" loading="lazy"
               onerror="this.src='https://placehold.co/400x300/F0F7FF/165DFF?text={prod['name'].replace(' ', '+')[:20]}'"/>
          {badge}
        </div>
        <div class="p-4">
          <h3 class="font-semibold text-body mb-1 truncate">{prod['name']}</h3>
          <p class="text-xs text-gray-500 mb-2 line-clamp-2">{prod['desc'][:60]}...</p>
          {features_html}
          {specs_html}
          <div class="flex items-center justify-between mt-2">
            <span class="text-brand font-bold text-sm">{prod['price']}</span>
            <span class="text-xs bg-brand text-white px-3 py-1.5 rounded-lg hover:bg-blue-700 transition-colors cursor-pointer">View</span>
          </div>
        </div>
      </div>'''
        product_cards.append(card)
    
    product_grid_html = "\n\n".join(product_cards)
    
    # 替换产品网格 - 匹配到 <!-- /product-grid --> 注释为止
    product_pattern = r'(<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5" id="product-grid">)[\s\S]*?(</div>\s*<!-- /product-grid -->)'
    product_replacement = f'\\1\n\n{product_grid_html}\n\n    \\2'
    content_new = re.sub(product_pattern, product_replacement, content_new, count=1)
    
    if content_new != content:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content_new)
        print("  [OK] index.html updated (navigation + products)")
        return True
    else:
        print("  [WARN] No changes made to index.html")
        return False

update_index_navigation()

print(f"\n[OK] Generated {len(generated)} pages:\n")
for p in generated:
    print(f"  {p}")
print("\n[OK] Product SKU folders with README.txt created for all products.")
print("Done!")
