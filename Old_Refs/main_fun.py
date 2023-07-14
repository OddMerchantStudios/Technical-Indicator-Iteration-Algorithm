# Define a class
class SignalIterator:
    
    def __init__(self, ticker, interval, stocks_df, share_size = 100, initial_cash = 10000):
        
        if interval == '5m':
            self.sqrt_val = 252 * 78 
        elif interval == '15m':
            self.sqrt_val = 252 * 26  
        elif interval == '30m':
            self.sqrt_val = 252 * 13 
        elif interval == '1h':
            self.sqrt_val = 252 * 6.5
        elif interval == '1d':
            self.sqrt_val = 252
            
        print(self.sqrt_val)
            
        self.stocks_df = stocks_df
        self.interval = interval
        self.ticker = ticker
        self.share_size = share_size
        self.initial_cash = initial_cash
        
        # Call the basic methods in the __init__ constructor to be immediately executed
        
        self.get_individual_stock()
        self.indicators()
        self.signals()

    def get_individual_stock(self):
        mask = self.stocks_df.columns.get_level_values(1) == self.ticker
        self.df = self.stocks_df.loc[:, mask]
        self.df.columns = self.df.columns.droplevel(1)
        self.df.dropna(inplace = True, axis = 0)
        
    def indicators(self):
        
        # EMA
        self.df['EMA_10'] = TA.EMA(self.df, 10)
        
        # EMA
        self.df['EMA_20'] = TA.EMA(self.df, 20)
        
         # EMA
        self.df['EMA_50'] = TA.EMA(self.df, 50)
        
        # BBANDS
        self.df[['BB_UPPER','BB_MIDDLE','BB_LOWER']] = TA.BBANDS(self.df, std_multiplier= 3)
        
        # SQZ setup
        self.df['SQZ'] = TA.SQZMI(self.df)
        
        # ADX
        self.df['ADX'] = TA.ADX(self.df)
        
        # MACD
        self.df[['MACD', 'SIGNAL']] = TA.MACD(self.df)
        
        # CHAIKIN
        self.df['CHAIKIN'] = TA.CHAIKIN(self.df)
        
        # MFI
        self.df['MFI'] = TA.MFI(self.df)
   
    def signals(self):
        
        ### BUY SIGNALS ###
        
        # EMA Signal logic
        self.df['EMA20_Signal'] = 0.0
        self.df['EMA20_Signal'] = np.where((self.df['Close'] > self.df['EMA_20']), 1.0, 0.0)
        
        # EMA Signal logic
        self.df['EMA50_Signal'] = 0.0
        self.df['EMA50_Signal'] = np.where((self.df['Close'] > self.df['EMA_50']), 1.0, 0.0)
        
        # SQZ Signal logic
        self.df['SQZ_Signal'] = 0.0
        self.df['SQZ_Signal'] = np.where(self.df['SQZ'] == False, 1.0, 0.0)
        
        # ADX Signal logic
        self.df['ADX_Signal'] = 0.0
        self.df['ADX_Signal'] = np.where(self.df['ADX'] > 30, 1.0, 0.0)
        
        # MACD Signal logic
        self.df['MACD_Signal'] = 0.0
        self.df['MACD_Signal'] = np.where(self.df['MACD'] > self.df['SIGNAL'], 1.0, 0.0)        
        
        # CHAIKIN Signal logic
        self.df['CHAIKIN_Signal'] = 0.0
        self.df['CHAIKIN_Signal'] = np.where(self.df['CHAIKIN'] > 0, 1.0, 0.0)        
        
        # MFI Signal logic
        self.df['MFI_Signal'] = 0.0
        self.df['MFI_Signal'] = np.where(self.df['MFI'] < 20, 1.0, 0.0)    
        
        ### SELL SIGNALS ###
        
        # BBANDS Sell Signal Logic
        self.df['BB_Sell_Signal'] = 0.0
        self.df['BB_Sell_Signal'] = np.where((self.df['Close'] > self.df['BB_UPPER']), 0.0, 1.0)        
        
    def result(self):
        
        # Define eval df columns
        columns = ['Buy Signals', 'Sell Signals', 'Annualized Return', 'Cumulative Return', 'Annual Volatility', 'Sharpe Ratio']
        eval_df = pd.DataFrame( columns= columns)
        # Define the signal column names
        buy_signal_columns = ['EMA50_Signal','EMA20_Signal','MACD_Signal','SQZ_Signal','ADX_Signal','CHAIKIN_Signal','MFI_Signal']
        sell_signal_columns = ['BB_Sell_Signal','EMA20_Signal', 'MACD_Signal','ADX_Signal']
        
        # Generate all combinations of signal columns
        for r_buy in range(1, len(buy_signal_columns) + 1):
            combinations_buy = list(itertools.combinations(buy_signal_columns, r_buy))

            # Generate all combinations of sell signal columns
            for r_sell in range(1, len(sell_signal_columns) + 1):
                combinations_sell = list(itertools.combinations(sell_signal_columns, r_sell))

                # Iterate over each combination of buy and sell signals
                for combo_buy in combinations_buy:
                    selected_buy_columns = list(combo_buy)

                    for combo_sell in combinations_sell:
                        selected_sell_columns = list(combo_sell)

                        # Initialize the first row of Main_Signal as 0
                        self.df['Main_Signal'] = 0.0

                        main_signal = self.df['Main_Signal'].values
                        buy_signal_arr = self.df[selected_buy_columns].values
                        sell_signal_arr = self.df[selected_sell_columns].values

                        # Iterate over the remaining rows
                        for i in range(1, self.df.shape[0]):
                            previous_signal = main_signal[i - 1]

                            if previous_signal == 0:
                                # Use Buy Signals to determine current signal
                                buy_signal_conditions = np.all(buy_signal_arr[i] == 1)
                                sell_signal_conditions = np.all(sell_signal_arr[i] == 1)
                                main_signal[i] = int(buy_signal_conditions & sell_signal_conditions)

                            else:
                                # Use Sell Signals to determine current signal
                                sell_signal_conditions = np.all(sell_signal_arr[i] == 1)
                                main_signal[i] = int(sell_signal_conditions)

                        # Entry/Exit logic
                        self.df['Main_Signal'] = main_signal

                        # Performance Metrics
                        self.df['Entry/Exit'] = self.df['Main_Signal'].diff()
                        self.df["Position"] = self.share_size * self.df['Main_Signal']
                        self.df["Entry/Exit Position"] = self.df["Position"].diff()
                        self.df["Portfolio Holdings"] = self.df["Position"] * self.df['Close']
                        self.df["Portfolio Cash"] = self.initial_cash - (self.df['Close'] * self.df['Entry/Exit Position']).cumsum()
                        self.df["Portfolio Total"] = self.df["Portfolio Cash"] + self.df["Portfolio Holdings"]
                        self.df["Portfolio Daily Returns"] = self.df["Portfolio Total"].pct_change()
                        self.df["Portfolio Cumulative Returns"] = (1 + self.df["Portfolio Daily Returns"]).cumprod()
                        self.df['Buy And Hold Return'] = (1 + self.df["Close"].pct_change()).cumprod()

                        # Create a df with performance summary for each combination

                        # append evaluation metrics to a df as a new row
                        ann_ret =  self.df['Portfolio Daily Returns'].mean() * self.sqrt_val
                        cum_ret = self.df['Portfolio Cumulative Returns'].iloc[-1]
                        ann_volat = self.df['Portfolio Daily Returns'].std() * np.sqrt(self.sqrt_val)
                        sharpe = ann_ret / ann_volat
                        buy_and_hold = self.df['Buy And Hold Return'].iloc[-1]
                        new_row = {'Buy Signals' : f'{buy_signal_columns}',
                                   'Sell Signals' : f'{sell_signal_columns}',
                                   'Annualized Return' : ann_ret,
                                   'Cumulative Return' : cum_ret,
                                   'Annual Volatility' : ann_volat,
                                   'Sharpe Ratio' : sharpe,
                                   'Buy and Hold': buy_and_hold,
                                   'Ticker': self.ticker}
                        
                        eval_df = eval_df.append(new_row, ignore_index=True)
                        
                        clear_output(wait=True)
                        print(f'{selected_buy_columns} & {selected_sell_columns}')

        self.filtered_df = eval_df[eval_df['Cumulative Return'] > 0].sort_values('Cumulative Return', ascending = False)
        self.filtered_df['Beat Buy and Hold?'] = np.where(self.filtered_df['Cumulative Return'] > self.filtered_df['Buy and Hold'], True, False)        
        return self.filtered_df 

    def plot_top_strategy(self):
        top_5_strategies = self.filtered_df.head(5)

        # Iterate over each row in the top 5 strategies
        for index, row in top_5_strategies.iterrows():
            # Create a new figure for each strategy
            plt.figure(figsize=(25, 10))

            # Get the strategy name
            ticker = row['Ticker']
            selected_buy_columns = eval(row['Buy Signals'])
            selected_sell_columns = eval(row['Sell Signals'])

            # Initialize the first row of Main_Signal as 0
            self.df['Main_Signal'] = 0.0

            main_signal = self.df['Main_Signal'].values
            buy_signal_arr = self.df[buy_signal_columns].values
            sell_signal_arr = self.df[sell_signal_columns].values

            # Iterate over the remaining rows
            for i in range(1, self.df.shape[0]):
                previous_signal = main_signal[i - 1]

                if previous_signal == 0:
                    # Use Buy Signals to determine current signal
                    buy_signal_conditions = np.all(buy_signal_arr[i] == 1)
                    sell_signal_conditions = np.all(sell_signal_arr[i] == 1)
                    main_signal[i] = int(buy_signal_conditions & sell_signal_conditions)

                else:
                    # Use Sell Signals to determine current signal
                    sell_signal_conditions = np.all(sell_signal_arr[i] == 1)
                    main_signal[i] = int(sell_signal_conditions)

            # Entry/Exit logic
            self.df['Main_Signal'] = main_signal

            # Performance Metrics
            self.df['Entry/Exit'] = self.df['Main_Signal'].diff()
            self.df["Position"] = self.share_size * self.df['Main_Signal']
            self.df["Entry/Exit Position"] = self.df["Position"].diff()
            self.df["Portfolio Holdings"] = self.df["Position"] * self.df['Close']
            self.df["Portfolio Cash"] = self.initial_cash - (self.df['Close'] * self.df['Entry/Exit Position']).cumsum()
            self.df["Portfolio Total"] = self.df["Portfolio Cash"] + self.df["Portfolio Holdings"]
            self.df["Portfolio Daily Returns"] = self.df["Portfolio Total"].pct_change()
            self.df["Portfolio Cumulative Returns"] = (1 + self.df["Portfolio Daily Returns"]).cumprod()
            self.df['Buy And Hold Return'] = (1 + self.df["Close"].pct_change()).cumprod()

            # Create a new figure for each strategy
            plt.figure(figsize=(25, 10))

            # Get the entry/exit signal
            entry_exit = self.df['Entry/Exit']
            bnh = self.df['Buy And Hold Return']
            close = self.df['Close']
            ema = self.df['EMA_20']

            portfolio_cumulative_returns = self.df['Portfolio Daily Returns']

            # Plot the portfolio cumulative returns
            plt.plot(bnh, label=f'{self.ticker} Cumulative Return')
            plt.plot(portfolio_cumulative_returns, label='Portfolio Cumulative Returns')

            # Plot the entry points as vertical lines
            for entry_index in entry_exit[entry_exit == 1].index:
                plt.axvline(entry_index, color='g', linestyle='--')

            # Plot the exit points as vertical lines
            for exit_index in entry_exit[entry_exit == -1].index:
                plt.axvline(exit_index, color='r', linestyle='--')

            # Set the plot title and labels
            plt.title("Strategy - Entry/Exits")
            plt.xlabel("Time")
            plt.ylabel("Price")
            plt.legend()

            # Show the plot for the current strategy
            plt.show()

# Define a class
class BespokeStrategy:
    
    def __init__(self, ticker, interval, stocks_df, share_size = 100, initial_cash = 100000):
        
        if interval == '5m':
            self.sqrt_val = 252 * 78 
        elif interval == '15m':
            self.sqrt_val = 252 * 26  
        elif interval == '30m':
            self.sqrt_val = 252 * 13 
        elif interval == '1h':
            self.sqrt_val = 252 * 6.5
        elif interval == '1d':
            self.sqrt_val = 252
            
        print(self.sqrt_val)
            
        self.stocks_df = stocks_df
        self.interval = interval
        self.ticker = ticker
        self.share_size = share_size
        self.initial_cash = initial_cash
        
        # Call the basic methods in the __init__ constructor to be immediately executed
        
        self.get_individual_stock()
        self.indicators()
        self.signals()

    def get_individual_stock(self):
        mask = self.stocks_df.columns.get_level_values(1) == self.ticker
        self.df = self.stocks_df.loc[:, mask]
        self.df.columns = self.df.columns.droplevel(1)
        self.df.dropna(inplace = True, axis = 0)
        
    def indicators(self):
        
        ### BUY INDICATORS ###
        
        # MACD
        self.df[['MACD', 'SIGNAL']] = TA.MACD(self.df)
        
        # Rolling return window
        self.df['Returns'] = self.df['Close'].pct_change()
        self.df['60_Day_Return'] = (self.df['Returns'] + 1).rolling(window=60).apply(lambda x: x.prod(), raw=True)
        
        # SQZ
        self.df['SQZ'] = TA.SQZMI(self.df)
        
        ### SELL INDICATORS ###
        
        # EMA
        self.df['EMA_20'] = TA.EMA(self.df, 20)
        # ADX
        self.df['ADX'] = TA.ADX(self.df)
   
    def signals(self):
        
        ### BUY SIGNALS ###
        

        
        # 60 day return lookback window
        self.df['60_Day_Return_Signal'] = 0.0
        self.df['60_Day_Return_Signal'] = np.where(self.df['60_Day_Return'] > 0.50, 1.0, 0.0)
        
        # EMA Signal logic
        self.df['EMA20_Signal'] = 0.0
        self.df['EMA20_Signal'] = np.where(self.df['Close'] > self.df['EMA_20'], 1.0, 0.0)      
        
        # SQZ Signal logic
        self.df['SQZ_Signal'] = 0.0
        self.df['SQZ_Signal'] = np.where(self.df['SQZ'] == True, 1.0, 0.0)
        
        # MACD Signal logic
        self.df['MACD_Signal'] = 0.0
        self.df['MACD_Signal'] = np.where(self.df['MACD'] > self.df['SIGNAL'], 1.0, 0.0) 
        
        ### SELL SIGNALS ### 
        
        # ADX Signal logic
        self.df['ADX_Signal'] = 0.0
        self.df['ADX_Signal'] = np.where(self.df['ADX'] <= 30, 0.0, 1.0)        

        
    def result(self):
        
        # Define eval df columns
        columns = ['Buy Signals', 'Sell Signals', 'Annualized Return', 'Cumulative Return', 'Annual Volatility', 'Sharpe Ratio']
        self.eval_df = pd.DataFrame( columns= columns)
        # Define the signal column names
        buy_signal_columns = ['MACD_Signal', 'ADX_Signal']
        sell_signal_columns = ['MACD_Signal', 'EMA20_Signal']
        
        # Initialize the first row of Main_Signal as 0
        self.df['Main_Signal'] = 0.0
        
        main_signal = self.df['Main_Signal'].values
        buy_signal_arr = self.df[buy_signal_columns].values
        sell_signal_arr = self.df[sell_signal_columns].values

        # Iterate over the remaining rows
        for i in range(1, self.df.shape[0]):
            previous_signal = main_signal[i - 1]

            if previous_signal == 0:
                # Use Buy Signals to determine current signal
                buy_signal_conditions = np.all(buy_signal_arr[i] == 1)
                sell_signal_conditions = np.all(sell_signal_arr[i] == 1)
                main_signal[i] = int(buy_signal_conditions & sell_signal_conditions)
                
            else:
                # Use Sell Signals to determine current signal
                sell_signal_conditions = np.all(sell_signal_arr[i] == 1)
                main_signal[i] = int(sell_signal_conditions)
        
        # Entry/Exit logic
        self.df['Main_Signal'] = main_signal
        self.df['Entry/Exit'] = self.df['Main_Signal'].diff()


        # Performance Metrics
        self.df["Position"] = self.share_size * self.df['Main_Signal']
        self.df["Entry/Exit Position"] = self.df["Position"].diff()
        self.df["Portfolio Holdings"] = self.df["Position"] * self.df['Close']
        self.df["Portfolio Cash"] = self.initial_cash - (self.df['Close'] * self.df['Entry/Exit Position']).cumsum()
        self.df["Portfolio Total"] = self.df["Portfolio Cash"] + self.df["Portfolio Holdings"]
        self.df["Portfolio Daily Returns"] = self.df["Portfolio Total"].pct_change()
        self.df["Portfolio Cumulative Returns"] = (1 + self.df["Portfolio Daily Returns"]).cumprod()
        self.df['Buy And Hold Return'] = (1 + self.df["Close"].pct_change()).cumprod()

        # Create a df with performance summary for each combination

        # append evaluation metrics to a df as a new row
        ann_ret =  self.df['Portfolio Daily Returns'].mean() * self.sqrt_val
        cum_ret = self.df['Portfolio Cumulative Returns'].iloc[-1]
        ann_volat = self.df['Portfolio Daily Returns'].std() * np.sqrt(self.sqrt_val)
        sharpe = ann_ret / ann_volat
        buy_and_hold = self.df['Buy And Hold Return'].iloc[-1]
        new_row = {'Buy Signals' : f'{buy_signal_columns}',
                   'Sell Signals' : f'{sell_signal_columns}',
                   'Annualized Return' : ann_ret,
                   'Cumulative Return' : cum_ret,
                   'Annual Volatility' : ann_volat,
                   'Sharpe Ratio' : sharpe,
                   'Buy and Hold': buy_and_hold,
                   'Ticker': self.ticker}
        self.eval_df = self.eval_df.append(new_row, ignore_index=True)
        self.eval_df['Beat Buy and Hold?'] = np.where(self.eval_df['Cumulative Return'] > self.eval_df['Buy and Hold'], True, False)     
        
        return self.eval_df

    def plot_strategy(self):

        # Create a new figure for each strategy
        plt.figure(figsize=(25, 10))
        
        # Get the entry/exit signal
        entry_exit = self.df['Entry/Exit']
        bnh = self.df['Buy And Hold Return']
        close = self.df['Close']
        ema = self.df['EMA_20']
        
        portfolio_cumulative_returns = self.df['Portfolio Daily Returns']
        
        # Plot the portfolio cumulative returns
        plt.plot(bnh, label=f'{self.ticker} Cumulative Return')
        plt.plot(portfolio_cumulative_returns, label='Portfolio Cumulative Returns')
        
        # Plot the entry points as vertical lines
        for entry_index in entry_exit[entry_exit == 1].index:
            plt.axvline(entry_index, color='g', linestyle='--')

        # Plot the exit points as vertical lines
        for exit_index in entry_exit[entry_exit == -1].index:
            plt.axvline(exit_index, color='r', linestyle='--')

        # Set the plot title and labels
        plt.title("Strategy - Entry/Exits")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.legend()

        # Show the plot for the current strategy
        plt.show()


# class to test different strategies            
class Tester:
    
    def __init__(self, interval, stocks_df, stock_list):
        
        self.stock_list = stock_list
        self.interval = interval
        self.stocks_data = stocks_df
        
        
        self.backtest_on_stocks()
        self.top_return()
        self.top_sharpe()
        self.beat_bnh()
        
    def backtest_on_stocks(self):
        self.combined = pd.DataFrame()
        for index, stock in enumerate(self.stock_list):
            self.iterator = SignalIterator(stock, interval = self.interval, stocks_df = self.stocks_data)
            result = self.iterator.result()
            self.combined = pd.concat([self.combined, result], axis=0)
            clear_output(wait=True)
            print(f'{stock} analysis complete ({index+1}/{len(self.stock_list)})')
    
    def top_return(self):
        return self.combined.sort_values('Cumulative Return', ascending= False).head(50)
    
    def top_sharpe(self):
        return self.combined.sort_values('Sharpe Ratio', ascending= False).head(50)
    
    def beat_bnh(self):
        return self.combined[self.combined['Beat Buy and Hold?'] == True].sort_values('Cumulative Return', ascending= False).head(50)
    def plot_top(self):
        self.iterator.plot_top_strategy()