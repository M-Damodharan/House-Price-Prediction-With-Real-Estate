import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Sample data parameters
num_samples = 100
locations = ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Erode', 'Hosur', 'Bangalore']
furnishing_types = ['Furnished', 'Semi-Furnished', 'Unfurnished']

# Generate synthetic data
data = {
    'BHK': np.random.randint(1, 6, size=num_samples),
    'Build_Area': np.random.randint(600, 2500, size=num_samples),
    'Total_Floors': np.random.randint(1, 21, size=num_samples),
    'Parking': np.random.choice(['Yes', 'No'], size=num_samples),
    'Furnishing': np.random.choice(furnishing_types, size=num_samples),
    'Location': np.random.choice(locations, size=num_samples),
}

# Create DataFrame
df = pd.DataFrame(data)

# Generate synthetic prices based on some logic
df['Price'] = df['BHK'] * 1000000 + df['Build_Area'] * 200 + np.random.randint(-500000, 500000, size=num_samples)

# Display the first few rows
print(df.head())

# Save to CSV
df.to_csv('house_price_data.csv', index=False)
