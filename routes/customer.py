from flask import Blueprint, render_template, request
from models.models import Wallpaper, WallpaperPack, Category, WebsiteSettings

customer = Blueprint('customer', __name__)

@customer.route('/')
def home():
    settings = WebsiteSettings.query.first()
    featured_wallpapers = Wallpaper.query.filter_by(is_featured=True, is_active=True).limit(6).all()
    categories = Category.query.filter_by(is_active=True).all()
    return render_template('home.html', settings=settings, wallpapers=featured_wallpapers, categories=categories)

@customer.route('/wallpapers')
def wallpapers():
    category_id = request.args.get('category')
    query = Wallpaper.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
        
    wallpapers = query.all()
    categories = Category.query.filter_by(is_active=True).all()
    return render_template('wallpapers.html', wallpapers=wallpapers, categories=categories)

@customer.route('/wallpaper/<int:id>')
def wallpaper_detail(id):
    wallpaper = Wallpaper.query.get_or_404(id)
    return render_template('wallpaper_detail.html', wallpaper=wallpaper)

@customer.route('/packs')
def packs():
    packs = WallpaperPack.query.filter_by(is_active=True).all()
    return render_template('packs.html', packs=packs)

@customer.route('/pack/<int:id>')
def pack_detail(id):
    pack = WallpaperPack.query.get_or_404(id)
    return render_template('pack_detail.html', pack=pack)

@customer.route('/about')
def about():
    settings = WebsiteSettings.query.first()
    return render_template('about.html', settings=settings)

@customer.route('/contact')
def contact():
    settings = WebsiteSettings.query.first()
    return render_template('contact.html', settings=settings)
