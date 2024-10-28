
# Google Trends as a Sentiment Indicator in Algorithmic Trading

## Project Description

This project explores the potential of using Google Trends data as a sentiment indicator to forecast price movements in the cryptocurrency market. By analyzing shifts in search volumes related to specific cryptocurrencies, the study aims to identify correlations between public interest and subsequent price changes, enabling more informed and profitable trading strategies.

---

## Table of Contents

1. [Data Sources](#data-sources)
2. [Methodology](#methodology)
   - [Data Collection and Cleaning](#data-collection-and-cleaning)
   - [Strategy Development](#strategy-development)
   - [Backtesting and Evaluation](#backtesting-and-evaluation)
3. [Results](#results)
4. [Conclusion](#conclusion)
5. [Future Improvements](#future-improvements)
6. [Sources and Related Content](#sources-and-related-content)

---

## Data Sources

- **Google Trends**: Provides search trend data over time for specific terms, which is used as a sentiment indicator.
- **Glimpse**: Chrome extension used to retrieve absolute search volumes for better accuracy in trend analysis.
- **Binance API**: Used to access historical cryptocurrency price data for strategy development and backtesting.

---

## Methodology

### Data Collection and Cleaning

1. **Google Trends Data**: Collected through the PyTrends API with adjustments for data normalization and resolution challenges. Glimpse was used to obtain absolute search volume data.
2. **Binance Data**: Historical price data for various cryptocurrencies was fetched using the Binance API, then cleaned and standardized for consistency, removing outliers and addressing any gaps.

### Strategy Development

1. **Trading Strategy**:
   - Significant increases in Google search volumes are used as buy signals, while significant decreases indicate potential sell signals.
   - The magnitude of these changes influences the quantity of cryptocurrency to be traded.

2. **Granger Causality Test**:
   - Conducted to statistically confirm a predictive relationship between Google Trends and cryptocurrency prices, determining optimal lag periods for each currency.

3. **Technical Indicators**:
   - **Bollinger Bands** and **Relative Strength Index (RSI)** are used to refine trading signals, reducing false positives and enhancing decision-making.

4. **Hyperparameter Optimization**:
   - A grid search was performed to optimize strategy parameters, aiming to maximize the Calmar Ratio and improve returns relative to risk.

### Backtesting and Evaluation

1. The dataset was divided into training and testing sets to ensure robust validation.
2. Strategy performance was assessed through backtesting, comparing it to a buy-and-hold benchmark strategy.
3. Key metrics for evaluation included:
   - **Annual Return**: Measures profitability over time.
   - **Sharpe Ratio**: Assesses return relative to risk.
   - **Max Drawdown**: Evaluates worst-case losses.
   - **Calmar Ratio**: Balances return against max drawdown.

---

## Results

- **Training Set**: The strategy outperformed the buy-and-hold benchmark, showing higher annual returns and a favorable Sharpe ratio.
- **Test Set**: Results indicated increased risk, with higher max drawdown values, suggesting a need for improved risk management to address volatility in the cryptocurrency market.

---

## Conclusion

This project provides evidence that Google Trends data can serve as a useful sentiment indicator for algorithmic trading in cryptocurrencies. However, due to the high volatility and susceptibility of the cryptocurrency market to external influences, the strategy requires enhanced risk management and continual refinement to achieve sustainable results.

---

## Future Improvements

1. **Real-Time Data Scraping**: Implement a live data collection system for more timely responses to market conditions.
2. **Reduced Analysis Window**: Decrease the time window to capture short-term fluctuations and increase trading responsiveness.
3. **Advanced Machine Learning Models**: Explore machine learning techniques for better pattern recognition and adaptability to market changes.
4. **Market Manipulation Mitigation**: Develop mechanisms to detect and adjust for potential market manipulation, enhancing model robustness.

---

## Sources and Related Content

- **Google Trends**: [Google Trends](https://trends.google.com)
- **Glimpse Extension**: [Glimpse Chrome Extension](https://chrome.google.com/webstore/detail/glimpse)
- **Binance API Documentation**: [Binance API](https://www.binance.com/en/binance-api)
