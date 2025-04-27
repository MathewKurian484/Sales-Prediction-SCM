import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
import logging
from pymongo import MongoClient

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to handle missing values
def handle_missing_values(data, mode_of_outlet_size):
    data['Item_Weight'] = data['Item_Weight'].fillna(data['Item_Weight'].mean())
    miss_values = data['Outlet_Size'].isnull()
    data.loc[miss_values, 'Outlet_Size'] = data.loc[miss_values, 'Outlet_Type'].apply(
        lambda x: mode_of_outlet_size[x] if x in mode_of_outlet_size.columns else "Small"
    )
    return data

# Function to clean Item_Fat_Content
def clean_item_fat_content(data):
    return data.replace({'Item_Fat_Content': {'low fat': 'Low Fat', 'LF': 'Low Fat', 'reg': 'Regular'}})

# Load training data
logging.info("Loading training data...")
sales_data = pd.read_csv('data/Train.csv')

# Feature Engineering: Add Outlet_Age
sales_data['Outlet_Age'] = 2025 - sales_data['Outlet_Establishment_Year']

# Handle missing values in training data
logging.info("Handling missing values in training data...")
mode_of_outlet_size = sales_data.pivot_table(values='Outlet_Size', columns='Outlet_Type', aggfunc=(lambda x: x.mode()[0]))
sales_data = handle_missing_values(sales_data, mode_of_outlet_size)

# Clean Item_Fat_Content in training data
logging.info("Cleaning Item_Fat_Content in training data...")
sales_data = clean_item_fat_content(sales_data)

# Encode categorical variables
logging.info("Encoding categorical variables...")
categorical_columns = ['Item_Identifier', 'Item_Fat_Content', 'Item_Type', 'Outlet_Identifier', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']
for col in categorical_columns:
    sales_data[col] = sales_data[col].astype('category')

# Split features and target
X = sales_data.drop(columns='Item_Outlet_Sales', axis=1)
Y = sales_data['Item_Outlet_Sales']

# Split into training and testing data
logging.info("Splitting data into training and testing sets...")
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# Check if the model file exists
model_file = "catboost_model.cbm"
if os.path.exists(model_file):
    # Load the saved model
    logging.info("Loading the saved CatBoost model...")
    catboost_model = CatBoostRegressor()
    catboost_model.load_model(model_file)
else:
    # Train the model and save it
    logging.info("Training CatBoost model...")
    catboost_model = CatBoostRegressor(
        iterations=500,
        learning_rate=0.1,
        depth=6,
        cat_features=categorical_columns,
        verbose=100,
        random_seed=2
    )
    catboost_model.fit(X_train, Y_train)
    catboost_model.save_model(model_file)
    logging.info(f"Model saved as '{model_file}'")

# Evaluate the model
logging.info("Evaluating the model...")
train_predictions = catboost_model.predict(X_train)
test_predictions = catboost_model.predict(X_test)
logging.info(f"Training R-squared value: {metrics.r2_score(Y_train, train_predictions):.4f}")
logging.info(f"Test R-squared value: {metrics.r2_score(Y_test, test_predictions):.4f}")

# Load test data
logging.info("Loading test data...")
try:
    test_data = pd.read_csv('data/Test.csv')
    test_data['Outlet_Age'] = 2025 - test_data['Outlet_Establishment_Year']
    test_data_processed = test_data.copy()

    # Handle missing values in test data
    logging.info("Handling missing values in test data...")
    test_data_processed = handle_missing_values(test_data_processed, mode_of_outlet_size)

    # Clean Item_Fat_Content in test data
    logging.info("Cleaning Item_Fat_Content in test data...")
    test_data_processed = clean_item_fat_content(test_data_processed)

    # Encode categorical variables in test data
    logging.info("Encoding categorical variables in test data...")
    for col in categorical_columns:
        test_data_processed[col] = test_data_processed[col].astype('category')

    # Make predictions on test data
    logging.info("Making predictions on test data...")
    test_predictions_file = catboost_model.predict(test_data_processed)

    # Save predictions to CSV
    submission = pd.DataFrame({
        'Item_Identifier': test_data['Item_Identifier'],
        'Outlet_Identifier': test_data['Outlet_Identifier'],
        'Item_Outlet_Sales': test_predictions_file
    })
    submission.to_csv('bigmart_sales_predictions_catboost.csv', index=False)
    logging.info("Predictions saved to 'bigmart_sales_predictions_catboost.csv'")

    # MongoDB Integration
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
        db = client["bigmart_sales"]  # Replace with your database name
        collection = db["predictions"]  # Replace with your collection name

        # Load predictions from the CSV file
        predictions_df = pd.read_csv('bigmart_sales_predictions_catboost.csv')

        # Convert DataFrame to a list of dictionaries
        predictions_data = predictions_df.to_dict(orient="records")

        # Insert data into MongoDB
        result = collection.insert_many(predictions_data)

        # Log the result
        logging.info(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")
    except Exception as e:
        logging.error(f"Error occurred while uploading predictions to MongoDB: {str(e)}")

except Exception as e:
    logging.error(f"Error occurred while processing Test.csv: {str(e)}", exc_info=True)

# Allow user to input the index of a product to view its predicted and actual sales
try:
    user_index = int(input("\nEnter the index of a product in the test dataset to view its sales: "))
    if 0 <= user_index < len(Y_test):
        print(f"\nPredicted sales for product at index {user_index}: {test_predictions[user_index]:.2f}")
        print(f"Actual sales for product at index {user_index}: {Y_test.iloc[user_index]:.2f}")
    else:
        print("Invalid index. Please enter a number within the range of the test dataset.")
except ValueError:
    print("Invalid input. Please enter a valid integer.")