import pandas as pd
from pymongo import MongoClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_predictions_to_mongodb(csv_file, db_name, collection_name, mongo_uri="mongodb://localhost:27017/"):
    """
    Uploads predictions from a CSV file to a MongoDB collection.

    Args:
        csv_file (str): Path to the CSV file containing predictions.
        db_name (str): Name of the MongoDB database.
        collection_name (str): Name of the MongoDB collection.
        mongo_uri (str): MongoDB connection URI.
    """
    try:
        # Connect to MongoDB
        logging.info("Connecting to MongoDB...")
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # Load predictions from the CSV file
        logging.info(f"Loading predictions from '{csv_file}'...")
        predictions_df = pd.read_csv(csv_file)

        # Convert DataFrame to a list of dictionaries
        predictions_data = predictions_df.to_dict(orient="records")

        # Insert data into MongoDB
        logging.info(f"Inserting data into MongoDB collection '{collection_name}'...")
        result = collection.insert_many(predictions_data)

        # Log the result
        logging.info(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")
    except Exception as e:
        logging.error(f"Error occurred while uploading predictions to MongoDB: {str(e)}")

if __name__ == "__main__":
    # File path to the predictions CSV
    csv_file = "bigmart_sales_predictions_catboost.csv"

    # MongoDB database and collection details
    db_name = "bigmart_sales"
    collection_name = "predictions"

    # Call the function to upload predictions
    upload_predictions_to_mongodb(csv_file, db_name, collection_name)