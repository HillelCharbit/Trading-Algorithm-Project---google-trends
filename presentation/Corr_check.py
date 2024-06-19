import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the categories and their respective colors
general_stocks = ['KO', 'PFE', 'WMT', 'PG', 'JNJ', 'DIS']
tech_stocks = ['AAPL', 'AMZN', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META', 'INTC', 'IBM']
finance_stocks = ['GS', 'BAC', 'WFC', 'USB', 'JPM', 'MA']
decentralized_currencies = ['BTC', 'ETH', 'ADA', 'BNB', 'SOL', 'XRP', 'DOGE', 'XMR', 'LTC']

# Define a color mapping for each category
color_map = {
    'general': 'deepskyblue',
    'tech': 'limegreen',
    'finance': 'darkorchid',
    'crypto': 'red'
}

def trend_corr(stock, days=60):
    t = pd.read_csv(f"C:\\Users\\guygl\\OneDrive\\שולחן העבודה\\Algotrade\\semester 2\\{stock}_trends.csv")
    p = pd.read_csv(f"C:\\Users\\guygl\\OneDrive\\שולחן העבודה\\Algotrade\\semester 2\\{stock}_Prices.csv")

    t['Date'] = pd.to_datetime(t['Date'])
    p['Date'] = pd.to_datetime(p['Date'])

    full_data = pd.merge(p, t, on='Date')

    full_data['log_returns'] = np.log(full_data.Close / full_data.Close.shift(1))
    full_data['Volatility'] = full_data['log_returns'].rolling(window=days).std() * np.sqrt(days)

    full_data['Delay_1'] = full_data.Trend.shift(1)
    full_data['Delay_2'] = full_data.Trend.shift(2)
    full_data['Delay_3'] = full_data.Trend.shift(3)
    full_data['Delay_4'] = full_data.Trend.shift(4)
    full_data['Delay_5'] = full_data.Trend.shift(5)
    full_data['Delay_6'] = full_data.Trend.shift(6)
    full_data['Delay_7'] = full_data.Trend.shift(7)

    rho = full_data.corr()
    rho_c = rho['Close']['Delay_7']
    return rho_c, full_data

# Calculate correlations for each category
volt_del_corr_general = [trend_corr(stock)[0] for stock in general_stocks]
volt_del_corr_tech = [trend_corr(stock)[0] for stock in tech_stocks]
volt_del_corr_finance = [trend_corr(stock)[0] for stock in finance_stocks]
volt_del_corr_crypto = [trend_corr(crypto)[0] for crypto in decentralized_currencies]

# Combine the results
volt_del_corr = volt_del_corr_general + volt_del_corr_tech + volt_del_corr_finance + volt_del_corr_crypto

# Create labels for the scatter plot
labels = general_stocks + tech_stocks + finance_stocks + decentralized_currencies

# Plot the scatter plot
plt.figure(figsize=(16, 8))
plt.scatter(range(len(general_stocks)), volt_del_corr_general, color=color_map['general'], label='General Stocks')
plt.scatter(range(len(general_stocks), len(general_stocks) + len(tech_stocks)), volt_del_corr_tech, color=color_map['tech'], label='Tech Stocks')
plt.scatter(range(len(general_stocks) + len(tech_stocks), len(general_stocks) + len(tech_stocks) + len(finance_stocks)), volt_del_corr_finance, color=color_map['finance'], label='Finance Stocks')
plt.scatter(range(len(general_stocks) + len(tech_stocks) + len(finance_stocks), len(general_stocks) + len(tech_stocks) + len(finance_stocks) + len(decentralized_currencies)), volt_del_corr_crypto, color=color_map['crypto'], label='Decentralized Currencies')
plt.axhline(y=0, color='black', linestyle='--')  # Add a horizontal line at y=0
plt.xlabel('Assets')
plt.ylabel('Correlation with 7-Day Delayed Trend')
plt.title('Correlation of Close Price and 7-Day Delayed Trend')
plt.legend()
plt.xticks(range(len(labels)), labels, rotation=90)
plt.tight_layout(pad=2.0)
plt.show()

# Print the correlation values and their mean
print(volt_del_corr, np.mean(volt_del_corr))

# Function to plot Close price, 7-days delay trend
def plot_stock_data(stock, days=60):
    t = pd.read_csv(f"C:\\Users\\guygl\\OneDrive\\שולחן העבודה\\Algotrade\\semester 2\\{stock}_trends.csv")
    p = pd.read_csv(f"C:\\Users\\guygl\\OneDrive\\שולחן העבודה\\Algotrade\\semester 2\\{stock}_Prices.csv")

    t['Date'] = pd.to_datetime(t['Date'])
    p['Date'] = pd.to_datetime(p['Date'])

    full_data = pd.merge(p, t, on='Date')

    full_data['log_returns'] = np.log(full_data.Close / full_data.Close.shift(1))
    full_data['Volatility'] = full_data['log_returns'].rolling(window=days).std() * np.sqrt(days)

    full_data['Delay_7'] = full_data.Trend.shift(7)

    # Determine the color based on the stock category
    if stock in general_stocks:
        color = color_map['general']
    elif stock in tech_stocks:
        color = color_map['tech']
    elif stock in finance_stocks:
        color = color_map['finance']
    else:
        color = color_map['crypto']

    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Plot Close price
    axes[0].plot(full_data['Date'], full_data['Close'], label='Close Price', color=color)
    axes[0].set_xlabel('Date')
    axes[0].set_ylabel('Close Price')
    axes[0].set_title(f'{stock}: Close Price')
    axes[0].legend()

    # Plot 7-days delay trend
    axes[1].plot(full_data['Date'], full_data['Delay_7'], label='7-Days Delay Trend', color='black')
    axes[1].set_xlabel('Date')
    axes[1].set_ylabel('7-Days Delay Trend')
    axes[1].set_title(f'{stock}: 7-Days Delay Trend')
    axes[1].legend()

    plt.tight_layout(pad=3.0)
    plt.show()

# Plot for each stock and decentralized currency
for stock in general_stocks + tech_stocks + finance_stocks + decentralized_currencies:
    plot_stock_data(stock)

