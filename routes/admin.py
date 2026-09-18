from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from models.models import db, User, Order, Payment, Wallpaper, WallpaperPack, Category, WebsiteSettings, UPISettings

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def dashboard():
    total_wallpapers = Wallpaper.query.count()
    total_packs = WallpaperPack.query.count()
    total_orders = Order.query.count()
    pending_payments = Order.query.filter_by(payment_status='Pending Verification').count()
    total_customers = User.query.filter_by(is_admin=False).count()
    
    # Compute total revenue from completed/paid orders
    paid_orders = Order.query.filter_by(payment_status='Paid').all()
    total_revenue = sum(order.total_amount for order in paid_orders)
    
    recent_orders = Order.query.order_by(Order.date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                           stats={
                               'total_wallpapers': total_wallpapers,
                               'total_packs': total_packs,
                               'total_orders': total_orders,
                               'pending_payments': pending_payments,
                               'total_customers': total_customers,
                               'total_revenue': total_revenue
                           },
                           recent_orders=recent_orders)

@admin.route('/payments')
@login_required
@admin_required
def payments():
    orders = Order.query.order_by(Order.date.desc()).all()
    return render_template('admin/payments.html', orders=orders)

@admin.route('/payments/verify/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def verify_payment(order_id):
    order = Order.query.get_or_404(order_id)
    order.payment_status = 'Paid'
    order.order_status = 'Completed'
    db.session.commit()
    flash(f'Payment for Order #{order.id} verified successfully.', 'success')
    return redirect(url_for('admin.payments'))

@admin.route('/payments/reject/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def reject_payment(order_id):
    order = Order.query.get_or_404(order_id)
    order.payment_status = 'Rejected'
    db.session.commit()
    flash(f'Payment for Order #{order.id} rejected.', 'success')
    return redirect(url_for('admin.payments'))

@admin.route('/wallpapers/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_wallpaper():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        price = float(request.form.get('price'))
        resolution = request.form.get('resolution')
        aspect_ratio = request.form.get('aspect_ratio')
        
        wallpaper_file = request.files.get('wallpaper_file')
        
        if wallpaper_file and wallpaper_file.filename != '':
            # Basic save (in a real app, use secure_filename and create unique names)
            from werkzeug.utils import secure_filename
            import os
            from flask import current_app
            
            filename = secure_filename(wallpaper_file.filename)
            file_path = os.path.join(current_app.config['WALLPAPER_FOLDER'], filename)
            wallpaper_file.save(file_path)
            
            new_wallpaper = Wallpaper(
                name=name,
                description=description,
                category_id=category_id,
                price=price,
                resolution=resolution,
                aspect_ratio=aspect_ratio,
                file_path=filename
            )
            
            db.session.add(new_wallpaper)
            db.session.commit()
            
            flash('Wallpaper added successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
            
    categories = Category.query.all()
    return render_template('admin/add_wallpaper.html', categories=categories)

@admin.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    web_settings = WebsiteSettings.query.first()
    upi_settings = UPISettings.query.first()
    
    if request.method == 'POST':
        web_settings.site_name = request.form.get('site_name')
        web_settings.hero_title = request.form.get('hero_title')
        
        upi_settings.upi_id = request.form.get('upi_id')
        upi_settings.upi_name = request.form.get('upi_name')
        
        qr_file = request.files.get('qr_code_image')
        if qr_file and qr_file.filename != '':
            from werkzeug.utils import secure_filename
            import os
            from flask import current_app
            filename = secure_filename(qr_file.filename)
            file_path = os.path.join(current_app.root_path, 'static', 'images', filename)
            qr_file.save(file_path)
            upi_settings.qr_code_image = filename
        
        db.session.commit()
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('admin.settings'))
        
    return render_template('admin/settings.html', web_settings=web_settings, upi_settings=upi_settings)
