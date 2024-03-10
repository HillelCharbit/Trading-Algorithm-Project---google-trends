import unittest
import pandas as pd
from strategies import BuyAndHoldStrategy, SellAndHoldStrategy
from backtesting import backtest, calc_realistic_price
import numpy as np
from models import ActionType

class Test_Backtesting(unittest.TestCase):
    def test_backtesting_long_bh(self):
        
        data = {
            'Open': [100 + i*10 for i in range(6)],
            'High': [100 + i*10 + 2 for i in range(6)],
            'Low': [100 + i*10 - 2 for i in range(6)],
            'Close': [100 + i*10 + 1 for i in range(6)],
            'Volume': [100000] * 6,
        }
        
        test_df = pd.DataFrame(data)
        b_df = backtest(test_df, BuyAndHoldStrategy(), starting_balance=100, slippage_factor=np.inf)
        
        # expected results
        expected_qty = [1.0, 1.0, 1.0, 1.0, 1.0, 0.0]
        expected_balance = [0.0, 0.0, 0.0, 0.0, 0.0, 150.0]
        expected_portfolio_value = [101.0, 111.0, 121.0, 131.0, 141.0, 150.0]
        
        # validate qty
        self.assertEqual(expected_qty, list(b_df.qty.values))
        
        # validate balance
        self.assertEqual(expected_balance, list(b_df.balance.values))
        
        # validate portfolio_value
        self.assertEqual(expected_portfolio_value, list(b_df.portfolio_value.values))
        
    def test_backtesting_short_sh(self):
        data = {
            'Open': [100 + i*10 for i in range(6)],
            'High': [100 + i*10 + 2 for i in range(6)],
            'Low': [100 + i*10 - 2 for i in range(6)],
            'Close': [100 + i*10 + 1 for i in range(6)],
            'Volume': [100000] * 6,
        }
        
        test_df = pd.DataFrame(data)
        b_df = backtest(test_df, SellAndHoldStrategy(), starting_balance=100, slippage_factor=np.inf)
        
        # expected results
        expected_qty = [-1.0, -1.0, -1.0, -1.0, -1.0, 0.0]
        expected_balance = [200.0, 200.0, 200.0, 200.0, 200.0, 50.0]
        expected_portfolio_value = [99.0, 89.0, 79.0, 69.0, 59.0, 50.0]
        
        # validate qty
        self.assertEqual(expected_qty, list(b_df.qty.values))
        
        # validate balance
        self.assertEqual(expected_balance, list(b_df.balance.values))
        
        # validate portfolio_value
        self.assertEqual(expected_portfolio_value, list(b_df.portfolio_value.values))

    def test_calculate_realistic_price(self):
        row = pd.Series({'Open': 100, 'Close': 90})
        
        # test buy price when price decrease
        action_type = ActionType.BUY
        result = calc_realistic_price(row, action_type, slippage_factor=5.0)
        self.assertEqual(result, 100)
        
        # test sell price when price decrease
        action_type = ActionType.SELL
        result = calc_realistic_price(row, action_type, slippage_factor=5.0)
        self.assertEqual(result, 98)
        
        row = pd.Series({'Open': 100, 'Close': 110})
        
        # test buy price when price increase
        action_type = ActionType.BUY
        result = calc_realistic_price(row, action_type, slippage_factor=5.0)
        self.assertEqual(result, 102)
        
        # test sell price when price increase
        action_type = ActionType.SELL
        result = calc_realistic_price(row, action_type, slippage_factor=5.0)
        self.assertEqual(result, 100)
        
if __name__ == '__main__':
    unittest.main()