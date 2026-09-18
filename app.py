import os
from flask import Flask
from config import Config
from models import db, User, Category, Wallpaper, WallpaperPack, PackItem, Wishlist, Order, OrderItem, Payment, Review, WebsiteSettings, UPISettings
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Ensure upload folders exist
    os.makedirs(app.config['PREVIEW_FOLDER'], exist_ok=True)
    os.makedirs(app.config['WALLPAPER_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PACK_FOLDER'], exist_ok=True)
    os.makedirs(app.config['QR_FOLDER'], exist_ok=True)

    with app.app_context():
        from routes.auth import auth as auth_blueprint
        from routes.customer import customer as customer_blueprint
        from routes.payments import payments as payments_blueprint
        from routes.admin import admin as admin_blueprint
        
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(customer_blueprint)
        app.register_blueprint(payments_blueprint)
        app.register_blueprint(admin_blueprint)
        
        db.create_all()
        # Create default settings if they don't exist
        if not WebsiteSettings.query.first():
            db.session.add(WebsiteSettings())
        if not UPISettings.query.first():
            db.session.add(UPISettings())
        db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
