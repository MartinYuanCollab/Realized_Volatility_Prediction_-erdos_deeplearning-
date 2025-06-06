import pandas as pd
import numpy as np

def book_for_stock(str_file_path,stock_id,time_id,create_para=True):
    """
    A function that returns a pandas dataframe containing the book data of a stock specified in str_file_path with certain time_id. 
    The function defaulted to create the wap and log return of wap, but this can be turned off by setting create_para to False. 
    :param str_file_path: A str of the path to the file of book data (parquet). 
    :param stock_id: The chosen stock_id. 
    :param time_id: An int that indicates the interested time_id. 
    :param create_para: Decides if wap and log return of wap will be created, defaulted to True. 
    :return: A dataframe containing book data of a chosen stock at time id. 
    """
    int_stock_id=stock_id
    str_file_path=str_file_path+"/stock_id="+str(int_stock_id)
    df_raw_book=pd.read_parquet(str_file_path)
    df_raw_book=df_raw_book[df_raw_book["time_id"]==time_id]
    # int_stock_id=int(str_file_path.split("=")[1])
    df_raw_book.loc[:,"stock_id"]=int_stock_id
    if create_para: 
        df_raw_book["wap"] = (df_raw_book["bid_price1"]*df_raw_book["ask_size1"]+df_raw_book["ask_price1"]*df_raw_book["bid_size1"])/(df_raw_book["bid_size1"]+df_raw_book["ask_size1"])
        df_raw_book.loc[:,"log_return"] = np.log(df_raw_book["wap"]).diff()
        df_raw_book=df_raw_book[~df_raw_book["log_return"].isnull()]
    df_raw_book=df_raw_book.reset_index()
    
    return df_raw_book

def trade_for_stock(str_file_path,stock_id,time_id):
    """
    A function that returns a pandas dataframe containing the trade data of a stock at a chosen time_id. 
    :param str_file_path: A str of the path to the file of trade data (parquet). 
    :param stock_id: The chosen stock_id. 
    :param time_id: An int that indicated the interested time_id. 
    :return: A pandas dataframe containing trade data of a chosen stock at time_id. 
    """
    int_stock_id=stock_id
    str_file_path=str_file_path+"/stock_id="+str(int_stock_id)
    df_raw_trade = pd.read_parquet(str_file_path) 
    df_raw_trade=df_raw_trade[df_raw_trade["time_id"]==time_id]
    # int_stock_id=int(str_file_path.split("=")[1])
    df_raw_trade.loc[:,"stock_id"]=int_stock_id
    return df_raw_trade 

def realized_vol(df_in,return_row_id=True): 
    """
    A function that returns the realized volatility based on the log return series input (for instance book["log_return"] where is book is a pandas dataframe containing book data for a stock and time id). 
    :param df_in: dataframe containing log return data (with "log_return" column). 
    :param return_row_id: Decides if the return value is a pair of form (Realized volatility,row_id) or only Realized volatility, defaulted to be True. 
    :return: return a value or a pair depending on the choice of return_row_id. 
    """
    
    series_log_return=df_in["log_return"]
    rv=np.sqrt(np.sum(series_log_return**2))
    stock_id=str(df_in["stock_id"][0])
    time_id=str(df_in["time_id"][0])
    row_id=stock_id+"-"+time_id
    if return_row_id:
        return rv, row_id
    else: 
        return rv