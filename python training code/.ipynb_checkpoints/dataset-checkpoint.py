import pandas as pd
import numpy as np
import random

# Define the number of records
num_records = 1000

# Generate synthetic data
data = {
    "BHK": np.random.randint(1, 6, num_records),  # BHK from 1 to 5
    "Build_Area": np.random.randint(500, 5000, num_records),  # Build area from 500 to 5000 sq ft
    "Total_Floors": np.random.randint(1, 20, num_records),  # Total floors in the building
    "Parking": np.random.choice(["Yes", "No"], num_records),  # Parking availability (Yes or No)
    "Furnishing": np.random.choice(["Furnished", "Semi-Furnished", "Unfurnished"], num_records),
    "Location": np.random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", 
                                  "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"], num_records),
}

# Create price based on features with some random variance
data["Price"] = (
    data["BHK"] * data["Build_Area"] * 150  # Price influenced by BHK and Build Area
    + data["Total_Floors"] * 1000  # More floors add some value
    + (np.array(data["Parking"]) == "Yes") * 5000  # Add value if parking is available
    + np.random.randint(-20000, 20000, num_records)  # Random variance
)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("synthetic_house_price_data_with_cities.csv", index=False)
print("Dataset saved as synthetic_house_price_data_with_cities.csv")
