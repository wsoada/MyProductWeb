from __future__ import annotations

import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent

BRAND = "SourceSure"
COMPANY = "Yiwu Juncheng Co., Ltd."
SLOGAN = "One-Stop Sourcing Service in China"

PALETTES = {
    "default": ((22, 93, 255), (11, 32, 96), (240, 247, 255)),
    "home-daily": ((22, 93, 255), (53, 122, 255), (240, 247, 255)),
    "pet-daily": ((16, 185, 129), (13, 148, 136), (236, 253, 245)),
    "beauty-care": ((236, 72, 153), (168, 85, 247), (253, 242, 248)),
    "craft-decor": ((245, 158, 11), (249, 115, 22), (255, 247, 237)),
    "tech-gadget": ((51, 65, 85), (6, 182, 212), (236, 254, 255)),
}

DETAIL_LABELS = [
    ("main.jpg", "Main Visual"),
    ("detail1.jpg", "Front View"),
    ("detail2.jpg", "Side / Back"),
    ("detail3.jpg", "Packaging"),
    ("detail4.jpg", "Detail Shot"),
    ("detail5.jpg", "Lifestyle"),
]

SLIDES = [
    ("slide1.jpg", "China Sourcing. World Delivered.", "SourceSure global wholesale supply chain"),
    ("slide2.jpg", "Home & Daily Essentials", "Reliable products for everyday retail and wholesale"),
    ("slide3.jpg", "Beauty & Pet Collections", "OEM-ready product lines with flexible MOQ"),
    ("slide4.jpg", "Certified Quality. Competitive Pricing.", "One-stop sourcing support from China"),
]

FEATURED_PRODUCTS = [
    ("kitchen-set.jpg", "Kitchen Set", "Featured Product"),
    ("bedding-set.jpg", "Bedding Set", "Featured Product"),
    ("pet-grooming.jpg", "Pet Grooming", "Featured Product"),
    ("pet-bed.jpg", "Pet Bed", "Featured Product"),
    ("skincare-set.jpg", "Skincare Set", "Featured Product"),
    ("haircare.jpg", "Hair Care", "Featured Product"),
    ("home-decor.jpg", "Home Decor", "Featured Product"),
    ("travel-gear.jpg", "Travel Gear", "Featured Product"),
]

FACTORY_IMAGES = [
    ("factory-main.jpg", "Factory Overview", "Production Base"),
    ("production.jpg", "Production Line", "Workshop"),
    ("warehouse.jpg", "Warehouse", "Logistics Ready"),
]

CERT_IMAGES = [
    ("iso9001.jpg", "ISO 9001", "Quality Management"),
    ("ce.jpg", "CE", "EU Compliance"),
    ("rohs.jpg", "RoHS", "Hazardous Substance Control"),
    ("oeko-tex.jpg", "OEKO-TEX", "Textile Safety"),
    ("sgs.jpg", "SGS", "Third-Party Audit"),
]

FONT_CANDIDATES = [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
]


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = FONT_CANDIDATES[:]
    if bold:
        candidates = [FONT_CANDIDATES[0], FONT_CANDIDATES[2], FONT_CANDIDATES[1], FONT_CANDIDATES[3]]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def blend(color_a: tuple[int, int, int], color_b: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    return tuple(int(color_a[i] + (color_b[i] - color_a[i]) * ratio) for i in range(3))


def make_gradient(size: tuple[int, int], start: tuple[int, int, int], end: tuple[int, int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size)
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            ratio = (x / max(width - 1, 1) + y / max(height - 1, 1)) / 2
            pixels[x, y] = blend(start, end, ratio)
    return image


def draw_wrapped_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, x: int, y: int, max_width: int, fill: tuple[int, int, int], line_spacing: int = 8) -> int:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = word if not current else f"{current} {word}"
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    cursor_y = y
    for line in lines:
        draw.text((x, cursor_y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, cursor_y), line, font=font)
        cursor_y += (bbox[3] - bbox[1]) + line_spacing
    return cursor_y


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_image(path: Path, image: Image.Image) -> None:
    ensure_parent(path)
    image.save(path, format="JPEG", quality=92, optimize=True)


def add_badge(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, bg: tuple[int, int, int], fg: tuple[int, int, int]) -> None:
    font = get_font(26, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0] + 34
    height = bbox[3] - bbox[1] + 18
    draw.rounded_rectangle((x, y, x + width, y + height), radius=18, fill=bg)
    draw.text((x + 17, y + 8), text, font=font, fill=fg)


def build_visual(size: tuple[int, int], title: str, subtitle: str, palette_key: str, label: str, overlay_style: str = "card") -> Image.Image:
    primary, secondary, light = PALETTES.get(palette_key, PALETTES["default"])
    image = make_gradient(size, secondary, primary)
    draw = ImageDraw.Draw(image)
    width, height = size

    wave_fill = (*light, 120)
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.ellipse((width * 0.58, -height * 0.08, width * 1.03, height * 0.42), fill=(255, 255, 255, 32))
    odraw.ellipse((-width * 0.15, height * 0.62, width * 0.38, height * 1.08), fill=(255, 255, 255, 22))
    odraw.polygon(
        [
            (0, height * 0.82),
            (width * 0.18, height * 0.75),
            (width * 0.4, height * 0.84),
            (width * 0.62, height * 0.77),
            (width * 0.82, height * 0.84),
            (width, height * 0.8),
            (width, height),
            (0, height),
        ],
        fill=(255, 255, 255, 28),
    )
    odraw.line((width * 0.06, height * 0.2, width * 0.42, height * 0.2), fill=wave_fill, width=4)
    odraw.line((width * 0.08, height * 0.24, width * 0.36, height * 0.24), fill=wave_fill, width=4)
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(image)

    if overlay_style == "card":
        panel = (int(width * 0.08), int(height * 0.16), int(width * 0.78), int(height * 0.78))
        draw.rounded_rectangle(panel, radius=34, fill=(255, 255, 255), outline=(255, 255, 255), width=0)
        add_badge(draw, label, panel[0] + 28, panel[1] + 26, primary, (255, 255, 255))
        end_y = draw_wrapped_text(draw, title, get_font(max(40, width // 22), bold=True), panel[0] + 30, panel[1] + 92, panel[2] - panel[0] - 60, (23, 23, 23), line_spacing=10)
        draw_wrapped_text(draw, subtitle, get_font(max(22, width // 44)), panel[0] + 30, end_y + 6, panel[2] - panel[0] - 60, (95, 99, 104), line_spacing=8)
        draw.text((panel[0] + 30, panel[3] - 44), f"{BRAND} · {SLOGAN}", font=get_font(max(18, width // 60), bold=True), fill=primary)
    elif overlay_style == "certificate":
        border = 24
        draw.rounded_rectangle((border, border, width - border, height - border), radius=22, fill=(250, 250, 252), outline=primary, width=8)
        draw.rounded_rectangle((border + 18, border + 18, width - border - 18, height - border - 18), radius=18, outline=secondary, width=3)
        draw.text((width // 2 - 140, 42), COMPANY, font=get_font(18, bold=True), fill=secondary)
        title_font = get_font(48, bold=True)
        title_box = draw.textbbox((0, 0), title, font=title_font)
        draw.text(((width - (title_box[2] - title_box[0])) / 2, 112), title, font=title_font, fill=primary)
        draw_wrapped_text(draw, subtitle, get_font(22), 70, 190, width - 140, (90, 94, 101), line_spacing=6)
        draw.text((74, height - 88), BRAND, font=get_font(28, bold=True), fill=primary)
        draw.line((width - 210, height - 84, width - 80, height - 84), fill=secondary, width=4)
        draw.text((width - 206, height - 72), "Authorized Signature", font=get_font(14), fill=(90, 94, 101))
    else:
        add_badge(draw, label, 54, 42, light, primary)
        end_y = draw_wrapped_text(draw, title, get_font(max(52, width // 18), bold=True), 56, 126, int(width * 0.68), (255, 255, 255), line_spacing=10)
        draw_wrapped_text(draw, subtitle, get_font(max(22, width // 45)), 56, end_y + 10, int(width * 0.62), (232, 240, 254), line_spacing=8)
        draw.text((56, height - 78), f"{BRAND} · {SLOGAN}", font=get_font(max(18, width // 62), bold=True), fill=(255, 255, 255))

    return image


def create_if_missing(path: Path, size: tuple[int, int], title: str, subtitle: str, palette_key: str, label: str, overlay_style: str = "card") -> bool:
    if path.exists():
        return False
    image = build_visual(size=size, title=title, subtitle=subtitle, palette_key=palette_key, label=label, overlay_style=overlay_style)
    save_image(path, image)
    return True


def copy_logo_if_needed() -> int:
    src = ROOT / "logo" / "logo.png"
    dst = ROOT / "images" / "logo" / "logo.png"
    if src.exists() and not dst.exists():
        ensure_parent(dst)
        shutil.copy2(src, dst)
        return 1
    return 0


def generate_global_assets() -> dict[str, int]:
    created = {"logo": copy_logo_if_needed(), "slides": 0, "featured": 0, "factory": 0, "certs": 0}

    for filename, title, subtitle in SLIDES:
        path = ROOT / "images" / "slides" / filename
        if create_if_missing(path, (1600, 900), title, subtitle, "default", "SourceSure", overlay_style="hero"):
            created["slides"] += 1

    featured_palette_cycle = ["home-daily", "home-daily", "pet-daily", "pet-daily", "beauty-care", "beauty-care", "craft-decor", "tech-gadget"]
    for (filename, title, subtitle), palette_key in zip(FEATURED_PRODUCTS, featured_palette_cycle):
        path = ROOT / "images" / "products" / filename
        if create_if_missing(path, (1200, 900), title, subtitle, palette_key, "Featured"):
            created["featured"] += 1

    for filename, title, subtitle in FACTORY_IMAGES:
        path = ROOT / "images" / "factory" / filename
        if create_if_missing(path, (1400, 900), title, subtitle, "default", "Factory"):
            created["factory"] += 1

    for filename, title, subtitle in CERT_IMAGES:
        path = ROOT / "images" / "certs" / filename
        if create_if_missing(path, (900, 1200), title, subtitle, "default", "Certificate", overlay_style="certificate"):
            created["certs"] += 1

    return created


def extract_product_name(readme_path: Path) -> str:
    try:
        first_line = readme_path.read_text(encoding="utf-8").splitlines()[0].strip()
    except (OSError, IndexError):
        return readme_path.parent.name
    if first_line.lower().startswith("product:"):
        return first_line.split(":", 1)[1].strip()
    return readme_path.parent.name


def generate_sku_assets() -> int:
    count = 0
    for readme in ROOT.glob("products/*/*/*/README.txt"):
        sku_dir = readme.parent
        parts = sku_dir.relative_to(ROOT).parts
        big_category = parts[1] if len(parts) > 1 else "default"
        product_name = extract_product_name(readme)
        sku = sku_dir.name

        for filename, label in DETAIL_LABELS:
            target = sku_dir / filename
            if target.exists():
                continue
            subtitle = f"{product_name} · {label}"
            if create_if_missing(target, (1000, 1000), sku, subtitle, big_category, label):
                count += 1
    return count


def main() -> None:
    global_counts = generate_global_assets()
    sku_count = generate_sku_assets()

    print("[DONE] Placeholder assets generated.")
    print(f"logo copied: {global_counts['logo']}")
    print(f"slides created: {global_counts['slides']}")
    print(f"featured product images created: {global_counts['featured']}")
    print(f"factory images created: {global_counts['factory']}")
    print(f"certificate images created: {global_counts['certs']}")
    print(f"SKU image files created: {sku_count}")


if __name__ == "__main__":
    main()
