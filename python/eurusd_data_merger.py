import pandas as pd
import glob
import os

# -----------------------------
# 1️⃣ Set the path to your CSV files
# -----------------------------
# Change 'data/' to the folder where your CSV files are located
csv_path = 'data/*.csv'

# List all CSV files in the folder
csv_files = glob.glob(csv_path)
print(f"{len(csv_files)} files found:")
for f in csv_files:
    print(f)

# -----------------------------
# 2️⃣ Read and concatenate all CSV files
# -----------------------------
dfs = []

for f in csv_files:
    df = pd.read_csv(f)
    dfs.append(df)

# Concatenate all DataFrames into a single one
df_full = pd.concat(dfs, ignore_index=True)
print(f"\nCombined DataFrame created with {df_full.shape[0]} rows and {df_full.shape[1]} columns.")

# -----------------------------
# 3️⃣ Clean and convert date/time
# -----------------------------
# Adjust column names according to your CSV
print("Original columns:")
print(list(df_full.columns))

# Drop unnecessary columns
if 'Volume' in df_full.columns:
    df_full = df_full.drop(columns=['Volume'])

# Rename columns
df_full.columns = ["datetime", "open", "high", "low", "close"]

# Convert datetime column and sort
df_full["datetime"] = pd.to_datetime(df_full["datetime"])
df_full = df_full.sort_values("datetime").reset_index(drop=True)

print("Final columns:")
print(list(df_full.columns))

# -----------------------------
# 4️⃣ Save the cleaned 1-minute CSV
# -----------------------------
output_1m = 'EURUSD_1m_clean.csv'
df_full.to_csv(output_1m, index=False)
print(f"\n1-minute CSV saved as: {os.path.abspath(output_1m)}")

# -----------------------------
# 5️⃣ Generate and save the 2-minute candles CSV
# -----------------------------
# Set datetime as index for resampling
df_full.set_index("datetime", inplace=True)

# Resample to 2-minute candles
df_2m = df_full.resample("2T").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last"
}).dropna().reset_index()

output_2m = 'EURUSD_2m_clean.csv'
df_2m.to_csv(output_2m, index=False)
print(f"2-minute CSV saved as: {os.path.abspath(output_2m)}")
