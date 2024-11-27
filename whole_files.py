import pandas as pd
import matplotlib.pyplot as plt

# Load the data
files = {
    "DELL": "project_files/DELL_daily_data.csv",
    "IBM": "project_files/IBM_daily_data.csv",
    "INTC": "project_files/INTC_daily_data.csv",
    "MSFT": "project_files/MSFT_daily_data.csv",
    "SONY": "project_files/SONY_daily_data.csv",
    "VZ": "project_files/VZ_daily_data.csv",
}

dataframes = {company: pd.read_csv(filepath) for company, filepath in files.items()}
for company, df in dataframes.items():
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    dataframes[company] = df[['Date', 'Close', 'Volume']]

merged_data = dataframes["MSFT"].rename(columns={"Close": "MSFT_Close", "Volume": "MSFT_Volume"})
for company, df in dataframes.items():
    if company != "MSFT":
        merged_data = merged_data.merge(
            df.rename(columns={"Close": f"{company}_Close", "Volume": f"{company}_Volume"}), on="Date", how="inner"
        )
merged_data.dropna(inplace=True)

# 1. Volatility Comparison
volatility = merged_data.filter(like="_Close").std().rename(lambda x: x.replace("_Close", ""))
plt.figure(figsize=(10, 6))
volatility.sort_values(ascending=False).plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Stock Price Volatility (Standard Deviation of Closing Prices)')
plt.ylabel('Standard Deviation')
plt.xlabel('Company')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Extreme Value Days
closing_price_stats = merged_data.filter(like="_Close").describe().T
closing_price_stats = closing_price_stats[["mean", "std", "min", "max"]]
thresholds = closing_price_stats.apply(lambda row: (row["mean"] - 2 * row["std"], row["mean"] + 2 * row["std"]), axis=1)
extreme_value_days = {}
for company in closing_price_stats.index:
    lower, upper = thresholds.loc[company]
    extreme_value_days[company] = {
        "days_below_threshold": (merged_data[company] < lower).sum(),
        "days_above_threshold": (merged_data[company] > upper).sum(),
    }
pd.DataFrame(extreme_value_days).T.plot(kind="bar", figsize=(12, 8), title="Extreme Value Days")
plt.ylabel("Number of Days")
plt.show()

# 3. Price Trends
price_trends = merged_data.filter(like="_Close")
plt.figure(figsize=(10, 6))
for col in price_trends.columns:
    plt.plot(merged_data['Date'], price_trends[col], label=col.replace("_Close", ""))
plt.title('Stock Price Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()
plt.show()

# 4. Average Trading Volume
average_volume = merged_data.filter(like="_Volume").mean().rename(lambda x: x.replace("_Volume", ""))
average_volume.plot(kind='bar', figsize=(10, 6), title="Average Trading Volume by Company")
plt.ylabel("Average Volume")
plt.xlabel("Company")
plt.show()

# 5. Trading Volume Trends
volume_trends = merged_data.filter(like="_Volume")
plt.figure(figsize=(12, 8))
for col in volume_trends.columns:
    plt.plot(merged_data['Date'], volume_trends[col], label=col.replace("_Volume", ""))
plt.title('Trading Volume Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.legend()
plt.show()

# 6. Performance Comparison
performance_comparison = ((merged_data.filter(like="_Close").iloc[-1] - merged_data.filter(like="_Close").iloc[0])
                          / merged_data.filter(like="_Close").iloc[0]) * 100
performance_comparison.plot(kind="bar", figsize=(10, 6), title="Percentage Growth in Stock Prices")
plt.ylabel("Percentage Growth (%)")
plt.xlabel("Company")
plt.show()

# 7. Correlation Analysis
correlation = merged_data.filter(like="_Close").corr()
plt.figure(figsize=(8, 6))
plt.matshow(correlation, fignum=False)
plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45)
plt.yticks(range(len(correlation.columns)), correlation.columns)
plt.colorbar()
plt.title('Stock Price Correlation Matrix')
plt.show()

# 8. Sensitivity Analysis
threshold_multipliers = [1.5, 2.0, 2.5]
sensitivity = {}
for threshold in threshold_multipliers:
    sensitivity[threshold] = {}
    for company in closing_price_stats.index:
        mean = closing_price_stats.loc[company, "mean"]
        std_dev = closing_price_stats.loc[company, "std"]
        lower_threshold = mean - threshold * std_dev
        upper_threshold = mean + threshold * std_dev
        sensitivity[threshold][company] = {
            "days_below_threshold": (merged_data[company] < lower_threshold).sum(),
            "days_above_threshold": (merged_data[company] > upper_threshold).sum()
        }

sensitivity_long = []
for threshold, companies_data in sensitivity.items():
    for company, metrics in companies_data.items():
        sensitivity_long.append({
            "Threshold Multiplier": threshold,
            "Company": company.replace("_Close", ""),
            "Total Extreme Values": metrics["days_below_threshold"] + metrics["days_above_threshold"]
        })

sensitivity_long_df = pd.DataFrame(sensitivity_long)
plt.figure(figsize=(12, 8))
for company in sensitivity_long_df["Company"].unique():
    company_data = sensitivity_long_df[sensitivity_long_df["Company"] == company]
    plt.plot(company_data["Threshold Multiplier"], company_data["Total Extreme Values"], label=company)

plt.title("Sensitivity of Extreme Value Counts to Thresholds")
plt.xlabel("Threshold Multiplier")
plt.ylabel("Total Extreme Value Days")
plt.legend()
plt.show()

# 9. Best and Worst Daily Changes
daily_changes = merged_data.filter(like="_Close").pct_change() * 100
best_changes = daily_changes.max()
worst_changes = daily_changes.min()
best_worst_df = pd.DataFrame({
    "Best Change (%)": best_changes,
    "Worst Change (%)": worst_changes
}).rename_axis("Company").reset_index()
best_worst_df["Company"] = best_worst_df["Company"].str.replace("_Close", "")
print(best_worst_df)

# 10. Price and Volume Relationships
correlation_volume_price = {
    company.replace("_Close", ""): merged_data[f"{company}"].pct_change().corr(
        merged_data[f"{company.replace('_Close', '_Volume')}"]
    )
    for company in merged_data.filter(like="_Close").columns
}
correlation_df = pd.DataFrame.from_dict(correlation_volume_price, orient="index", columns=["Correlation"])
print(correlation_df)
