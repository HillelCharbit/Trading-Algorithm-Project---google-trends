from datetime import datetime
import pandas as pd
import requests

# Function to make an API call to Binance
def make_api_call(base_url, endpoint="", method="GET", **kwargs):
    # Construct the full URL
    full_url = f'{base_url}{endpoint}'

    # Make the API call
    response = requests.request(method=method, url=full_url, **kwargs)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response
    else:
        # If the request was not successful, raise an exception with the error message
        raise Exception(f'API request failed with status code {response.status_code}: {response.text}')

def get_binance_historical_data(symbol, interval, start_date, end_date=None):
    
    # define basic parameters for call
    base_url = 'https://fapi.binance.com'
    endpoint = '/fapi/v1/klines'
    method = 'GET'
    
    # Set the start time parameter in the params dictionary
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 1500,
        'startTime': start_date # Start time in milliseconds
    }
    
    # If end_date is provided, set it in the params dictionary
    if end_date:
        params['endTime'] = end_date

    # Make initial API call to get candles
    response = make_api_call(base_url, endpoint=endpoint, method=method, params=params)

    candles_data = []

    while len(response.json()) > 0:
        # Append the received candles to the list
        candles_data.extend(response.json())

        # Update the start time for the next API call
        params['startTime'] = candles_data[-1][0] + 1 # last candle open_time + 1ms
        
        # If end_date is provided and the last candle's open_time is greater than or equal to end_date, stop fetching data
        if end_date and candles_data[-1][0] >= end_date:
            break

        # Make the next API call
        response = make_api_call(base_url, endpoint=endpoint, method=method, params=params)

    
    # Wrap the candles data as a pandas DataFrame
    columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
               'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
    dtype={
    'open_time': 'datetime64[ms, Asia/Jerusalem]',
    'open': 'float64',
    'high': 'float64',
    'low': 'float64',
    'close': 'float64',
    'volume': 'float64',
    'close_time': 'datetime64[ms, Asia/Jerusalem]',
    'quote_asset_volume': 'float64',
    'number_of_trades': 'int64',
    'taker_buy_base_asset_volume': 'float64',
    'taker_buy_quote_asset_volume': 'float64',
    'ignore': 'float64'
    }
    
    df = pd.DataFrame(candles_data, columns=columns)
    df = df.astype(dtype)

    return df

# def TR(high, low, prev_close):
#     return max(high,prev_close) - min(low,prev_close)

# def ATR(tr, atr_length):
#     aapl_df['ATR'] = (np.maximum(aapl_df['High'], aapl_df['Close'].shift(1)) - np.minimum(aapl_df['Low'], aapl_df['Close'].shift(1))).rolling(n).mean()

#     atr = []
#     for i in range(0,atr_length):
#         atr[i]= data.apply(lambda row: TR(row['high'], row['low'], row['prev_close']), axis=1)
#     data['atr'] = data['tr'].rolling(window=atr_length).mean()
#     data['atr'] = data['atr'].fillna(method='bfill')  # Backfill to handle initial NA values
#     return data['atr']

# # def crossover(a,b):
# #     return curr_a > curr_b and prev_a < prev_b

# def UTBot(data, key_value, atr_length):
#     data['prev_close'] = data['close'].shift(1)
#     atr = ATR(data, atr_length)
#     data['loss_threshold'] = key_value * atr
    
#     data['trailing_stop'] = np.nan
#     for i in range(1, len(data)):
#         if data['close'][i] > data['close'][i-1]:  # Assuming upward trend for simplicity
#             data['trailing_stop'][i] = max(data['trailing_stop'][i-1], data['close'][i] - data['loss_threshold'][i])
#         else:  # Downward or stable trend
#             data['trailing_stop'][i] = data['close'][i] + data['loss_threshold'][i]

#     # Your buy/sell logic here based on crossover or other conditions

#     return data

# # STC Oscillator pseudo code

# def MacdDiff(close, fast_length, slow_length):
#     fast_ema = ema(close, fast_length)
#     slow_ema = ema(close, slow_length)
#     return fast_ema - slow_ema

# def SmoothSrs(srs, smoothing_f):
#     smoothed_srs = [0, …, 0] # init
#     smoothed_srs[0] = srs[0]

#     for i from 1 to num_rows:
#         if smoothed_srs[i-1] == Na:
#             smoothed_srs[i] = srs[i]
#         else:
#             smoothed_srs[i] = \
#                 smoothed_srs[i-1] + smoothing_f * (srs[i] - smoothed_srs[i-1])
#     return smoothed_srs

# def NormalizeSmoothSrs(series, window_length, smoothing_f):
#     lowest = rolling_min(series, window_length)
#     highest_range = rolling_max(series, window_length) – lowest

#     normalized_series = (element-wise)
#         if highest_range > 0:
#             normalized_value = (series - lowest) / highest_range * 100
#         else:
#             normalized_value = Na
#     Forward_fill(normalized_series)

#     smoothed_series = SmoothSrs(normalized_series, smoothing_f)
#     return smoothed_series

# def STC(close, stc_length, fast_length, slow_length, smoothing_factor=0.5):
#     macd_diff = MacdDiff(close, fast_length, slow_length)
#     normalized_macd = NormalizeSmoothSrs(macd_diff, stc_length, smoothing_factor)
#     final_stc = NormalizeSmoothSrs(normalized_macd, stc_length, smoothing_factor)
#     return final_stc

