import pandas as pd

def load_data():
    excel_path = 'data/Sample - Superstore.xlsx'
    df = pd.read_excel(excel_path, sheet_name='Orders')
    dfd = pd.read_excel(excel_path, sheet_name='Returns')

    accumulated_sales = df['Sales'].sum()
    profit_ratio = df['Profit'].sum() / accumulated_sales if accumulated_sales != 0 else 0
    total_discount = df['Discount'].sum()
    average_quantity = df['Quantity'].mean() 
    average_days_to_ship = df['Ship Date'] - df['Order Date']
    total_returns = dfd['Returned'].count()  

    return df, accumulated_sales, profit_ratio, total_discount, average_quantity, average_days_to_ship, total_returns

df, accumulated_sales, profit_ratio, total_discount, average_quantity, average_days_to_ship, total_returns = load_data()
