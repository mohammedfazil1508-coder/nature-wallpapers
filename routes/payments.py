import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, send_from_directory
from flask_login import login_required, current_user
from models.models import db, Order, OrderItem, Payment, Wallpaper, WallpaperPack, UPISettings

payments = Blueprint('payments', __name__)

@payments.route('/cart', methods=['GET'])
def cart():
    # Cart is currently managed mostly by JS on frontend (using localStorage)
    return render_template('cart.html')

@payments.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    upi_settings = UPISettings.query.first()
    
    if request.method == 'POST':
        # Assuming cart data is sent as JSON string in form
        cart_data_str = request.form.get('cart_data')
        total_amount = float(request.form.get('total_amount', 0))
        upi_reference = request.form.get('upi_reference')
        
        if not cart_data_str or total_amount <= 0:
            flash('Your cart is empty or invalid.', 'error')
            return redirect('/cart')
            
        if not upi_reference:
            flash('Please provide a UPI reference number.', 'error')
            return redirect('/checkout')
            
        try:
            cart_items = json.loads(cart_data_str)
            
            # Create Order
            order = Order(user_id=current_user.id, total_amount=total_amount)
            db.session.add(order)
            db.session.flush() # Get order ID
            
            # Create Order Items
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_type=item['type'],
                    product_id=item['id'],
                    price=item['price']
                )
                db.session.add(order_item)
                
            # Create Payment Record
            payment = Payment(order_id=order.id, upi_reference=upi_reference)
            db.session.add(payment)
            
            db.session.commit()
            
            return redirect(url_for('payments.order_success', order_id=order.id))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while processing your order.', 'error')
            print(f"Error: {str(e)}")
            return redirect('/checkout')
            
    return render_template('checkout.html', upi_settings=upi_settings)

@payments.route('/order-success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('order_success.html', order=order)

@payments.route('/account')
@login_required
def account():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date.desc()).all()
    for order in orders:
        for item in order.items:
            if item.product_type == 'single':
                w = Wallpaper.query.get(item.product_id)
                item.product_name = w.name if w else "Unknown Wallpaper"
            else:
                p = WallpaperPack.query.get(item.product_id)
                item.product_name = p.name if p else "Unknown Pack"
    return render_template('account.html', orders=orders)

@payments.route('/download/<int:order_id>/<int:product_id>')
@login_required
def download(order_id, product_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    if order.payment_status != 'Paid':
        flash('Payment has not been verified yet.', 'error')
        return redirect('/account')
        
    # Check if product is in order items
    order_item = OrderItem.query.filter_by(order_id=order.id, product_id=product_id, product_type='single').first()
    
    if order_item:
        wallpaper = Wallpaper.query.get_or_404(product_id)
        if wallpaper.file_path:
            return send_from_directory(current_app.config['WALLPAPER_FOLDER'], wallpaper.file_path, as_attachment=True)
            
    # Also handle downloading packs (could download a zip, or we just let them download individual ones for now)
    # For simplicity, if it's a pack, we might need a different route or return a zip. 
    # For this demo, we assume the user downloads individual items from the pack.
    
    flash('Invalid download request.', 'error')
    return redirect('/account')
