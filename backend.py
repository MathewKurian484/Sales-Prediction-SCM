from flask import Flask, request, jsonify
from catboost import CatBoostRegressor
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load the saved model
model = CatBoostRegressor()
model.load_model("catboost_model.cbm")

# Load the test dataset
test_data = pd.read_csv('data/Test.csv')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request
        data = request.get_json()
        index = data.get('index')

        # Validate index
        if index is None or index < 0 or index >= len(test_data):
            return jsonify({'error': 'Invalid index. Please enter a valid index.'}), 400

        # Get the row corresponding to the index
        input_data = test_data.iloc[[index]].copy()

        # Ensure categorical columns are of type 'category'
        categorical_columns = ['Item_Identifier', 'Item_Fat_Content', 'Item_Type', 
                               'Outlet_Identifier', 'Outlet_Size', 
                               'Outlet_Location_Type', 'Outlet_Type']
        for col in categorical_columns:
            if col in input_data.columns:
                input_data[col] = input_data[col].astype('category')

        # Make prediction
        prediction = model.predict(input_data)

        # Return the prediction as JSON
        return jsonify({'predicted_sales': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)