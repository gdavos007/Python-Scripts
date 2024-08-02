import pandas as pd
import holidays
from datetime import datetime, timedelta
import os

# Define the range of dates for the files that need processing
start_date = datetime(2024, 3, 18)
end_date = datetime(2024, 7, 16)

# Define the directory where the files are stored
local_dir = '/path/to/local-directory/'

# Define US public holidays for 2024 and beyond
us_holidays = holidays.UnitedStates(years=[2024, 2025, 2026, 2027, 2028])  # Add more years as needed

# Create a list to store DataFrames
dataframes = []

# Loop over the date range
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    file_name = f"file_{date_str}.csv"
    local_file_path = os.path.join(local_dir, file_name)
    
    try:
        if os.path.exists(local_file_path):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(local_file_path)
            # Update the 'Date' column to match the date from the file name
            df['Date'] = date_str
            # Add the 'HOLIDAY' column
            df['HOLIDAY'] = 1 if current_date in us_holidays else 0
            dataframes.append(df)
        else:
            print(f"File {local_file_path} does not exist.")
    except IOError:
        print(f"Error reading file {local_file_path}.")
    
    # Move to the next day
    current_date += timedelta(days=1)

# Concatenate all DataFrames if any dataframes exist
if dataframes:
    combined_df = pd.concat(dataframes)
    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv('/path/to/combined_file.csv', index=False)
    print("All files have been consolidated into 'combined_file.csv'")
else:
    print("No files were found or processed.")
