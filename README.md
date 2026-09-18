# Animated Nature Wallpapers

A complete, production-style full-stack e-commerce website for selling digital wallpapers, built with Python, Flask, and Vanilla HTML/CSS/JS.

## Features
- **Frontend**: Responsive, modern UI using Vanilla CSS with CSS Grid/Flexbox and glassmorphism.
- **Backend**: Flask RESTful structure with SQLAlchemy (SQLite).
- **Authentication**: Secure registration and login using Flask-Login and Werkzeug hashing.
- **Storefront**: Browse wallpapers and packs, filter by category.
- **Cart & Checkout**: LocalStorage-based cart system, integrating manual UPI checkout.
- **Order Management**: Customers can view orders and securely download high-res wallpapers after payment verification.
- **Admin Panel**: Separate admin login to manage website settings, UPI details, and verify/reject pending payments.

## Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python 3.11+, Flask 3
- **Database**: SQLite
- **Libraries**: Flask-SQLAlchemy, Flask-Login, Pillow

## Folder Structure
```
animated_nature_wallpapers/
├── app.py                  # Main Flask application
├── config.py               # Configuration and paths
├── init_db.py              # Script to initialize database and demo data
├── create_placeholder.py   # Script to generate placeholder preview image
├── requirements.txt        # Dependencies
├── instance/               # Contains SQLite DB
├── models/                 # SQLAlchemy DB models
├── routes/                 # Flask Blueprints (auth, customer, admin, payments)
├── static/                 # CSS, JS, and UI images
├── templates/              # HTML Templates (Jinja2)
└── uploads/                # Protected and public user content
```

## Installation & Setup

1. **Initialize the Virtual Environment**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

2. **Install Dependencies**
```powershell
pip install -r requirements.txt
```

3. **Initialize the Database and Create Demo Data**
```powershell
# Optional: Create a placeholder image for demo wallpapers
python create_placeholder.py

# Initialize DB
python init_db.py
```
*Note: `init_db.py` creates default demo wallpapers, a dummy pack, and default admin/customer accounts.*

4. **Run the Application**
```powershell
python app.py
```
Then open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Default Accounts
- **Admin**: `admin@example.com` / `admin123`
- **Customer**: `customer@example.com` / `customer123`
*(Change these in a real production environment!)*

## How Payment Verification Works
1. Customer adds wallpapers to the cart and proceeds to checkout.
2. Customer makes a payment to the displayed UPI ID/QR Code using their preferred app.
3. Customer enters the 12-digit UTR/Reference number on the checkout page and submits.
4. The order status becomes **Pending Verification**.
5. Admin logs into the Admin Panel (`/admin`), navigates to **Manage Payments**, and verifies the payment against their bank statement.
6. Upon clicking **Verify**, the order is marked as **Paid**.
7. The customer can now log into their account and securely download the high-resolution files.

## Adding Wallpapers & Changing Prices
Currently, you can manage the initial data by modifying `init_db.py` before running it, or you can implement the Admin Product Management CRUD forms inside the Admin Panel. The backend models and UI are prepared for this expansion.

To change UPI details, log in as admin and visit the **Settings** page.
