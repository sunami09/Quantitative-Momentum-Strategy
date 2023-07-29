# Quantitative Momentum Strategy: A Weighted Mean Analysis for Portfolio Optimization


This repository contains the implementation of a comprehensive Quantitative Momentum Strategy that uses a weighted mean analysis to optimize portfolio allocation. 

 <div align = "center">
<img width="800" alt="Screenshot 2023-07-29 at 10 57 35 AM" src="https://github.com/sunami09/Quantitative-Momentum-Strategy/assets/66564001/2cc4193d-cdac-4999-b5a8-d6cbddb43bff">
</div>
  
The strategy integrates two key financial indicators: Market Capitalization and Momentum Performance Indices, to identify lucrative investment opportunities.


## Overview

The core of this strategy is a dual-weighting algorithm. It attributes a higher weight to the Momentum Performance Indices, a composite measure encapsulating short and medium-term momentum, calculated using statistical percentile scores of daily, 5-day, monthly, and quarterly returns. Simultaneously, it assigns a lesser weight to the Market Capitalization of the stocks, a measure of a company's total market value, to ensure a balanced exposure across different market segments.

```python
for i in range(0, len(df.index)):
   d1 = df.loc[i, '1D']
   d5 = df.loc[i, '5D'] * 1.5
   m1 = df.loc[i, '1M'] * 1.25
   m3 = df.loc[i, '3M'] * 0.25
   df.loc[i, 'HQM Score'] = mean([d1, d5, m1, m3])
```

The strategy is dynamic, adjusting the portfolio weights based on the evolving market conditions and momentum scores of the stocks. This risk-adjusted approach aims to maximize the Sharpe Ratio, a measure of risk-adjusted returns, of the portfolio.

```python
for i in range(0, len(df.index)):
   df.loc[i, 'H'] = (df.loc[i, 'HQM Score'] / total_h) * 100
   df.loc[i, 'M'] = (df.loc[i, 'Market Cap ($)']/ total_asset) * 100
   df.loc[i, 'TM'] = (df.loc[i, 'H'] * 0.85) + (df.loc[i, 'M'] * 0.15)
```

## Implementation

The implementation of this strategy is facilitated through the Alpaca API, a robust financial services API that enables seamless execution of trades. The underlying technology stack includes Python for data processing and statistical analysis, pandas for data manipulation, and scipy for statistical functions. The project also uses the Financial Modeling Prep API for real-time financial data and the openpyxl library for Excel operations.

```python
def order(symbol, shares, side):
    data = {
        "symbol": symbol,
        "qty": shares,
        "side": side,
        "type": "market",
        "time_in_force": "day"
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        print(f"Failed to {side} {symbol} shares")
```

## Results

After running the algorithm, we get a list of stocks with their respective weights and the number of shares to buy. Here is a snippet of the output:

| Name | Symbol | Price ($) | Weight (%) | Shares to Buy |
| --- | --- | --- | --- | --- |
| Align Technology, Inc. | ALGN | 392 | 94.52 | 0.15 |
| Packaging Corporation of America | PKG | 154.59 | 94.14 | 0.36 |
| WestRock Company | WRK | 33.09 | 93.77 | 1.66 |
| T. Rowe Price Group, Inc. | TROW | 127.60 | 93.54 | 0.44 |
| MSCI Inc. | MSCI | 560.80 | 93.38 | 0.10 |
| Newell Brands Inc. | NWL | 10.91 | 92.71 | 4.95 |
| International Paper Company | IP | 35.98 | 92.59 | 1.53 |
| Pentair plc | PNR | 70.24 | 91.89 | 0.77 |
| Cincinnati Financial Corporation | CINF | 109.26 | 91.85 | 0.50 |
| Western Digital Corporation | WDC | 42.27 | 91.46 | 1.28 |


The complete results are saved in an Excel file for further analysis and review.

## Investment Horizon

The investment horizon for this strategy is small to medium term. The strategy is designed to capture the momentum in the stocks over a period of time and hence, it is best suited for investors with a small to medium term investment horizon.

## Conclusion

This project stands as a testament to the power of combining traditional financial indicators with modern quantitative techniques to create a robust, data-driven investment strategy. It demonstrates how a systematic, data-driven approach can lead to effective portfolio management and potentially superior returns.

## Disclaimer

Investing in the stock market involves risk and potential loss of principal, investors are advised to do their own due diligence and research before making any investment decisions. The strategies discussed here are for illustrative and educational purpose only and are not a recommendation or solicitation to buy or sell any securities.
