from app import create_app
from models.models import db, User, Category, Wallpaper, WallpaperPack, PackItem, WebsiteSettings, UPISettings

app = create_app()

def init_db():
    with app.app_context():
        # Create tables without dropping them
        db.create_all()

        # Check if admin exists; if yes, do not re-initialize
        if User.query.filter_by(email='admin@example.com').first():
            print("Database already initialized.")
            return

        # Add admin
        admin = User(name='Admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Add a customer
        customer = User(name='Customer', email='customer@example.com', is_admin=False)
        customer.set_password('customer123')
        db.session.add(customer)

        # Settings
        db.session.add(WebsiteSettings())
        db.session.add(UPISettings())

        # Categories
        cat_nature = Category(name='Nature')
        cat_mountains = Category(name='Mountains')
        cat_cinematic = Category(name='Cinematic')
        db.session.add_all([cat_nature, cat_mountains, cat_cinematic])
        
        db.session.commit()
        
        print("Database initialized successfully with admin and settings. No dummy data added.")
        print("Admin: admin@example.com / admin123")

if __name__ == '__main__':
    init_db()
