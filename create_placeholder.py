from PIL import Image, ImageDraw
import os

def create_placeholder(path, color, text):
    img = Image.new('RGB', (800, 600), color=color)
    d = ImageDraw.Draw(img)
    d.text((10,10), text, fill=(255,255,255))
    img.save(path)

uploads_dir = 'uploads'
wallpapers_dir = os.path.join(uploads_dir, 'wallpapers')
os.makedirs(wallpapers_dir, exist_ok=True)
create_placeholder(os.path.join(wallpapers_dir, 'demo.jpg'), (73, 109, 137), 'Demo Wallpaper')
print("Created demo.jpg")
