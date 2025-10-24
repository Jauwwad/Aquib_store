from flask import Flask, render_template, request, redirect, url_for
from models import db, Product
import cloudinary
import cloudinary.uploader
import os
import config

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Cloudinary setup
cloudinary.config(
    cloud_name=config.CLOUD_NAME,
    api_key=config.API_KEY,
    api_secret=config.API_SECRET
)

# ✅ Create tables when app starts (Flask 3.x compatible)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/admin')
def admin():
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    category = request.form['category']
    price = request.form['price']
    description = request.form['description']
    image = request.files['image']

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(image)
    image_url = upload_result['secure_url']

    product = Product(
        name=name,
        category=category,
        price=price,
        description=description,
        image_url=image_url
    )
    db.session.add(product)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.category = request.form['category']
        product.price = request.form['price']
        product.description = request.form['description']

        image = request.files.get('image')
        if image:
            upload_result = cloudinary.uploader.upload(image)
            product.image_url = upload_result['secure_url']

        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit.html', product=product)

if __name__ == '__main__':
    # Bind to host/port from environment for compatibility with platforms
    # like Render or Docker. Default to 0.0.0.0:5000 for local dev.
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    # Allow controlling debug via FLASK_DEBUG env (1 or 0)
    debug_env = os.environ.get('FLASK_DEBUG')
    if debug_env is not None:
        debug = debug_env in ('1', 'true', 'True')
    else:
        debug = True
    app.run(host=host, port=port, debug=debug)
