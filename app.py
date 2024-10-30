from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

class Order(db.Model):
    __tablename__ = 'orders'  # Explicitly setting the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    drink = db.Column(db.String(80), nullable=False)
    size = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    name = request.form['name']
    drink = request.form['drink']
    size = request.form['size']
    
    existing_order = Order.query.filter_by(name=name).first()
    if existing_order:
        return jsonify({'error': 'Order with this name already exists.'}), 400

    new_order = Order(name=name, drink=drink, size=size)
    db.session.add(new_order)
    db.session.commit()
    
    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    all_orders = Order.query.all()
    return render_template('orders.html', orders=all_orders)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the tables within the app context
    app.run(debug=True)