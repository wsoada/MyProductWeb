# SourceSure Product Structure

This website is organized for easy product replacement and future expansion.

## Brand information
- Brand: SourceSure
- Company: Yiwu Juncheng Co., Ltd.
- Slogan: One-Stop Sourcing Service in China
- WhatsApp: +86 18735731692
- Email: 18735731692@163.com

## Main entry pages
- `/index.html` -> homepage
- `/products/home-daily/index.html`
- `/products/pet-daily/index.html`
- `/products/beauty-care/index.html`
- `/products/craft-decor/index.html`
- `/products/other-supplies/index.html`

## Folder logic
Each sub-category has its own folder and its own `index.html`.
Each product inside that sub-category has its own SKU folder for images.

Example:

```text
products/
  home-daily/
    kitchenware/
      index.html
      KW001/
        main.jpg
        detail1.jpg
        detail2.jpg
        detail3.jpg
        detail4.jpg
        detail5.jpg
        README.txt
```

## Image naming rules
For every product folder, use:
- `main.jpg` -> main cover image
- `detail1.jpg` -> front/detail shot
- `detail2.jpg` -> side/back view
- `detail3.jpg` -> packaging image
- `detail4.jpg` -> close-up / materials
- `detail5.jpg` -> lifestyle / in-use image

The product pages will automatically use these files in the product popup gallery.

## Generated category coverage
### Home & Daily Essentials
- Kitchenware
- Bedding
- Bathroom Supplies
- Cleaning Products
- Storage Solutions

### Pet Daily Needs
- Food & Treats
- Grooming Tools
- Toys
- Beds & Furniture
- Health Care

### Beauty & Personal Care
- Skincare
- Haircare
- Makeup
- Bath & Body
- Fragrances

### Craft & Decor
- Home Decor
- DIY Supplies
- Art Materials
- Party Decorations
- Handicrafts

### Other Supplies
- Stationery
- Electronics Accessories
- Travel Gear
- Sports Equipment

## Notes
- All image paths are relative paths.
- If an image is missing, the page shows a placeholder automatically.
- WhatsApp icons across the site already link directly to chat.
- Replace `images/logo/logo.png` to update the brand logo globally.
