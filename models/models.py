from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    orders = db.relationship('Order', backref='user', lazy=True)
    wishlist_items = db.relationship('Wishlist', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    wallpapers = db.relationship('Wallpaper', backref='category', lazy=True)

class Wallpaper(db.Model):
    __tablename__ = 'wallpapers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    price = db.Column(db.Float, nullable=False)
    resolution = db.Column(db.String(50), nullable=True)
    aspect_ratio = db.Column(db.String(20), nullable=True)
    preview_image = db.Column(db.String(255), nullable=True)
    file_path = db.Column(db.String(255), nullable=False) # Protected path
    tags = db.Column(db.String(255), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    reviews = db.relationship('Review', backref='wallpaper', lazy=True)

class WallpaperPack(db.Model):
    __tablename__ = 'wallpaper_packs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    preview_image = db.Column(db.String(255), nullable=True)
    num_wallpapers = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    pack_items = db.relationship('PackItem', backref='pack', lazy=True)

class PackItem(db.Model):
    __tablename__ = 'pack_items'
    id = db.Column(db.Integer, primary_key=True)
    pack_id = db.Column(db.Integer, db.ForeignKey('wallpaper_packs.id'), nullable=False)
    wallpaper_id = db.Column(db.Integer, db.ForeignKey('wallpapers.id'), nullable=False)

class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wallpaper_id = db.Column(db.Integer, db.ForeignKey('wallpapers.id'), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='Pending Verification') # Pending, Verified, Rejected
    order_status = db.Column(db.String(20), default='Pending') # Pending, Completed
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True)
    payment = db.relationship('Payment', backref='order', uselist=False, lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_type = db.Column(db.String(20), nullable=False) # 'single' or 'pack'
    product_id = db.Column(db.Integer, nullable=False) # Wallpaper ID or Pack ID
    price = db.Column(db.Float, nullable=False)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    upi_reference = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wallpaper_id = db.Column(db.Integer, db.ForeignKey('wallpapers.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # 1-5
    comment = db.Column(db.Text, nullable=True)
    is_published = db.Column(db.Boolean, default=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class WebsiteSettings(db.Model):
    __tablename__ = 'website_settings'
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default='Animated Nature Wallpapers')
    hero_title = db.Column(db.String(255), default='Bring Nature to Your Screen')
    hero_subtitle = db.Column(db.String(255), default='Premium cinematic wallpapers crafted for beautiful screens.')
    contact_email = db.Column(db.String(120), default='contact@example.com')
    about_text = db.Column(db.Text, nullable=True)

class UPISettings(db.Model):
    __tablename__ = 'upi_settings'
    id = db.Column(db.Integer, primary_key=True)
    upi_id = db.Column(db.String(100), default='yourupi@upi')
    upi_name = db.Column(db.String(100), default='Animated Nature Wallpapers')
    qr_code_image = db.Column(db.String(255), nullable=True)
    instructions = db.Column(db.Text, default='Scan the QR code or use the UPI ID to make the payment. Then enter the UTR/Reference number below.')
