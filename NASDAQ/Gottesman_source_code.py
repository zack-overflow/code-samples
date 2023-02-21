# Zachary Gottesman
# Nasdaq Exercise Source Code
# Friday, January 29, 2020

# Make sure pandas is installed (pip install pandas) for this script to run properly
import pandas as pd

def process_daily_data(filename):
    df = pd.read_csv(filename, header=None)

    df = df.set_index(0)
    df = df.rename_axis(None, axis=0)

    df[1] = df[1].map(lambda x: x.lstrip('['))
    df[8] = df[8].map(lambda x: x.rstrip(']'))
    
    return df


def find_max_profit(df):
    top_ticker = ""
    daily_max_profit = 0
    for index, row in df.iterrows():
        min_price = int(row[1])
        max_profit = 0

        for i in range(1, len(row)):
            min_price = min(min_price, int(row[i]))
            potential_profit = int(row[i]) - min_price
            max_profit = max(max_profit, potential_profit)

        if max_profit > daily_max_profit:
            daily_max_profit = max_profit
            top_ticker = index
        
    return (top_ticker, daily_max_profit)

def combine_dfs(day_files):
    
    combined = process_daily_data(day_files[0])
    for i in range(1, len(day_files)):
        day_filename = day_files[i]
        df = process_daily_data(day_filename)
        combined = combined.join(df, rsuffix="_repeat", how="outer")
    combined.columns = range(1, combined.shape[1]+1)
    return combined

def process_sectors(filename):
    df = pd.read_csv(filename, header=None)
    df = df.set_index(0)
    df = df.rename_axis(None, axis=0)
    df.columns = ["Sector"]
    return df


def find_ticker_performance(ticker_data):
    initial_price = ticker_data[1]
    final_price = ticker_data[len(ticker_data)]
    return int(final_price) - int(initial_price)


def find_sector_performance(sectors_df, tickers_df):
    
    sectors_performance = {}
    for sector in process_sectors("tickers_sectors.csv").Sector.unique():
        sectors_performance[sector] = 0
        
    for index, row in tickers_df.iterrows():
        ticker_performance = find_ticker_performance(row)
        ticker_sector = sectors_df.loc[index].Sector
        sectors_performance[ticker_sector] += ticker_performance
    
    return sectors_performance

def pick_best_sector(sectors_performance):
    
    top_sector = ""
    best_performance = float("-inf")
    
    for sector in sectors_performance:
        if sectors_performance[sector] > best_performance:
            top_sector = sector
            best_performance = sectors_performance[sector]
    
    return top_sector, best_performance


def full_pipeline_part_1(day_files):
    top_stocks = []
    for day_filename in day_files:
        df = process_daily_data(day_filename)
        ticker, profit = find_max_profit(df)
        top_stocks.append((ticker, profit))
    
    top_stock_day = 1
    top_stock = top_stocks[0][0]
    max_profit = top_stocks[0][1]
    
    for i in range(1,len(top_stocks)):
        stock = top_stocks[i]
        
        if stock[1] > max_profit:
            top_stock_day = i + 1
            top_stock = stock[0]
            max_profit = stock[1]
            
    return top_stock, max_profit, top_stock_day


def generate_answer_part_1(days):
    top_stock, max_profit, top_stock_day = full_pipeline_part_1(days)
    print(f"1. The top ticker was {top_stock} from day {top_stock_day}, which generated a profit of {max_profit}!")


def full_pipeline_part_2(day_files):
    
    combined_df = combine_dfs(day_files)
    return find_max_profit(combined_df)

def generate_answer_part_2(days):
    top_stock, max_profit = full_pipeline_part_2(days)
    print(f"2. I understood this question to ask me to find the best stock if you were allowed to buy and sell at any point within the five day period. In that case, the top ticker was {top_stock}, which generated a profit of {max_profit}!")


def full_pipeline_part_3(day_files, sectors_file):
    
    sectors_df = process_sectors(sectors_file)
    combined_df = combine_dfs(day_files)
    
    sector_performances = find_sector_performance(sectors_df, combined_df)
    
    return pick_best_sector(sector_performances)


def generate_answer_part_3(days):
    top_stock, max_profit = full_pipeline_part_3(days, "tickers_sectors.csv")
    print(f"3. I found the question prompt slightly confusing, but I interpreted it to mean that we wanted to look for the sector whose stocks had the greatest sum of performance. By performance, I mean the difference between the stock's price on the last day compared to the first day. Given this interpretation, the top ticker was {top_stock}, which generated a profit of {max_profit}!")

def generate_answers():
    days = ["tickers_prices_day_1.csv",
            "tickers_prices_day_2.csv",
            "tickers_prices_day_3.csv",
            "tickers_prices_day_4.csv",
            "tickers_prices_day_5.csv"]
    generate_answer_part_1(days)
    print()
    generate_answer_part_2(days)
    print()
    generate_answer_part_3(days)

generate_answers()
