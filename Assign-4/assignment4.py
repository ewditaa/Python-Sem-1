import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Task 1 — Data Acquisition & Loading


# Replace with your weather CSV file
file_path = "weather.csv"  

df = pd.read_csv(file_path)

print("\n--- HEAD ---")
print(df.head())

print("\n--- INFO ---")
print(df.info())

print("\n--- DESCRIBE ---")
print(df.describe(include="all"))


# Task 2 — Data Cleaning & Processing


# Convert date columns
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Drop rows where date couldn’t be parsed
df = df.dropna(subset=['date'])

# Fill missing values
df['temperature'] = df['temperature'].fillna(df['temperature'].mean())
df['rainfall'] = df['rainfall'].fillna(0)
df['humidity'] = df['humidity'].fillna(df['humidity'].median())

# Keep relevant columns
df = df[['date', 'temperature', 'rainfall', 'humidity']]


# Task 3 — NumPy Statistical Analysis


temps = df['temperature'].to_numpy()

print("\n--- Temperature Statistics ---")
print("Mean:", np.mean(temps))
print("Min:", np.min(temps))
print("Max:", np.max(temps))
print("Std Dev:", np.std(temps))

# Monthly stats
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

monthly_stats = df.groupby('month')['temperature'].agg(['mean', 'min', 'max', 'std'])
print("\n--- Monthly Stats ---")
print(monthly_stats)

yearly_stats = df.groupby('year')['temperature'].agg(['mean', 'min', 'max', 'std'])
print("\n--- Yearly Stats ---")
print(yearly_stats)


# Task 4 — Visualization (Matplotlib)


plt.figure(figsize=(12, 10))

# 1. Line chart — daily temperature
plt.subplot(2, 1, 1)
plt.plot(df['date'], df['temperature'])
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")

# 2. Combined figure: Rainfall + Scatter humidity vs temp
plt.subplot(2, 2, 3)
monthly_rainfall = df.groupby('month')['rainfall'].sum()
plt.bar(monthly_rainfall.index, monthly_rainfall.values)
plt.title("Monthly Rainfall")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")

plt.subplot(2, 2, 4)
plt.scatter(df['temperature'], df['humidity'])
plt.title("Humidity vs Temperature")
plt.xlabel("Temperature")
plt.ylabel("Humidity")

plt.tight_layout()
plt.show()


# Task 5 — Grouping & Aggregation


# Group by month
month_group = df.groupby('month').agg({
    'temperature': 'mean',
    'rainfall': 'sum',
    'humidity': 'mean'
})
print("\n--- Grouped by Month ---")
print(month_group)

# Seasonal grouping (DJF, MAM, JJA, SON)
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

df['season'] = df['month'].apply(get_season)

season_group = df.groupby('season').agg({
    'temperature': 'mean',
    'rainfall': 'sum',
    'humidity': 'mean'
})

print("\n--- Grouped by Season ---")
print(season_group)
