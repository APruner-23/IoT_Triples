import pandas as pd
import random
import datetime

# Define the paths to the CSV files
csv_file = "data.csv"  # Existing file with timestamps
new_csv_file = "iot_data.csv"  # New file with IoT data

# Read the existing CSV file
df = pd.read_csv(csv_file)

# Extract exactly 25 timestamps from row 2 to row 26
iot_timestamps = df.iloc[:, df.columns.get_loc("Timestamp")].tolist()

# Generate 25 IoT data measurements
iot_data = {
    "Heartbeat (bpm)": [random.randint(60, 100) for _ in range(25)],
    "Steps": [random.randint(0, 10000) for _ in range(25)],
    "Temperature (°C)": [round(random.uniform(35.0, 40.0), 1) for _ in range(25)],
    "Humidity (%)": [round(random.uniform(30.0, 70.0), 1) for _ in range(25)],
    "Battery Level (%)": [random.randint(10, 100) for _ in range(25)],
    "Air Quality Index": [random.randint(0, 500) for _ in range(25)],
    "Timestamp": iot_timestamps
}

# Create a DataFrame and save it to the new CSV file
iot_df = pd.DataFrame(iot_data)
iot_df.to_csv(new_csv_file, index=False)

print("IoT data CSV file created successfully!")