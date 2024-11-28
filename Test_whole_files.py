import pytest
import pandas as pd
import numpy as np
from whole_files import merged_data, volatility, closing_price_stats, performance_comparison, best_worst_df, correlation_df

def test_data_loading_and_merging():
    """Test if data is loaded and merged correctly."""
    assert not merged_data.empty, "Merged data should not be empty."
    assert "MSFT_Close" in merged_data.columns, "Merged data must contain 'MSFT_Close' column."
    assert len(merged_data["Date"].unique()) == len(merged_data), "Dates should not have duplicates."

def test_volatility_computation():
    """Test standard deviation (volatility) computation."""
    assert isinstance(volatility, pd.Series), "Volatility should be a Pandas Series."
    assert volatility["MSFT"] > 0, "Volatility for MSFT should be greater than 0."
    assert len(volatility) == 6, "Volatility should be calculated for 6 companies."

def test_closing_price_statistics():
    """Test descriptive statistics for closing prices."""
    assert not closing_price_stats.empty, "Closing price statistics should not be empty."
    assert "mean" in closing_price_stats.columns, "Statistics must include 'mean' column."
    assert "std" in closing_price_stats.columns, "Statistics must include 'std' column."
    assert closing_price_stats.loc["MSFT_Close", "std"] > 0, "MSFT standard deviation should be greater than 0."

def test_performance_comparison():
    """Test percentage growth calculation."""
    assert isinstance(performance_comparison, pd.Series), "Performance comparison should be a Pandas Series."
    assert "MSFT_Close" in performance_comparison.index, "Performance comparison should include MSFT_Close."
    assert performance_comparison["MSFT_Close"] != 0, "MSFT performance growth should not be 0."
    assert len(performance_comparison) == 6, "Performance comparison should be calculated for 6 companies."

def test_best_and_worst_changes():
    """Test best and worst daily changes."""
    assert not best_worst_df.empty, "Best/Worst daily changes DataFrame should not be empty."
    assert "Best Change (%)" in best_worst_df.columns, "DataFrame must include 'Best Change (%)'."
    assert "Worst Change (%)" in best_worst_df.columns, "DataFrame must include 'Worst Change (%)'."
    assert best_worst_df["Best Change (%)"].max() > 0, "There should be at least one positive best change."
    assert best_worst_df["Worst Change (%)"].min() < 0, "There should be at least one negative worst change."

def test_correlation_analysis():
    """Test stock price correlation analysis."""
    assert not correlation_df.empty, "Correlation DataFrame should not be empty."
    assert "Correlation" in correlation_df.columns, "Correlation DataFrame must include 'Correlation' column."
    assert (correlation_df["Correlation"] >= -1).all() and (correlation_df["Correlation"] <= 1).all(), \
        "All correlation values should be between -1 and 1."
