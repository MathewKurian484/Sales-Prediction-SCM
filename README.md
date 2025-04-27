# BigMart Sales Prediction System

A machine learning-based sales prediction system for BigMart retail stores, built with Python, CatBoost, and Flask.

## Overview

This project implements a sales prediction system that uses machine learning to forecast product sales in BigMart retail stores. The system processes historical sales data, trains a CatBoost regression model, and provides predictions through both a web interface and API endpoints.

## Features

- Sales prediction using CatBoost regression
- Web interface for viewing predictions
- MongoDB integration for data storage
- RESTful API endpoints
- Data preprocessing and feature engineering
- Model evaluation and performance metrics

## Prerequisites

- Python 3.x
- MongoDB
- Required Python packages:
  - pandas
  - numpy
  - scikit-learn
  - catboost
  - flask
  - pymongo
  - matplotlib
  - seaborn

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd bigmart_app
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Ensure MongoDB is running on your local machine or update the connection string in the code.

## Project Structure

- `main.py`: Core machine learning model training and prediction
- `app.py`: Flask web application
- `backend.py`: API endpoints
- `templates/`: HTML templates for the web interface
- `data/`: Training and test datasets
- `images/`: Visualization outputs
- `upload_to_mongodb.py`: Script for uploading data to MongoDB

## Usage

1. Train the model and generate predictions:
```bash
python main.py
```

2. Start the web application:
```bash
python app.py
```

3. Access the web interface at `http://localhost:5000`

## Model Details

The system uses a CatBoost regression model with the following features:
- Item characteristics (weight, fat content, type)
- Outlet information (size, location, type, age)
- Historical sales data

## API Endpoints

- `GET /`: Homepage with list of products
- `GET /product/<id>`: Detailed view of a specific product's predictions

## Data Storage

Predictions and product information are stored in MongoDB with the following structure:
- Database: bigmart_sales
- Collection: predictions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]

## Contact

[Add your contact information here] 