import pandas as pd
import random
import datetime

# Define the path to the CSV file
csv_file = "data.csv"  

# Generate 25 random timestamps within a reasonable time range
def generate_random_timestamps(n=25):
    timestamps = []
    for _ in range(n):
        year = 2025
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Ensuring valid days in all months
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        timestamp = datetime.datetime(year, month, day, hour, minute, second)
        timestamps.append(timestamp)
    return timestamps

random_timestamps = generate_random_timestamps()

# Read the existing CSV file
df = pd.read_csv(csv_file)

# Ensure the DataFrame has at least 26 rows
while len(df) < 26:
    df = df._append(pd.Series(dtype='object'), ignore_index=True)

# Insert timestamps from row 2 to row 26
df.loc[1:25, "Timestamp"] = random_timestamps

# Save the updated DataFrame back to CSV
df.to_csv(csv_file, index=False)

print("Timestamps added successfully!")
