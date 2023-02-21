# Maximize Profit

You have 5 days of stock price data. For each day, there's an array of for which the n-th element is the price of a given stock within a day. The first element in array is start price for that day.

You are only allowed to complete one transaction (buy and sell 1 share of the stock) to find the most profit.

## Data
tickers_prices_day_1.csv (1 file for each day)
* XYZ: [1, 4, 3] -  XYZ is the ticker (stock symbol) with a start price of 1 and close price 3 for a given day.

tickers_sectors.csv
* mapping of tickers to their respective sectors

## Examples
Example 1
Input- ABC: [8, 2, 6, 4, 7, 5]
Result- 5
* max. difference = 7-2 = 5 (not 8-2 = 6, selling price needs to be higher than buying price.)

Example 2
Input- ABC: [8, 7, 5, 4, 2]
Result- 0
* no transaction, max profit = 0

## Questions to Answer
* Which ticker has the most profit on which day?
* Which ticker has the most profit in a 5 days?
* Which sector performed best?

Submit complete source code with answers, printed to console.
