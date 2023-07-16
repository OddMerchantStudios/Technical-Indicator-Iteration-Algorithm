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
- ~~Fundamental metrics under considering for model building and forecasting include:~~
  - ~~P/E ratio~~
  - ~~Industry Sector~~
  - ~~Price-Sales~~
  - ~~Price-Book~~
  - ~~PEG Ratio~~
  - ~~Net Profit Margin~~
  - ~~ROE~~
  - ~~ROA~~
  - ~~ROI~~
  - ~~EPS beat last quarter (Y/N)~~
  - ~~% EPS beats last 4 quarter’s (x/4)~~
  - ~~% EPS beats last 8 quarter’s (x/8)~~
  - ~~EPS beat % last quarter (x%)~~
  - ~~% EPS beats last 4 quarter’s (x%)~~
  - ~~% EPS beats last 8 quarter’s (x%)~~
  - ~~Sales beat last quarter (Y/N)~~
  - ~~% Sales beats last 4 quarter’s (x/4)~~
  - ~~% Sales beats last 8 quarter’s (x/8)~~
  - ~~Sales beat % last quarter (x%)~~
  - ~~% Sales beats last 4 quarter’s (x%)~~
  - ~~% Sales beats last 8 quarter’s (x%)~~
  - ~~Forward guidance change (up/down/no)~~
  - ~~% guidance change (+/-/0)~~
  - ~~EBITDA~~

- Trading Timeframes for data collection and analysis include:
  - ~~Intra-Day:~~
    - ~~2m~~
    - ~~3m~~
    - ~~5m~~
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
  - 2017 – 2020
- Forecasting: Quant Algo Fund Simulation - Forward testing period: 5 years (yearly)
  - 2021 – 2023

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

--------------
## Notebooks
- [JUPYTER LAB NOTEBOOK LINK](./main.ipynb)
- [Final Analysis](./file.ipynb)
---------

## Getting Started - Prerequisites
-----------
### ​You must have Python 3 installed:

```
python3 --version
```

### You must have Anaconda installed:
```
$ anaconda --version
```

### Install Environmnet:
```
conda create -n <env_name> python=3.7 anaconda
```

### Clone/Run Repository 
```
git clone git@github.com:OddMerchantStudios/Project-2-Algo.git
```

### Activate Environment
```
conda activate <env_name>
```

### Install Dependencies
- Please make sure you are in your intended activate environment before running this command
```
pip install -r requirements.txt
```


## Built With

- [![Python 3.7.13](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)]([https://www.python.org/downloads/release/python-3713/)
[![Python](https://img.shields.io/badge/Python-3.7.13-blue)](https://www.python.org/downloads/release/python-3713/) - Programming Language
- [![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/docs/#) - Data maniupulation library
- [![Numpy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/) - Multi-dimensional array library
- [![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/python/) - Visualization library for plots
- [![Matplotlib](https://img.shields.io/badge/Matplotlib-3776AB?style=for-the-badge&logo=plotly&logoColor=white)](https://matplotlib.org/) - Visualization library for plots
- [![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=for-the-badge&logo=plotly&logoColor=white)](https://seaborn.pydata.org/) - Visualization library for plots
- [![Alpaca](https://img.shields.io/badge/Alpaca-3776AB?style=for-the-badge&logo=plotly&logoColor=white)](https://alpaca.markets/) - Trading API
- [![HVPlot](https://img.shields.io/badge/HVPlot-3776AB?style=for-the-badge&logo=plotly&logoColor=white)](https://hvplot.holoviz.org/) - Visualization library for plots
- [![PyViz](https://img.shields.io/badge/PyViz-3776AB?style=for-the-badge&logo=plotly&logoColor=white)](https://pyviz.org/) - Visualization library for plots
- [![GeoViews](https://img.shields.io/badge/GeoViews-3776AB?style=for-the-badge&logo=plotly&logoColor=white)](https://geoviews.org/) - Visualization library for plots
- [![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)](https://jupyter.org/) - Notebook IDE
- [![JupyterLab](https://img.shields.io/badge/JupyterLab-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)](https://jupyter.org/) - Notebook IDE
- [![Anaconda](https://img.shields.io/badge/Anaconda-44A833?style=for-the-badge&logo=anaconda&logoColor=white)](https://www.anaconda.com/) - Data science platform
- [![Yahoo Finance API](https://img.shields.io/badge/Yahoo%20Finance%20API-800080?style=for-the-badge&logo=yahoo&logoColor=white)](https://pypi.org/project/yfinance/) - Yahoo Finance API
- [![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/stable/) - Machine learning library
- [![Quantstats](https://img.shields.io/badge/Quantstats-800080?style=for-the-badge&logo=yahoo&logoColor=white)](https://pypi.org/project/quantstats/) - Quantstats library
- [![PyPortfolioOpt](https://img.shields.io/badge/PyPortfolioOpt-800080?style=for-the-badge&logo=yahoo&logoColor=white)](https://pypi.org/project/pyportfolioopt/) - PyPortfolioOpt library
- [![Cufflinks](https://img.shields.io/badge/Cufflinks-800080?style=for-the-badge&logo=yahoo&logoColor=white)](https://pypi.org/project/cufflinks/) - Cufflinks library

## Authors
- **Kirill Chugunov** - [LinkedIn](https://www.linkedin.com/in/kirill-chugunov-b680811a4/) | [Github](https://github.com/OddMerchantStudios)
- **Hiren Patel** - [LinkedIn](https://www.linkedin.com/in/hdpatel/) | [Github](https://github.com/hpnhs25)
- **Varoujan John Khorozian** - [LinkedIn](https://www.linkedin.com/in/varoujan-khorozian/) | [Github](https://github.com/vkhorozian)
