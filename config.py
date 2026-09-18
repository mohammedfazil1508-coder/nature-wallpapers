import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///wallpaper_store.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB max upload size

    PREVIEW_FOLDER = os.path.join(UPLOAD_FOLDER, 'previews')
    WALLPAPER_FOLDER = os.path.join(UPLOAD_FOLDER, 'wallpapers')
    PACK_FOLDER = os.path.join(UPLOAD_FOLDER, 'packs')
    QR_FOLDER = os.path.join(UPLOAD_FOLDER, 'qr')
