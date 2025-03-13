import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# The import must be done after db initialization due to circular import issue
from models import Products

@app.route('/', methods=['GET'])
def index():
    show_products = request.args.get('show_products', 'false') == 'true'
    print('Request for index page received')
    products = Products.query.all() if show_products else []
    return render_template('index.html', products=products, show_products=show_products)

# @app.route('/<int:id>', methods=['GET'])
# def details(id):
#     product = Products.query.where(Products.id == id).first()
#     return render_template('details.html', product=product)

# @app.route('/create', methods=['GET'])
# def create_restaurant():
#     print('Request for add restaurant page received')
#     return render_template('create_restaurant.html')

@app.route('/product/new', methods=['GET', 'POST'])
@csrf.exempt
def new_product():
    if request.method == 'POST':
        product = Products(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price'])
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_product.html')

# @app.route('/product/<int:id>/edit', methods=['GET', 'POST'])
# @csrf.exempt
# def edit_product(id):
#     product = Products.query.get_or_404(id)
#     if request.method == 'POST':
#         product.name = request.form['name']
#         product.description = request.form['description']
#         product.price = float(request.form['price'])
#         db.session.commit()
#         return redirect(url_for('index'))
#     return render_template('edit_product.html', product=product)

@app.route('/product/<int:id>/delete', methods=['POST'])
@csrf.exempt
def delete_product(id):
    product = Products.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))
    
# @app.route('/add', methods=['POST'])
# @csrf.exempt
# def add_restaurant():
#     try:
#         name = request.values.get('products_name')
#         price = request.values.get('price')

#     except (KeyError):
#         # Redisplay the question voting form.
#         return render_template('add_restaurant.html', {
#             'error_message': "You must include a restaurant name, address, and description",
#         })
#     else:
#         product = Products()
#         product.name = name
#         product.price = price
#         db.session.add(product)
#         db.session.commit()

#         return redirect(url_for('details', id=product.id))

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()
