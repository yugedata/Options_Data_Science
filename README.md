Options_Data_Science

Disclosure: Most files in this repo are under maintenance, 
            REFER only to mine.py, make_files.py, token_refresh.py 

Description: 

1. mining - retrieve raw options data with TD ameritrade APIs
2. analyzing - researching trends and paper trading spreads
3. visualizing - graphing data and trading results with matplotlib and Tableau
            

  
Directions: 

a) create a developer account on this link. https://developer.tdameritrade.com/apis

b) run token_refresh.py to produce the td_state.json credentials file

c) Before mining, SQLite files must be made locally. In your working directory make a 'Data' folder
   Open make_files.py in your working directory and run it to produce a sqlite file for each trading
   day of 2021. Add or remove different columns in the columns_wanted array in create_files.py
   In mine.py lookup up columns_unwanted, those are the options i didnt use but you can add.
   

* In the stocks array, edit this list to collect options for any stock you want

* Inside the get_get() method, 'toDate' value is a date.
Change the date to pull all weekly option chains leading up to that day. 
Make sure the date is a Friday.

d) Run mine.py right before market opens. ~09:25 EST



** ONLY IF CREATING FILES FROM INSIDE mine.py
The tables created for puts and calls are based off the wanted and unwanted                     
columns. They are hard coded into arrays (wanted_columns & unwanted_columns)                     
at the top of the file. To create tables with different columns move the                         
column name from one array to the other, all must be accounted for in both                   
lists.

            
            
 Future addons:
 1) live trading
 2) back testing
 3) gui to activate and deactive different trading algos and keep track of paper portfolio
 4) twitter sentiment 
 5) econmic models to predict market volatility
 6) adding to a variety of different trading systems
            
            
            
