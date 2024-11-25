CMSC 6950 Project: Stock Data Analysis
Overview
This project provides a comprehensive analysis of historical stock data for six major companies:

Microsoft (MSFT)
Dell (DELL)
IBM
Intel (INTC)
Sony (SONY)
Verizon (VZ)
The analysis covers various aspects of stock performance, including volatility, extreme value days, price trends, trading volume trends, and relationships between price changes and trading activity.

Features
Volatility Comparison:

Identifies the most and least volatile stocks based on standard deviations of closing prices.
Extreme Value Days:

Counts the number of days when stock prices were significantly above or below their historical mean.
Price Trends:

Visualizes the evolution of stock prices over time for each company.
Trading Volume Insights:

Compares average trading volumes to understand market activity.
Performance Comparison:

Computes the percentage growth or decline in stock prices during the analysis period.
Sensitivity Analysis:

Explores how extreme value counts change with varying thresholds for "extreme."
Best and Worst Daily Changes:

Identifies the most significant daily price swings for each company.
Price and Volume Relationships:

Analyzes the correlation between trading volume and price changes.
Usage
Prerequisites
Python 3.x
Required Python Libraries: pandas, matplotlib, numpy
Setup
Clone the repository:
bash
Copy code
git clone https://github.com/AnshumanTiwary35canada/CSMC_6950_project.git
Navigate to the project directory:
bash
Copy code
cd CSMC_6950_project
Install dependencies (optional if libraries are missing):
bash
Copy code
pip install pandas matplotlib numpy
Execution
Run the main analysis script to generate results:

bash
Copy code
python main_analysis.py
Project Structure
data/: Contains historical stock data for analysis.
scripts/: Python scripts for data cleaning, analysis, and visualization.
results/: Output files (charts, tables) generated during analysis.
README.md: Project documentation.
Key Results
Summary of Findings:
Volatile Stocks:
Dell and Intel exhibit higher price volatility.
Stable Performers:
Microsoft and IBM have more consistent performance over time.
Best and Worst Days:
Significant daily swings are observed in stocks like Dell and Intel.
Trading Insights:
Weak correlations between trading volume and price changes suggest additional factors influence stock behavior.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or suggestions, please reach out:

Author: Anshuman Tiwari
Email: ATiwari@mun.ca