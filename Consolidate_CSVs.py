import pandas as pd
import holidays
import paramiko
from datetime import datetime, timedelta
import os

hostname = "12345"
username = os.getenv("WINSCP_USERNAME")
password = os.getenv("WINSCP_PASSWORD")

if not username or not password:
    print("Username or password not set in environment variables.")
    exit()

# Login into SCP
try:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password)

    sftp_client = ssh_client.open_sftp()
except paramiko.SSHException as e:
    print(f"SSH connection error: {e}") 
    exit()

# Define the range of dates for the files that need processing
start_date = datetime(2021, 1, 18)
end_date = datetime(2024, 7, 20)

# Define the directory where the files are stored
remote_dir = '/directory_path/folder_of_interest/'

# Define US public holidays for 2024 and beyond
us_holidays = holidays.UnitedStates(years=[2024, 2025, 2026, 2027, 2028])  # Add more years as needed

# Create a list to store DataFrames
dataframes = []

# Loop over the date range
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    file_name = f"final_{date_str}.csv"
    remote_file_path = os.path.join(remote_dir, file_name)
    
    try:
        with sftp_client.file(remote_file_path, 'r') as remote_file:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(remote_file)
            # Update the 'Date' column to match the date from the file name
            df['Date'] = date_str
            # Add the 'HOLIDAY' column
            df['HOLIDAY'] = 1 if current_date in us_holidays else 0
            dataframes.append(df)
    except IOError:
        print(f"File {remote_file_path} does not exist.")
    
    # Move to the next day
    current_date += timedelta(days=1)

# Concatenate all DataFrames if any dataframes exist
if dataframes:
    combined_df = pd.concat(dataframes)
    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv('/path/to/combined_files.csv', index=False)
    print("All files have been consolidated into 'combined_files.csv'")
else:
    print("No files were found or processed.")

# Close the SFTP client
sftp_client.close()
ssh_client.close()
