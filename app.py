from flask import Flask, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta  # Import datetime and timedelta

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.bigmart_sales
collection = db.predictions

@app.route('/')
def index():
    products = list(collection.find().limit(10))  # First 10 products
    return render_template('index.html', products=products)

@app.route('/product/<id>')
def product_detail(id):
    product = collection.find_one({'_id': ObjectId(id)})
    predicted_demand = 150  # Example hardcoded value for predicted demand
    return render_template(
        'product.html',
        product=product,
        now=datetime.now(),
        timedelta=timedelta,
        predicted_demand=predicted_demand
    )


if __name__ == '__main__':
    app.run(debug=True)