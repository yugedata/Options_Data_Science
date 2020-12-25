# Options_Data_Science

Description: 1. mining - retrieve raw options data with TD ameritrade APIs
             2. analyzing - researching trends and paper trading spreads
             3. visualizing - graphing data and trading results with matplotlib and Tableau
             
   
   
Directions: a) create a developer account on this link. https://developer.tdameritrade.com/apis
            b) run token_refresh.py to produce the td_state.json credentials file
            c) Before mining, SQLite files must be made locally.
                   1) go to the bottom of the file uncomment make_sqlite_table('calls')
                   2)                                        make_sqlite_table('puts')
                   3) comment the main() on the last line
                   4) run mine.py
                 fyi) The tables created for puts and calls are based off the wanted and unwanted                       columns. They are hard coded into arrays (wanted_columns & unwanted_columns)                       at the top of the file. To create tables with different columns move the                           column name from one array to the other, all must be accounted for in both                         lists.
            d) Options.db should have been created in your directory with 2 Tables
            e) reverse step(c, 1-3) & run mine.py during market hours 930-1600 est 
            
            
            
 Future addons:
 1) automated trading of spreads with paper trading
 2) gui to activate and deactive different trading algos and keep track of paper portfolio
 3) twitter sentiment 
 4) econmic models to predict market volatility

            
            
            
