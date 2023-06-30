# Project 2 Outline:

## Project Goal:

This project will focus on creating, back testing, forecasting, and analyzing algorithmic trading strategies.  This project will focus on creating and testing algos based on technical and fundamental analysis.  We’ll be creating strategies for:

    - Intra-day trading (hourly holding period) 
    - Swing trades (1-20 day holding periods)
    - Position trades (6-12 month holding periods)

1. Data Collection: 
- Obtain historical data for the desired timeframe.
- Yahoo Finance data, Interactive Brokers data will be our primary data sources.
- Stocks, ETFs, Indexes will be analyzed along with the following Technical and Fundamental features: 
- Technical indicators under consideration in algo model building include:
  - Squeeze Indicator (Bollinger Bands + Keltner  Channels)
  - 8 and 21 EMA
  - MACD Two-Line
  - ADX Indicator
  - Other potential features to test: Stochastic Oscillator, RSI
- Fundamental metrics under considering for model building and forecasting include:
  - P/E ratio
  - Industry Sector
  - Price-Sales
  - Price-Book
  - PEG Ratio
  - Net Profit Margin
  - ROE
  - ROA
  - ROI
  - EPS beat last quarter (Y/N)
  - % EPS beats last 4 quarter’s (x/4)
  - % EPS beats last 8 quarter’s (x/8)
  - EPS beat % last quarter (x%)
  - % EPS beats last 4 quarter’s (x%)
  - % EPS beats last 8 quarter’s (x%)
  - Sales beat last quarter (Y/N)
  - % Sales beats last 4 quarter’s (x/4)
  - % Sales beats last 8 quarter’s (x/8)
  - Sales beat % last quarter (x%)
  - % Sales beats last 4 quarter’s (x%)
  - % Sales beats last 8 quarter’s (x%)
  - Forward guidance change (up/down/no)
  - % guidance change (+/-/0)
  - EBITDA

• Trading Timeframes for data collection and analysis include:
- Intra-Day:
  - 2m
  - 3m
  - 5m
- Swing Day:
  - 15 m
  - 30 m
  - Daily
- Position Day:
  - Daily
  - Weekly
  - Monthly
- Gather relevant features such as opening price, closing price, highest price, lowest price, and volume for each time intervals. 
- Time Periods: Model Building
  - Training and back-testing period: 10 years (normal train/test split)
  - 2007 – 2017
- Forecasting: Model Implementation and Review - Forward testing period: 5 years (yearly)
  - 2018 – 2022

2. Data Preprocessing:
   - Perform data cleaning by handling missing values,  outliers, and inconsistencies.
   - Explore the dataset to identify any potential  patterns or correlations between features.
   - Split the dataset into training and testing sets,  considering an appropriate ratio (e.g., 80% for  training, 20% for testing).
3. Feature Engineering:
   - Extract relevant features from the dataset that can  capture the characteristics of momentum price  movement in various trading instruments (stocks,  ETFs, Indexes).
   - Examples of features could include price  volatility, relative price changes, technical  indicators (e.g., Bollinger Bands, moving averages),  or any other domain-specific indicators that are  known to be relevant.
4. Model Selection and Training:
  -  Choose a suitable machine learning algorithm for binary classification (buy/sell signals, performance segments by % returns, price action patterns).
  - Intra-Day Algo Models:
    - Return Rank Segmentation (last month returns, last quarter, last 6 months, last 12 months)
    - Trend/Swing/Chop Segmentation (OHLC prices by time)
    - Technical and Fundamental signal model (features above)
 - Swing Trades Algo Models:
    - Return Rank Segmentation
    - Trend/Swing/Chop Segmentation
    - Technical and Fundamental signal model
 - Position Trades Algo Models:
   - Return Rank Segmentation
   - Trend/Swing/Chop Segmentation
   - Technical and Fundamental signal model
 - Train the model using the training dataset, using appropriate techniques such as cross-validation and hyper parameter tuning to optimize model performance.
 - Evaluate the model's performance metrics, such as accuracy, precision, recall, and F1-score, to assess its effectiveness in predicting momentum trades.
5. Model Deployment and Testing:
 - Deploy the trained model in a trading algo strategy.
 - Apply the model to the testing dataset and evaluate its performance metrics on unseen data.
 - Analyze the model's predictions and compare them with the actual market movement to assess the model's accuracy and reliability.
6. Iteration and Improvement:
 - Iterate and refine the model based on the evaluation results.
 - Explore different algorithms, feature combinations, or data transformations to improve the model's accuracy and robustness.
 - Continuously monitor and update the model's performance as new data becomes available.
