from app import create_app
from models.models import db, User, Category, Wallpaper, WallpaperPack, PackItem, WebsiteSettings, UPISettings

app = create_app()

def init_db():
    with app.app_context():
        # Clean existing tables and recreate
        db.drop_all()
        db.create_all()

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

        # Wallpapers
        wallpapers = [
            Wallpaper(name='Misty Mountain', description='A beautiful misty mountain wallpaper.', category_id=cat_mountains.id, price=30.0, file_path='demo.jpg', tags='mountain,mist,nature'),
            Wallpaper(name='Rainy Forest', description='Dark moody forest in the rain.', category_id=cat_nature.id, price=30.0, file_path='demo.jpg', tags='forest,rain,dark'),
            Wallpaper(name='Golden Sunset', description='Cinematic golden hour sunset.', category_id=cat_cinematic.id, price=30.0, file_path='demo.jpg', tags='sunset,golden,cinematic'),
            Wallpaper(name='Ocean Waves', description='Crashing ocean waves from top view.', category_id=cat_nature.id, price=30.0, file_path='demo.jpg', tags='ocean,water,blue'),
            Wallpaper(name='Moonlit Mountains', description='Mountains under a bright full moon.', category_id=cat_mountains.id, price=30.0, file_path='demo.jpg', tags='moon,night,mountain'),
            Wallpaper(name='Cinematic Road', description='An empty road through a dark forest.', category_id=cat_cinematic.id, price=30.0, file_path='demo.jpg', tags='road,travel,dark'),
            Wallpaper(name='Green Valley', description='Lush green valley in spring.', category_id=cat_nature.id, price=30.0, file_path='demo.jpg', tags='green,valley,spring'),
            Wallpaper(name='Cloudy Peaks', description='High mountain peaks piercing clouds.', category_id=cat_mountains.id, price=30.0, file_path='demo.jpg', tags='clouds,peaks,high')
        ]
        db.session.add_all(wallpapers)
        db.session.commit()

        # Packs
        pack1 = WallpaperPack(name='Nature Starter Pack', description='A collection of 10 essential nature wallpapers.', price=150.0, num_wallpapers=10)
        pack2 = WallpaperPack(name='Cinematic Nature Pack', description='10 premium cinematic wallpapers.', price=150.0, num_wallpapers=10)
        db.session.add_all([pack1, pack2])
        db.session.commit()

        # Add items to packs (just dummy assignments for demo)
        db.session.add(PackItem(pack_id=pack1.id, wallpaper_id=wallpapers[0].id))
        db.session.add(PackItem(pack_id=pack1.id, wallpaper_id=wallpapers[1].id))
        db.session.add(PackItem(pack_id=pack2.id, wallpaper_id=wallpapers[2].id))
        db.session.add(PackItem(pack_id=pack2.id, wallpaper_id=wallpapers[3].id))
        
        db.session.commit()
        
        print("Database initialized successfully with demo data.")
        print("Admin: admin@example.com / admin123")
        print("Customer: customer@example.com / customer123")

if __name__ == '__main__':
    init_db()
