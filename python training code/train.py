import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
data = pd.read_csv("house_price_data.csv")

# Select features and target
X = pd.get_dummies(data[["BHK", "Build_Area", "Total_Floors", "Parking", "Furnishing", "Location"]])
y = data["Price"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model saved as model.pkl")

# Load the model
with open('model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

print("Model loaded from model.pkl")

# Make predictions with the loaded model
y_pred = loaded_model.predict(X_test)

# Output results
print("Predictions:", y_pred)

from joblib import dump, load

# Save the model
dump(model, 'model.joblib')

# Load the model
loaded_model = load('model.joblib')

