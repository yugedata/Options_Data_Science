Options_Data_Science

Disclosure: 

1. Most files in this repo are under maintenance, REFER only to mine.py, token_refresh.py, test_trade.py 
2. If you want stock data simultanously, run test_trade.py. it is not finished though
3. The file paths in my code work for MacOS, if on windows you will have to edit all the file paths

Description: 

1. mining - retrieve raw options data with TD ameritrade APIs - Directions bellow are for this
2. analyzing - researching trends and paper trading spreads 
3. visualizing - graphing data and trading results with matplotlib and Tableau
            

  
Directions: 

a) create a developer account on this link. https://developer.tdameritrade.com/apis. 
* Create/register an App


b) pip install td-ameritrade-python-api


c) run token_refresh.py to produce the td_state.json credentials file. 
   YouTube video to help: skip to minute 22!!
   https://www.youtube.com/watch?v=8N1IxYXs4e8&t=1138s&ab_channel=SigmaCoding


d) In your working directory make a 'Data' for data storage
            The tables created in mine.py will have the columns specified in the columns_wanted array. 
            * If you want to remove a column, cut it out of columns_wanted and paste it in columns_unwanted. 
            * If you want to add a column, cut it out of columns_unwated and paste it in columns_wanted. 
            * All possible columns must be accounted for in both arrays.
   

* In the stocks array, edit this list to collect options for any stock you want

* in main(), change the argument in last_chain(#) to how many weeks of data u want. -> to_date = str(last_chain(5))


e) Run mine.py right before market opens. ~09:25 EST

            
After getting familiar with the mine script, refer to test_trade how where to insert your own trading logic
      
 Future addons:
 1) live trading
 2) back testing
 3) gui to activate and deactive different trading algos and keep track of paper portfolio
 4) twitter sentiment 
 5) econmic models to predict market volatility
 6) adding to a variety of different trading systems
            
            
            
