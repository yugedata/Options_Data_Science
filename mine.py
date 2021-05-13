from sqlalchemy import create_engine
from td.client import TDClient
from datetime import datetime
from datetime import date
from td import exceptions
import pandas as pd
import sqlite3
import time
import credentials


TDSession = TDClient(
    client_id=credentials.client_id,
    redirect_uri='https://127.0.0.1',
    credentials_path=credentials.json_path
)

TDSession.login()


def history(symbol):
    quotes = TDClient.get_price_history(TDSession, symbol=symbol, period_type='day',
                                        period=1, frequency_type='minute', frequency=1,
                                        extended_hours=False)
    # start_date = 1606086000000, end_date = 1606341600000,

    return quotes


def make_sqlite_table(table_name):
    engine = create_engine('sqlite:///Data/Options.db', echo=False)
    table_columns = pd.DataFrame(columns=columns_wanted)
    table_columns.to_sql(table_name, con=engine)

    return 0


def add_rows(clean_data, table_name):
    global file_date
    engine = create_engine(f'sqlite:///Data/Options_{file_date}.db', echo=False)
    clean_data.to_sql(table_name, con=engine, if_exists='append', index_label='index')

    return 0


def delete_row(table_name, column, argument):
    conn = sqlite3.connect('Options.db')
    con = conn.cursor()
    con.execute(f'DELETE FROM {table_name} WHERE {column}={argument}')
    conn.commit()
    conn.close()

    return 0


def delete_db_table(table_name):
    conn = sqlite3.connect('options.db')
    con = conn.cursor()
    con.execute(f'DROP TABLE {table_name}')
    conn.commit()
    conn.close()

    return 0


def show_db_table(puts_calls):
    conn = sqlite3.connect('options.db')
    con = conn.cursor()
    for row in con.execute(f'SELECT * FROM {puts_calls}'):
        print(row)
    conn.close()

    return 0


file_date = 0
to_date = 0

trade_days_2021 = {'jan': [4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 19, 20, 21, 22, 25, 26, 27, 28, 29],
                   'feb': [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 16, 17, 18, 19, 22, 23, 24, 25, 26],
                   'mar': [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 29, 30, 31],
                   'apr': [5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 26, 27, 28, 29, 30],
                   'may': [3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28],
                   'jun': [1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 28, 29, 30],
                   'jul': [1, 2, 6, 7, 8, 9, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 26, 27, 28, 29, 30],
                   'aug': [2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 30, 31],
                   'sep': [1, 2, 3, 7, 8, 9, 10, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 27, 28, 29, 30],
                   'oct': [1, 4, 5, 6, 7, 8, 12, 13, 14, 15, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29],
                   'nov': [1, 2, 3, 4, 5, 8, 9, 10, 12, 15, 16, 17, 18, 19, 22, 23, 24, 29, 30],
                   'dec': [1, 2, 3, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 20, 21, 22, 27, 28, 29, 30]}


opt_column_names = ['putCall', 'symbol', 'description', 'exchangeName', 'bid', 'ask', 'last', 'mark', 'bidSize',
                    'askSize', 'bidAskSize', 'lastSize', 'highPrice', 'lowPrice', 'openPrice', 'closePrice',
                    'totalVolume', 'tradeDate', 'tradeTimeInLong', 'quoteTimeInLong', 'netChange', 'volatility',
                    'delta', 'gamma', 'theta', 'vega', 'rho', 'openInterest', 'timeValue', 'theoreticalOptionValue',
                    'theoreticalVolatility', 'optionDeliverablesList', 'strikePrice', 'expirationDate',
                    'daysToExpiration',
                    'expirationType', 'lastTradingDay', 'multiplier', 'settlementType', 'deliverableNote',
                    'isIndexOption', 'percentChange', 'markChange', 'markPercentChange', 'mini', 'inTheMoney',
                    'nonStandard']

columns_unwanted = ['description', 'mark', 'bidSize', 'askSize', 'bidAskSize', 'lastSize', 'tradeDate',
                    'tradeTimeInLong', 'theoreticalOptionValue', 'optionDeliverablesList',
                    'expirationType', 'lastTradingDay', 'multiplier', 'settlementType', 'deliverableNote',
                    'isIndexOption', 'markChange', 'markPercentChange', 'nonStandard', 'inTheMoney', 'mini']

columns_wanted = ['putCall', 'symbol', 'exchangeName', 'bid', 'ask', 'last', 'highPrice',
                  'lowPrice', 'openPrice', 'closePrice', 'totalVolume', 'quoteTimeInLong',
                  'netChange', 'volatility', 'delta', 'gamma', 'theta', 'vega', 'rho', 'openInterest', 'timeValue',
                  'theoreticalVolatility', 'strikePrice', 'expirationDate', 'daysToExpiration', 'percentChange']

stocks = ['AAPL', 'AMD', 'AMZN', 'TSLA', 'MU', 'NVDA', 'GOOG', 'ROKU', 'NFLX', 'FB', 'CMG', 'GME', 'MCD', 'SNAP']

''' ~4700 stocks to add to stock list  
         
         ['A', 'AA', 'AACQ', 'AAIC', 'AAL', 'AAN', 'AAOI', 'AAON', 'AAP', 'AAPL', 'AAT', 'AAU', 'AAWW', 'AAXJ', 'AB', 'ABB',
          'ABBV', 'ABC', 'ABCB', 'ABEO', 'ABEV', 'ABG', 'ABIO', 'ABM', 'ABMD', 'ABNB', 'ABR', 'ABT', 'ABTX', 'ABUS', 'ACA',
          'ACAD', 'ACB', 'ACC', 'ACCD', 'ACCO', 'ACEL', 'ACER', 'ACES', 'ACEV', 'ACGL', 'ACH', 'ACHC', 'ACI', 'ACIU', 'ACIW',
          'ACLS', 'ACM', 'ACMR', 'ACN', 'ACOR', 'ACR', 'ACRE', 'ACRS', 'ACRX', 'ACTC', 'ACTG', 'ACWI', 'ACWV', 'ACWX', 'ADAP',
          'ADBE', 'ADC', 'ADCT', 'ADI', 'ADM', 'ADMA', 'ADMP', 'ADMS', 'ADN', 'ADNT', 'ADP', 'ADPT', 'ADS', 'ADSK', 'ADT', 'ADTN',
          'ADTX', 'ADUS', 'ADV', 'ADVM', 'AEE', 'AEG', 'AEGN', 'AEIS', 'AEL', 'AEM', 'AEO', 'AEP', 'AER', 'AERI', 'AES', 'AEZS',
          'AFG', 'AFI', 'AFL', 'AFMD', 'AFRM', 'AFTY', 'AFYA', 'AG', 'AGC', 'AGCB', 'AGCO', 'AGEN', 'AGFS', 'AGG', 'AGI', 'AGIO',
          'AGLE', 'AGM', 'AGNC', 'AGO', 'AGQ', 'AGR', 'AGRO', 'AGRX', 'AGS', 'AGTC', 'AGX', 'AGYS', 'AHC', 'AHCO', 'AHH', 'AHT',
          'AI', 'AIA', 'AIG', 'AIMC', 'AIN', 'AINV', 'AIR', 'AIRC', 'AIRG', 'AIT', 'AIV', 'AIZ', 'AJAX', 'AJG', 'AJRD', 'AJX', 'AKAM',
          'AKBA', 'AKR', 'AKRO', 'AKTS', 'AL', 'ALB', 'ALBO', 'ALC', 'ALDX', 'ALE', 'ALEC', 'ALEX', 'ALFA', 'ALG', 'ALGM', 'ALGN', 'ALGT',
          'ALK', 'ALKS', 'ALL', 'ALLE', 'ALLK', 'ALLO', 'ALLT', 'ALLY', 'ALNY', 'ALPN', 'ALRM', 'ALSK', 'ALSN', 'ALT', 'ALTG', 'ALTO', 'ALTR',
          'ALTU', 'ALV', 'ALVR', 'ALXN', 'ALXO', 'AM', 'AMAT', 'AMBA', 'AMBC', 'AMC', 'AMCR', 'AMCX', 'AMD', 'AME', 'AMED', 'AMG',
          'AMGN', 'AMH', 'AMJ', 'AMKR', 'AMLP', 'AMN', 'AMNB', 'AMOT', 'AMP', 'AMPE', 'AMPH', 'AMPY', 'AMR', 'AMRC', 'AMRN', 'AMRS',
          'AMRX', 'AMSC', 'AMSF', 'AMSWA', 'AMT', 'AMTX', 'AMWD', 'AMWL', 'AMX', 'AMZA', 'AMZN', 'AN', 'ANAB', 'ANAT', 'ANDE', 'ANET',
          'ANF', 'ANGI', 'ANGL', 'ANGO', 'ANH', 'ANIK', 'ANIP', 'ANSS', 'ANTE', 'ANTM', 'AON', 'AOS', 'AOSL', 'AOUT', 'AP', 'APA', 'APAM',
          'APD', 'APEI', 'APEN', 'APEX', 'APG', 'APH', 'APHA', 'API', 'APLE', 'APLS', 'APLT', 'APO', 'APOG', 'APPF', 'APPH', 'APPN', 'APPS',
          'APRE', 'APRN', 'APT', 'APTO', 'APTS', 'APTV', 'APTX', 'APXT', 'APYX', 'AQB', 'AQMS', 'AQN', 'AQST', 'AQUA', 'AR', 'ARAV', 'ARAY',
          'ARC', 'ARCB', 'ARCC', 'ARCH', 'ARCO', 'ARCT', 'ARD', 'ARDX', 'ARE', 'ARES', 'ARGT', 'ARGX', 'ARI', 'ARKF', 'ARKG', 'ARKK', 'ARKQ',
          'ARKW', 'ARLO', 'ARLP', 'ARMK', 'ARNA', 'ARNC', 'AROC', 'AROW', 'ARQT', 'ARR', 'ARRY', 'ARVN', 'ARW', 'ARWR', 'ARYA', 'ASA', 'ASAN',
          'ASB', 'ASC', 'ASGN', 'ASH', 'ASHR', 'ASHS', 'ASIX', 'ASMB', 'ASML', 'ASNAQ', 'ASND', 'ASO', 'ASPN', 'ASPS', 'ASR', 'ASRT', 'ASRV',
          'ASTE', 'ASUR', 'ASYS', 'AT', 'ATAC', 'ATAX', 'ATCO', 'ATEC', 'ATEN', 'ATEX', 'ATGE', 'ATH', 'ATHM', 'ATHX', 'ATI', 'ATKR', 'ATLC',
          'ATNF', 'ATNI', 'ATNM', 'ATNX', 'ATO', 'ATOM', 'ATOS', 'ATR', 'ATRA', 'ATRC', 'ATRO', 'ATRS', 'ATSG', 'ATUS', 'ATVI', 'AU', 'AUB',
          'AUDC', 'AUMN', 'AUPH', 'AUTO', 'AUY', 'AVA', 'AVAV', 'AVB', 'AVCT', 'AVD', 'AVDL', 'AVEO', 'AVGO', 'AVID', 'AVIR', 'AVLR', 'AVNS',
          'AVNT', 'AVRO', 'AVT', 'AVTR', 'AVXL', 'AVY', 'AVYA', 'AWAY', 'AWH', 'AWI', 'AWK', 'AWR', 'AWRE', 'AX', 'AXAS', 'AXDX', 'AXGN', 'AXL',
          'AXNX', 'AXON', 'AXP', 'AXS', 'AXSM', 'AXTA', 'AXTI', 'AXU', 'AY', 'AYI', 'AYRO', 'AYX', 'AZEK', 'AZN', 'AZO', 'AZPN', 'AZUL', 'AZZ',
          'B', 'BA', 'BABA', 'BAC', 'BAH', 'BAL', 'BALY', 'BAM', 'BANC', 'BAND', 'BANF', 'BANR', 'BAP', 'BATRA', 'BATRK', 'BAX', 'BB', 'BBAR',
          'BBBY', 'BBCA', 'BBD', 'BBDC', 'BBEU', 'BBH', 'BBIG', 'BBIO', 'BBL', 'BBSI', 'BBU', 'BBVA', 'BBW', 'BBY', 'BC', 'BCBP', 'BCC', 'BCDA',
          'BCE', 'BCEI', 'BCEL', 'BCI', 'BCLI', 'BCO', 'BCOR', 'BCOV', 'BCPC', 'BCRX', 'BCS', 'BCSF', 'BDC', 'BDN', 'BDSI', 'BDTX', 'BDX', 'BE',
          'BEAM', 'BECN', 'BEEM', 'BEKE', 'BELFB', 'BEN', 'BEP', 'BEPC', 'BERY', 'BEST', 'BETZ', 'BFAM', 'BFI', 'BFLY', 'BFOR', 'BFT', 'BG',
          'BGCP', 'BGFV', 'BGNE', 'BGS', 'BHC', 'BHE', 'BHF', 'BHLB', 'BHP', 'BHR', 'BHVN', 'BIB', 'BIDU', 'BIG', 'BIGC', 'BIIB', 'BIL', 'BILI',
          'BILL', 'BIO', 'BIOC', 'BIP', 'BIS', 'BIV', 'BJ', 'BJK', 'BJRI', 'BK', 'BKCC', 'BKD', 'BKE', 'BKEP', 'BKF', 'BKH', 'BKI', 'BKLN', 'BKNG',
          'BKR', 'BKU', 'BKYI', 'BL', 'BLCN', 'BLD', 'BLDP', 'BLDR', 'BLFS', 'BLI', 'BLK', 'BLKB', 'BLL', 'BLMN', 'BLNK', 'BLOK', 'BLU', 'BLUE',
          'BLV', 'BLX', 'BMA', 'BMBL', 'BMI', 'BMO', 'BMRA', 'BMRN', 'BMTC', 'BMY', 'BND', 'BNDX', 'BNED', 'BNFT', 'BNGO', 'BNL', 'BNO', 'BNS',
          'BNTX', 'BOCH', 'BOH', 'BOIL', 'BOKF', 'BOND', 'BOOM', 'BOOT', 'BOTZ', 'BOX', 'BP', 'BPFH', 'BPMC', 'BPMP', 'BPOP', 'BPT', 'BPY', 'BPYU',
          'BQ', 'BR', 'BRBR', 'BRC', 'BRF', 'BRFS', 'BRG', 'BRK.B', 'BRKL', 'BRKR', 'BRKS', 'BRMK', 'BRO', 'BRP', 'BRX', 'BRY', 'BRZU', 'BSAC',
          'BSBR', 'BSET', 'BSGM', 'BSIG', 'BSM', 'BSMX', 'BSQR', 'BSRR', 'BSV', 'BSX', 'BSY', 'BTAI', 'BTBT', 'BTEGF', 'BTG', 'BTI', 'BTN', 'BTNB',
          'BTU', 'BTWN', 'BUD', 'BUG', 'BUR', 'BURL', 'BUSE', 'BV', 'BVN', 'BW', 'BWA', 'BWX', 'BWXT', 'BX', 'BXC', 'BXMT', 'BXP', 'BXRX', 'BXS',
          'BYD', 'BYND', 'BYSI', 'BZH', 'BZQ', 'BZUN', 'C', 'CAAP', 'CAAS', 'CABA', 'CAC', 'CACC', 'CACI', 'CADE', 'CAE', 'CAF', 'CAG', 'CAH', 'CAI',
          'CAJ', 'CAKE', 'CAL', 'CALA', 'CALM', 'CALX', 'CAMP', 'CAMT', 'CAN', 'CANE', 'CAPA', 'CAPL', 'CAPR', 'CAR', 'CARA', 'CARG', 'CARR', 'CARS',
          'CASA', 'CASH', 'CASS', 'CASY', 'CAT', 'CATB', 'CATM', 'CATO', 'CATY', 'CB', 'CBAT', 'CBAY', 'CBB', 'CBD', 'CBIO', 'CBLAQ', 'CBOE', 'CBPO',
          'CBRE', 'CBRL', 'CBSH', 'CBT', 'CBU', 'CBZ', 'CC', 'CCAC', 'CCEP', 'CCI', 'CCIV', 'CCJ', 'CCK', 'CCL', 'CCLP', 'CCMP', 'CCNE', 'CCO', 'CCOI',
          'CCRN', 'CCS', 'CCX', 'CCXI', 'CD', 'CDAY', 'CDE', 'CDEV', 'CDK', 'CDLX', 'CDMO', 'CDNA', 'CDNS', 'CDR', 'CDTX', 'CDW', 'CDXC', 'CDXS',
          'CDZI', 'CE', 'CECE', 'CEIX', 'CELH', 'CELJF', 'CEMB', 'CEMI', 'CENT', 'CENTA', 'CENX', 'CEQP', 'CERC', 'CERN', 'CERS', 'CERT', 'CEVA',
          'CEW', 'CF', 'CFA', 'CFAC', 'CFFN', 'CFG', 'CFII', 'CFR', 'CFRX', 'CFX', 'CG', 'CGBD', 'CGC', 'CGEN', 'CGNT', 'CGNX', 'CGRO', 'CHAD',
          'CHAU', 'CHCO', 'CHD', 'CHDN', 'CHE', 'CHEF', 'CHGG', 'CHH', 'CHIC', 'CHIQ', 'CHIX', 'CHK', 'CHKP', 'CHMA', 'CHNG', 'CHPT', 'CHRS',
          'CHRW', 'CHS', 'CHT', 'CHTR', 'CHUY', 'CHWY', 'CHX', 'CI', 'CIA', 'CIB', 'CIBR', 'CIEN', 'CIG', 'CIIC', 'CIM', 'CINF', 'CIO', 'CIR',
          'CIT', 'CIVB', 'CKH', 'CKPT', 'CL', 'CLA', 'CLAR', 'CLB', 'CLBK', 'CLBS', 'CLDR', 'CLDT', 'CLDX', 'CLF', 'CLFD', 'CLGX', 'CLH', 'CLI',
          'CLII', 'CLIR', 'CLLS', 'CLMT', 'CLNC', 'CLNE', 'CLNY', 'CLOU', 'CLOV', 'CLR', 'CLS', 'CLSD', 'CLSK', 'CLSN', 'CLVR', 'CLVS', 'CLVT',
          'CLW', 'CLX', 'CM', 'CMA', 'CMC', 'CMCM', 'CMCO', 'CMCSA', 'CMD', 'CME', 'CMG', 'CMI', 'CMLF', 'CMO', 'CMP', 'CMPR', 'CMPS', 'CMRE',
          'CMRX', 'CMS', 'CMTL', 'CNA', 'CNC', 'CNCE', 'CNDT', 'CNET', 'CNHI', 'CNI', 'CNK', 'CNMD', 'CNNE', 'CNO', 'CNOB', 'CNP', 'CNQ', 'CNR',
          'CNS', 'CNSL', 'CNST', 'CNTY', 'CNX', 'CNXC', 'CNXN', 'CNXT', 'CNYA', 'CO', 'CODI', 'CODX', 'COF', 'COG', 'COHR', 'COHU', 'COLB', 'COLD',
          'COLL', 'COLM', 'COMM', 'COMS', 'CONE', 'CONN', 'COO', 'COOP', 'COP', 'COR', 'CORE', 'CORN', 'CORR', 'CORT', 'COST', 'COTY', 'COUP', 'COW',
          'COWN', 'COWZ', 'CP', 'CPA', 'CPB', 'CPE', 'CPER', 'CPF', 'CPG', 'CPK', 'CPLG', 'CPLP', 'CPRI', 'CPRT', 'CPRX', 'CPS', 'CPSH', 'CPSI',
          'CPSS', 'CPST', 'CPT', 'CPTA', 'CQP', 'CQQQ', 'CR', 'CRAI', 'CRBP', 'CRC', 'CRDF', 'CREE', 'CRESY', 'CRH', 'CRI', 'CRIS', 'CRK', 'CRL',
          'CRM', 'CRMD', 'CRMT', 'CRNC', 'CRNT', 'CROC', 'CRON', 'CROX', 'CRS', 'CRSA', 'CRSP', 'CRSR', 'CRTO', 'CRTX', 'CRUS', 'CRVL', 'CRVS',
          'CRWD', 'CRWS', 'CRY', 'CS', 'CSCO', 'CSD', 'CSGP', 'CSGS', 'CSII', 'CSIQ', 'CSL', 'CSLT', 'CSOD', 'CSPR', 'CSR', 'CSTE', 'CSTL', 'CSTM',
          'CSU', 'CSV', 'CSWC', 'CSX', 'CTAS', 'CTB', 'CTBI', 'CTG', 'CTIC', 'CTLT', 'CTMX', 'CTRE', 'CTRN', 'CTS', 'CTSH', 'CTSO', 'CTT', 'CTVA',
          'CTXS', 'CUB', 'CUBE', 'CUBI', 'CUE', 'CUK', 'CULP', 'CURE', 'CURI', 'CURO', 'CUTR', 'CUZ', 'CVA', 'CVAC', 'CVBF', 'CVCO', 'CVCY', 'CVE',
          'CVEO', 'CVET', 'CVGI', 'CVGW', 'CVI', 'CVLG', 'CVLT', 'CVM', 'CVNA', 'CVS', 'CVX', 'CVY', 'CW', 'CWB', 'CWCO', 'CWEB', 'CWEN', 'CWH',
          'CWI', 'CWK', 'CWST', 'CWT', 'CX', 'CXDC', 'CXP', 'CXW', 'CYB', 'CYBE', 'CYBR', 'CYCN', 'CYD', 'CYH', 'CYRX', 'CYTK', 'CZNC', 'CZR',
          'CZZ', 'D', 'DAC', 'DADA', 'DAKT', 'DAL', 'DAN', 'DAO', 'DAR', 'DASH', 'DB', 'DBA', 'DBB', 'DBC', 'DBD', 'DBE', 'DBEF', 'DBEU', 'DBI',
          'DBJP', 'DBO', 'DBP', 'DBS', 'DBV', 'DBVT', 'DBX', 'DCI', 'DCO', 'DCOM', 'DCP', 'DCPH', 'DCT', 'DD', 'DDD', 'DDG', 'DDM', 'DDOG',
          'DDS', 'DE', 'DEA', 'DECK', 'DEEP', 'DEI', 'DELL', 'DEM', 'DENN', 'DEO', 'DES', 'DESP', 'DFE', 'DFEN', 'DFH', 'DFIN', 'DFJ', 'DFS',
          'DG', 'DGICA', 'DGII', 'DGL', 'DGLY', 'DGNR', 'DGNS', 'DGRO', 'DGRW', 'DGS', 'DGX', 'DHC', 'DHI', 'DHR', 'DHT', 'DHX', 'DIA', 'DIG',
          'DIN', 'DIOD', 'DIS', 'DISCA', 'DISCK', 'DISH', 'DJP', 'DK', 'DKL', 'DKNG', 'DKS', 'DLB', 'DLHC', 'DLN', 'DLNG', 'DLR', 'DLS', 'DLTH',
          'DLTR', 'DLX', 'DM', 'DMAC', 'DMLP', 'DMRC', 'DMTK', 'DMYD', 'DNB', 'DNLI', 'DNMR', 'DNN', 'DNOW', 'DOC', 'DOCU', 'DOFSQ', 'DOG', 'DOMO',
          'DON', 'DOOR', 'DORM', 'DOV', 'DOW', 'DOX', 'DOYU', 'DPST', 'DPW', 'DPZ', 'DQ', 'DRD', 'DRE', 'DRH', 'DRI', 'DRIP', 'DRIV', 'DRN',
          'DRNA', 'DRQ', 'DRRX', 'DRV', 'DRVN', 'DS', 'DSKE', 'DSL', 'DSPG', 'DSX', 'DT', 'DTE', 'DTEA', 'DTEC', 'DTIL', 'DTN', 'DUG', 'DUK',
          'DUSL', 'DUST', 'DVA', 'DVAX', 'DVN', 'DVY', 'DWAS', 'DWX', 'DX', 'DXC', 'DXCM', 'DXD', 'DXJ', 'DXJS', 'DXLG', 'DXPE', 'DXYN', 'DY',
          'DYAI', 'DZSI', 'E', 'EA', 'EAF', 'EAR', 'EARS', 'EAT', 'EB', 'EBAY', 'EBC', 'EBF', 'EBIX', 'EBIZ', 'EBND', 'EBON', 'EBS', 'EBSB',
          'EC', 'ECH', 'ECHO', 'ECL', 'ECNS', 'ECOL', 'ECOM', 'ECON', 'ECPG', 'ED', 'EDAP', 'EDC', 'EDIT', 'EDIV', 'EDOC', 'EDU', 'EDV', 'EDZ',
          'EEFT', 'EEM', 'EEMV', 'EET', 'EEV', 'EEX', 'EFA', 'EFAV', 'EFC', 'EFG', 'EFSC', 'EFV', 'EFX', 'EFZ', 'EGAN', 'EGBN', 'EGHT', 'EGLE',
          'EGO', 'EGOV', 'EGP', 'EGRX', 'EGY', 'EH', 'EHC', 'EHTH', 'EIDO', 'EIG', 'EIGR', 'EINC', 'EIX', 'EKSO', 'EL', 'ELAN', 'ELD', 'ELF',
          'ELMD', 'ELOX', 'ELP', 'ELS', 'ELY', 'EMAN', 'EMB', 'EME', 'EMKR', 'EMLC', 'EMLP', 'EMN', 'EMQQ', 'EMR', 'EMXC', 'ENB', 'ENBL',
          'ENDP', 'ENG', 'ENIA', 'ENIC', 'ENLC', 'ENLV', 'ENPH', 'ENR', 'ENS', 'ENSG', 'ENTA', 'ENTG', 'ENV', 'ENVA', 'ENZ', 'ENZL', 'EOG',
          'EOLS', 'EOSE', 'EPAC', 'EPAM', 'EPAY', 'EPC', 'EPD', 'EPI', 'EPM', 'EPP', 'EPR', 'EPRT', 'EPV', 'EPZM', 'EQC', 'EQH', 'EQIX',
          'EQNR', 'EQOS', 'EQR', 'EQT', 'EQX', 'ERF', 'ERIC', 'ERIE', 'ERII', 'ERJ', 'ERX', 'ERY', 'ES', 'ESCA', 'ESE', 'ESGC', 'ESGE',
          'ESGU', 'ESI', 'ESNT', 'ESPO', 'ESPR', 'ESRT', 'ESS', 'ESSC', 'ESTA', 'ESTC', 'ET', 'ETH', 'ETM', 'ETN', 'ETNB', 'ETR', 'ETRN',
          'ETSY', 'ETWO', 'EUFN', 'EUM', 'EUO', 'EURL', 'EURN', 'EVA', 'EVBG', 'EVC', 'EVER', 'EVFM', 'EVGN', 'EVH', 'EVLO', 'EVOK', 'EVOP',
          'EVR', 'EVRG', 'EVRI', 'EVTC', 'EW', 'EWA', 'EWBC', 'EWC', 'EWD', 'EWG', 'EWH', 'EWI', 'EWJ', 'EWK', 'EWL', 'EWM', 'EWN', 'EWP',
          'EWQ', 'EWS', 'EWT', 'EWU', 'EWV', 'EWW', 'EWX', 'EWY', 'EWZ', 'EXAS', 'EXC', 'EXEL', 'EXK', 'EXLS', 'EXP', 'EXPC', 'EXPD', 'EXPE',
          'EXPI', 'EXPO', 'EXPR', 'EXR', 'EXTN', 'EXTR', 'EYE', 'EYEN', 'EYPT', 'EZA', 'EZJ', 'EZPW', 'EZU', 'F', 'FAF', 'FAII', 'FALN',
          'FAN', 'FANG', 'FANH', 'FARO', 'FAS', 'FAST', 'FATE', 'FAZ', 'FB', 'FBC', 'FBHS', 'FBIZ', 'FBK', 'FBNC', 'FBP', 'FBT', 'FC', 'FCA',
          'FCAC', 'FCBC', 'FCEL', 'FCF', 'FCFS', 'FCG', 'FCN', 'FCOM', 'FCPT', 'FCRD', 'FCX', 'FDIS', 'FDL', 'FDLO', 'FDN', 'FDP', 'FDS',
          'FDUS', 'FDX', 'FE', 'FELE', 'FEM', 'FENC', 'FENG', 'FENY', 'FEP', 'FET', 'FEX', 'FEYE', 'FEZ', 'FF', 'FFBC', 'FFG', 'FFIC', 'FFIN',
          'FFIV', 'FFNW', 'FFTY', 'FGD', 'FGEN', 'FHB', 'FHI', 'FHLC', 'FHN', 'FI', 'FIBK', 'FICO', 'FIDU', 'FIII', 'FINV', 'FINX', 'FIS',
          'FISI', 'FISV', 'FITB', 'FIVE', 'FIVG', 'FIVN', 'FIW', 'FIX', 'FIXX', 'FIZZ', 'FL', 'FLDM', 'FLEX', 'FLGT', 'FLIC', 'FLIR', 'FLMN',
          'FLNT', 'FLO', 'FLOW', 'FLR', 'FLS', 'FLT', 'FLWS', 'FLXN', 'FLY', 'FM', 'FMAT', 'FMBI', 'FMC', 'FMNB', 'FMS', 'FMX', 'FN', 'FNB',
          'FNCL', 'FND', 'FNDA', 'FNDE', 'FNDF', 'FNDX', 'FNF', 'FNGS', 'FNHC', 'FNKO', 'FNLC', 'FNV', 'FOCS', 'FOE', 'FOLD', 'FOR', 'FORM',
          'FORR', 'FOSL', 'FOUR', 'FOX', 'FOXA', 'FOXF', 'FPAC', 'FPE', 'FPH', 'FPI', 'FPRX', 'FPX', 'FR', 'FRAK', 'FRBK', 'FRC', 'FREE',
          'FREL', 'FREQ', 'FRG', 'FRGI', 'FRHC', 'FRME', 'FRO', 'FROG', 'FRPT', 'FRSX', 'FRT', 'FRTA', 'FRX', 'FSK', 'FSKR', 'FSLR', 'FSLY',
          'FSM', 'FSP', 'FSR', 'FSRV', 'FSS', 'FST', 'FSTA', 'FSTR', 'FTAG', 'FTAI', 'FTC', 'FTCH', 'FTCS', 'FTDR', 'FTEC', 'FTEK', 'FTFT',
          'FTGC', 'FTI', 'FTK', 'FTNT', 'FTOC', 'FTRCQ', 'FTRI', 'FTS', 'FTV', 'FUBO', 'FUL', 'FULT', 'FUN', 'FUSE', 'FUSN', 'FUTU', 'FUTY',
          'FUV', 'FV', 'FVD', 'FVRR', 'FWONA', 'FWONK', 'FWRD', 'FXA', 'FXB', 'FXC', 'FXD', 'FXE', 'FXF', 'FXG', 'FXH', 'FXI', 'FXL', 'FXN',
          'FXO', 'FXP', 'FXR', 'FXU', 'FXY', 'FXZ', 'G', 'GABC', 'GAIA', 'GAIN', 'GALT', 'GAMR', 'GAN', 'GASS', 'GATX', 'GAU', 'GB', 'GBCI',
          'GBDC', 'GBT', 'GBX', 'GCI', 'GCO', 'GCP', 'GD', 'GDDY', 'GDEN', 'GDOT', 'GDRX', 'GDS', 'GDX', 'GDXJ', 'GDYN', 'GE', 'GEF', 'GEL',
          'GEM', 'GEN', 'GENE', 'GEO', 'GEOS', 'GERM', 'GERN', 'GES', 'GEVO', 'GFF', 'GFI', 'GFL', 'GFN', 'GGAL', 'GGB', 'GGG', 'GH', 'GHL',
          'GHM', 'GHYB', 'GIB', 'GIFI', 'GIGB', 'GIII', 'GIK', 'GIL', 'GILD', 'GILT', 'GINN', 'GIS', 'GIX', 'GKOS', 'GL', 'GLAD', 'GLCN',
          'GLD', 'GLDD', 'GLIN', 'GLL', 'GLMD', 'GLNG', 'GLOB', 'GLOG', 'GLOP', 'GLP', 'GLPG', 'GLPI', 'GLRE', 'GLT', 'GLUU', 'GLW', 'GLYC',
          'GM', 'GMAB', 'GMBL', 'GMDA', 'GME', 'GMED', 'GMF', 'GMLP', 'GMRE', 'GMS', 'GMTX', 'GNCA', 'GNE', 'GNK', 'GNL', 'GNLN', 'GNMK',
          'GNOG', 'GNOM', 'GNPX', 'GNR', 'GNRC', 'GNSS', 'GNTX', 'GNUS', 'GNW', 'GO', 'GOCO', 'GOEV', 'GOEX', 'GOGL', 'GOGO', 'GOL', 'GOLD',
          'GOLF', 'GOOD', 'GOOG', 'GOOGL', 'GOOS', 'GORO', 'GOSS', 'GOVT', 'GP', 'GPC', 'GPI', 'GPK', 'GPL', 'GPMT', 'GPN', 'GPORQ', 'GPP',
          'GPRE', 'GPRK', 'GPRO', 'GPS', 'GPX', 'GRA', 'GRBK', 'GRC', 'GREK', 'GRFS', 'GRMN', 'GROW', 'GRPN', 'GRTS', 'GRUB', 'GRWG', 'GS',
          'GSAH', 'GSAT', 'GSBC', 'GSEW', 'GSG', 'GSHD', 'GSIE', 'GSIT', 'GSK', 'GSKY', 'GSLC', 'GSM', 'GSS', 'GSUM', 'GSX', 'GT', 'GTE',
          'GTES', 'GTHX', 'GTIM', 'GTLS', 'GTN', 'GTS', 'GTT', 'GTXMQ', 'GTY', 'GUNR', 'GURU', 'GUSH', 'GVA', 'GVI', 'GVIP', 'GWB', 'GWPH',
          'GWRE', 'GWW', 'GWX', 'GXC', 'GXG', 'GXGX', 'GYLD', 'H', 'HA', 'HACK', 'HAE', 'HAFC', 'HAIN', 'HAL', 'HALL', 'HALO', 'HARP', 'HAS',
          'HASI', 'HAYN', 'HBAN', 'HBI', 'HBIO', 'HBM', 'HBNC', 'HBP', 'HCA', 'HCAT', 'HCC', 'HCCI', 'HCHC', 'HCI', 'HCKT', 'HCSG', 'HD',
          'HDB', 'HDGE', 'HDSN', 'HDV', 'HE', 'HEAR', 'HEDJ', 'HEES', 'HEFA', 'HEI', 'HELE', 'HEP', 'HEPA', 'HERO', 'HES', 'HESM', 'HEWG',
          'HEWJ', 'HEXO', 'HEZU', 'HFC', 'HFWA', 'HGEN', 'HGV', 'HHC', 'HI', 'HIBB', 'HIBS', 'HIG', 'HII', 'HIL', 'HIMS', 'HIMX', 'HIW',
          'HL', 'HLF', 'HLI', 'HLIO', 'HLIT', 'HLNE', 'HLT', 'HLX', 'HMC', 'HMHC', 'HMN', 'HMST', 'HMSY', 'HMTV', 'HMY', 'HNGR', 'HNI',
          'HNP', 'HOFT', 'HOG', 'HOL', 'HOLI', 'HOLX', 'HOMB', 'HOME', 'HOMZ', 'HON', 'HOOK', 'HOPE', 'HP', 'HPE', 'HPP', 'HPQ', 'HPR',
          'HQY', 'HR', 'HRB', 'HRC', 'HRI', 'HRL', 'HRMY', 'HROW', 'HRTG', 'HRTX', 'HRZN', 'HSBC', 'HSC', 'HSIC', 'HSII', 'HST', 'HSTM',
          'HSY', 'HT', 'HTA', 'HTBI', 'HTBK', 'HTBX', 'HTGC', 'HTGM', 'HTH', 'HTHT', 'HTLD', 'HTLF', 'HTZGQ', 'HUBB', 'HUBG', 'HUBS', 'HUGE',
          'HUM', 'HUN', 'HURN', 'HUYA', 'HVT', 'HWC', 'HWCC', 'HWKN', 'HWM', 'HXL', 'HY', 'HYBB', 'HYD', 'HYFM', 'HYG', 'HYGH', 'HYLB',
          'HYLD', 'HYLN', 'HYMB', 'HYMC', 'HYRE', 'HYS', 'HYXU', 'HZN', 'HZNP', 'HZO', 'IAA', 'IAC', 'IAG', 'IAI', 'IART', 'IAT', 'IAU',
          'IBB', 'IBCP', 'IBIO', 'IBKR', 'IBM', 'IBN', 'IBOC', 'IBP', 'IBTX', 'IBUY', 'ICAD', 'ICE', 'ICF', 'ICFI', 'ICHR', 'ICLK', 'ICLN',
          'ICLR', 'ICMB', 'ICON', 'ICPT', 'ICUI', 'ICVT', 'IDA', 'IDCC', 'IDEX', 'IDN', 'IDNA', 'IDRA', 'IDRV', 'IDT', 'IDU', 'IDV', 'IDXX',
          'IDYA', 'IEA', 'IEF', 'IEFA', 'IEI', 'IEMG', 'IEO', 'IEP', 'IEUR', 'IEV', 'IEX', 'IEZ', 'IFF', 'IFGL', 'IFN', 'IFRX', 'IGC', 'IGE',
          'IGF', 'IGIB', 'IGLB', 'IGM', 'IGMS', 'IGN', 'IGOV', 'IGSB', 'IGT', 'IGV', 'IHAK', 'IHDG', 'IHE', 'IHF', 'IHI', 'IHRT', 'IHY', 'IIIN',
          'IIIV', 'IIN', 'IIPR', 'IIVI', 'IJH', 'IJJ', 'IJK', 'IJR', 'IJS', 'IJT', 'ILF', 'ILMN', 'ILPT', 'IMAX', 'IMGN', 'IMH', 'IMKTA', 'IMMR',
          'IMO', 'IMOS', 'IMUX', 'IMV', 'IMVT', 'INCY', 'INDA', 'INDB', 'INDL', 'INDY', 'INFI', 'INFN', 'INFO', 'INFY', 'ING', 'INGN', 'INGR',
          'INMD', 'INN', 'INO', 'INOD', 'INOV', 'INSG', 'INSM', 'INSP', 'INSW', 'INT', 'INTC', 'INTEQ', 'INTF', 'INTU', 'INVA', 'INVE', 'INVH',
          'IO', 'IONS', 'IOO', 'IOSP', 'IOVA', 'IP', 'IPAR', 'IPAY', 'IPFF', 'IPG', 'IPGP', 'IPHI', 'IPI', 'IPO', 'IPOD', 'IPOE', 'IPOF', 'IPV',
          'IQ', 'IQDF', 'IQLT', 'IQV', 'IR', 'IRBO', 'IRBT', 'IRDM', 'IRM', 'IRT', 'IRTC', 'IRWD', 'ISBC', 'ISEE', 'ISIG', 'ISRA', 'ISRG', 'IT',
          'ITA', 'ITB', 'ITCI', 'ITEQ', 'ITGR', 'ITI', 'ITM', 'ITOT', 'ITP', 'ITRI', 'ITRN', 'ITT', 'ITUB', 'ITW', 'IUSB', 'IUSG', 'IUSV', 'IVAC',
          'IVC', 'IVE', 'IVLU', 'IVOL', 'IVR', 'IVV', 'IVW', 'IVZ', 'IWB', 'IWC', 'IWD', 'IWF', 'IWM', 'IWN', 'IWO', 'IWP', 'IWR', 'IWS', 'IWV',
          'IXC', 'IXJ', 'IXN', 'IXP', 'IXUS', 'IYE', 'IYF', 'IYG', 'IYH', 'IYJ', 'IYM', 'IYR', 'IYT', 'IYW', 'IYZ', 'IZEA', 'J', 'JACK', 'JAGX',
          'JAMF', 'JAX', 'JAZZ', 'JBGS', 'JBHT', 'JBL', 'JBLU', 'JBSS', 'JBT', 'JCI', 'JCOM', 'JD', 'JDST', 'JE', 'JEF', 'JELD', 'JETS', 'JG',
          'JHG', 'JIH', 'JILL', 'JJC', 'JJG', 'JJSF', 'JKHY', 'JKS', 'JLL', 'JMIA', 'JNCE', 'JNJ', 'JNK', 'JNPR', 'JNUG', 'JO', 'JOBS', 'JOE',
          'JOET', 'JP', 'JPEM', 'JPIN', 'JPM', 'JPUS', 'JRVR', 'JUST', 'JWN', 'JWS', 'JYNT', 'K', 'KAI', 'KALA', 'KALU', 'KALV', 'KAMN', 'KAR',
          'KARS', 'KB', 'KBA', 'KBAL', 'KBE', 'KBH', 'KBR', 'KBWB', 'KC', 'KCE', 'KDMN', 'KDNY', 'KDP', 'KE', 'KELYA', 'KEP', 'KERN', 'KEX', 'KEY',
          'KEYS', 'KFRC', 'KFY', 'KGC', 'KHC', 'KIDS', 'KIE', 'KIM', 'KIN', 'KIRK', 'KKR', 'KL', 'KLAC', 'KLDO', 'KLIC', 'KLR', 'KMB', 'KMDA',
          'KMI', 'KMPH', 'KMPR', 'KMT', 'KMX', 'KN', 'KNDI', 'KNL', 'KNOP', 'KNSA', 'KNSL', 'KNX', 'KO', 'KOD', 'KODK', 'KOF', 'KOLD', 'KOP',
          'KOPN', 'KORU', 'KOS', 'KPTI', 'KR', 'KRA', 'KRC', 'KRE', 'KREF', 'KRG', 'KRMD', 'KRNT', 'KRNY', 'KRO', 'KRON', 'KRP', 'KRTX', 'KRYS',
          'KSA', 'KSS', 'KSU', 'KT', 'KTB', 'KTCC', 'KTOS', 'KURA', 'KVHI', 'KW', 'KWEB', 'KWR', 'KXIN', 'KYN', 'KZIA', 'KZR', 'L', 'LABD',
          'LABU', 'LAC', 'LAD', 'LADR', 'LAKE', 'LAMR', 'LANC', 'LAND', 'LASR', 'LAUR', 'LAZ', 'LAZR', 'LB', 'LBAI', 'LBJ', 'LBRDA', 'LBRDK',
          'LBRT', 'LBTYA', 'LBTYK', 'LC', 'LCI', 'LCII', 'LCNB', 'LCTX', 'LCUT', 'LDEM', 'LDL', 'LDOS', 'LE', 'LEA', 'LEAF', 'LECO', 'LEE',
          'LEG', 'LEGH', 'LEGN', 'LEJU', 'LEMB', 'LEN', 'LESL', 'LEU', 'LEVI', 'LFC', 'LFMD', 'LFT', 'LFUS', 'LFVN', 'LGIH', 'LGND', 'LH',
          'LHCG', 'LHX', 'LI', 'LII', 'LILA', 'LILAK', 'LIN', 'LINC', 'LIND', 'LIT', 'LITE', 'LIVN', 'LIVX', 'LJPC', 'LKFN', 'LKNCY', 'LKQ',
          'LL', 'LLNW', 'LLY', 'LMAT', 'LMND', 'LMNR', 'LMNX', 'LMRK', 'LMT', 'LNC', 'LNDC', 'LNG', 'LNN', 'LNT', 'LNTH', 'LOB', 'LOCO', 'LODE',
          'LOGI', 'LOMA', 'LOOP', 'LOPE', 'LORL', 'LOTZ', 'LOUP', 'LOV', 'LOVE', 'LOW', 'LPCN', 'LPG', 'LPI', 'LPL', 'LPLA', 'LPRO', 'LPSN',
          'LPX', 'LQD', 'LQDA', 'LQDH', 'LQDT', 'LRCX', 'LRGF', 'LRN', 'LSCC', 'LSI', 'LSPD', 'LSTR', 'LSXMA', 'LSXMK', 'LTC', 'LTHM', 'LTPZ',
          'LTRPA', 'LU', 'LULU', 'LUMN', 'LUNG', 'LUV', 'LVS', 'LW', 'LX', 'LXFR', 'LXP', 'LXRX', 'LXU', 'LYB', 'LYFT', 'LYG', 'LYTS', 'LYV',
          'LZB', 'M', 'MA', 'MAA', 'MAC', 'MACK', 'MAG', 'MAGA', 'MAGS', 'MAIN', 'MAN', 'MANH', 'MANT', 'MANU', 'MAR', 'MARA', 'MARK', 'MAS',
          'MASI', 'MAT', 'MATW', 'MATX', 'MAXN', 'MAXR', 'MBB', 'MBI', 'MBIO', 'MBT', 'MBUU', 'MBWM', 'MC', 'MCBC', 'MCD', 'MCF', 'MCFE', 'MCFT',
          'MCHI', 'MCHP', 'MCK', 'MCO', 'MCRB', 'MCRI', 'MCS', 'MCY', 'MD', 'MDB', 'MDC', 'MDCA', 'MDGL', 'MDIV', 'MDLA', 'MDLZ', 'MDP', 'MDRX',
          'MDT', 'MDU', 'MDXG', 'MDY', 'MDYG', 'MED', 'MEDP', 'MEG', 'MEI', 'MEIP', 'MELI', 'MEOH', 'MERC', 'MESA', 'MESO', 'MET', 'MEXX', 'MFA',
          'MFC', 'MFG', 'MFGP', 'MFIN', 'MG', 'MGA', 'MGC', 'MGEE', 'MGI', 'MGIC', 'MGK', 'MGLN', 'MGM', 'MGNI', 'MGNX', 'MGP', 'MGPI', 'MGRC',
          'MGTA', 'MGTX', 'MGV', 'MGY', 'MHK', 'MHLD', 'MHO', 'MIC', 'MIDD', 'MIDU', 'MIK', 'MILE', 'MIME', 'MIND', 'MIST', 'MITK', 'MITT', 'MIXT',
          'MJ', 'MKC', 'MKL', 'MKSI', 'MKTX', 'MLCO', 'MLHR', 'MLI', 'MLM', 'MLND', 'MLPA', 'MLPX', 'MLR', 'MMC', 'MMI', 'MMLP', 'MMM', 'MMP',
          'MMS', 'MMSI', 'MMYT', 'MN', 'MNKD', 'MNKKQ', 'MNOV', 'MNR', 'MNRL', 'MNRO', 'MNSO', 'MNST', 'MNTX', 'MO', 'MOAT', 'MOD', 'MODN', 'MODV',
          'MOGO', 'MOH', 'MOMO', 'MOO', 'MORN', 'MOS', 'MOV', 'MP', 'MPAA', 'MPC', 'MPLN', 'MPLX', 'MPW', 'MPWR', 'MPX', 'MRC', 'MRCC', 'MRCY',
          'MREO', 'MRK', 'MRKR', 'MRLN', 'MRNA', 'MRNS', 'MRO', 'MRSN', 'MRTN', 'MRTX', 'MRVI', 'MRVL', 'MS', 'MSA', 'MSB', 'MSCI', 'MSEX', 'MSFT',
          'MSGE', 'MSGN', 'MSGS', 'MSI', 'MSM', 'MSON', 'MSOS', 'MSP', 'MSTR', 'MT', 'MTA', 'MTB', 'MTCH', 'MTD', 'MTDR', 'MTEM', 'MTG', 'MTH', 'MTL',
          'MTLS', 'MTN', 'MTOR', 'MTRN', 'MTRX', 'MTSC', 'MTSI', 'MTUM', 'MTW', 'MTX', 'MTZ', 'MU', 'MUB', 'MUFG', 'MUNI', 'MUR', 'MUSA', 'MUX',
          'MVIS', 'MVO', 'MWA', 'MWK', 'MX', 'MXI', 'MXIM', 'MXL', 'MYE', 'MYGN', 'MYOV', 'MYRG', 'MYY', 'MZZ', 'NAIL', 'NAK', 'NANR', 'NARI',
          'NAT', 'NATI', 'NAV', 'NAVB', 'NAVI', 'NBEV', 'NBHC', 'NBIX', 'NBLX', 'NBR', 'NBRV', 'NBSE', 'NBTB', 'NCLH', 'NCMI', 'NCNO', 'NCR',
          'NCTY', 'NDAQ', 'NDLS', 'NDSN', 'NEE', 'NEM', 'NEO', 'NEOG', 'NEOS', 'NEP', 'NEPT', 'NERD', 'NERV', 'NESR', 'NET', 'NETL', 'NEU', 'NEW',
          'NEWR', 'NEWT', 'NEX', 'NFBK', 'NFE', 'NFG', 'NFLX', 'NG', 'NGA', 'NGAC', 'NGD', 'NGG', 'NGL', 'NGM', 'NGS', 'NGVC', 'NGVT', 'NH',
          'NHC', 'NHI', 'NHTC', 'NI', 'NIB', 'NICE', 'NINE', 'NIO', 'NIU', 'NJR', 'NK', 'NKE', 'NKLA', 'NKTR', 'NKTX', 'NL', 'NLOK', 'NLS', 'NLSN',
          'NLTX', 'NLY', 'NM', 'NMCI', 'NMFC', 'NMIH', 'NMM', 'NMR', 'NMRD', 'NMRK', 'NMTR', 'NNA', 'NNBR', 'NNDM', 'NNI', 'NNN', 'NNOX', 'NNVC',
          'NOA', 'NOAH', 'NOBL', 'NOC', 'NOG', 'NOK', 'NOMD', 'NOV', 'NOVA', 'NOVT', 'NOW', 'NP', 'NPA', 'NPO', 'NPTN', 'NR', 'NRBO', 'NRG', 'NRP',
          'NRT', 'NRZ', 'NS', 'NSA', 'NSC', 'NSCO', 'NSIT', 'NSP', 'NSSC', 'NSTG', 'NTAP', 'NTCO', 'NTCT', 'NTEC', 'NTES', 'NTGR', 'NTLA', 'NTNX',
          'NTP', 'NTR', 'NTRA', 'NTRS', 'NTUS', 'NTWK', 'NUAN', 'NUE', 'NUGT', 'NUS', 'NUVA', 'NVAX', 'NVCR', 'NVDA', 'NVEE', 'NVGS', 'NVMI', 'NVO',
          'NVRO', 'NVS', 'NVST', 'NVT', 'NVTA', 'NWBI', 'NWE', 'NWG', 'NWL', 'NWN', 'NWPX', 'NWS', 'NWSA', 'NX', 'NXE', 'NXGN', 'NXPI', 'NXRT', 'NXST',
          'NXTC', 'NXTD', 'NYCB', 'NYMT', 'NYMX', 'NYT', 'O', 'OAS', 'OBSV', 'OC', 'OCDX', 'OCFC', 'OCFT', 'OCGN', 'OCN', 'OCSI', 'OCSL', 'OCUL', 'OCX',
          'ODFL', 'ODP', 'ODT', 'OEC', 'OEF', 'OEG', 'OESX', 'OFC', 'OFG', 'OFIX', 'OGE', 'OGI', 'OGIG', 'OGS', 'OHI', 'OI', 'OIH', 'OII', 'OIS',
          'OKE', 'OKTA', 'OLED', 'OLLI', 'OLN', 'OLP', 'OMC', 'OMCL', 'OMER', 'OMEX', 'OMF', 'OMI', 'OMP', 'ON', 'ONB', 'ONCS', 'ONCT', 'ONEM',
          'ONLN', 'ONTO', 'OOMA', 'OPCH', 'OPEN', 'OPI', 'OPK', 'OPRA', 'OPRX', 'OPTT', 'OPY', 'OR', 'ORA', 'ORAN', 'ORBC', 'ORC', 'ORCC', 'ORCL',
          'ORGO', 'ORI', 'ORIC', 'ORLY', 'ORMP', 'ORN', 'ORTX', 'OSBC', 'OSG', 'OSH', 'OSIS', 'OSK', 'OSPN', 'OSTK', 'OSUR', 'OSW', 'OTEX', 'OTIC',
          'OTIS', 'OTRK', 'OTTR', 'OUNZ', 'OUSA', 'OUT', 'OVID', 'OVLH', 'OVT', 'OVV', 'OXFD', 'OXM', 'OXSQ', 'OXY', 'OZK', 'OZON', 'PAA', 'PAAS',
          'PACB', 'PACE', 'PACK', 'PACW', 'PAE', 'PAG', 'PAGP', 'PAGS', 'PAHC', 'PAM', 'PANW', 'PAR', 'PARR', 'PASG', 'PATK', 'PAVE', 'PAVM', 'PAX',
          'PAYA', 'PAYC', 'PAYS', 'PAYX', 'PB', 'PBA', 'PBCT', 'PBF', 'PBFX', 'PBH', 'PBI', 'PBPB', 'PBR', 'PBT', 'PBW', 'PBYI', 'PCAR', 'PCEF',
          'PCG', 'PCH', 'PCOM', 'PCRX', 'PCSB', 'PCTI', 'PCTY', 'PCY', 'PCYG', 'PCYO', 'PD', 'PDAC', 'PDBC', 'PDCE', 'PDCO', 'PDD', 'PDFS', 'PDM',
          'PDP', 'PDS', 'PEAK', 'PEB', 'PEBO', 'PEG', 'PEGA', 'PEI', 'PEJ', 'PEN', 'PENN', 'PEO', 'PEP', 'PERI', 'PERS', 'PESI', 'PETQ', 'PETS',
          'PEY', 'PEZ', 'PFBC', 'PFC', 'PFE', 'PFF', 'PFFA', 'PFG', 'PFGC', 'PFLT', 'PFM', 'PFMT', 'PFPT', 'PFS', 'PFSI', 'PFSW', 'PFX', 'PG', 'PGC',
          'PGEN', 'PGF', 'PGJ', 'PGNY', 'PGR', 'PGRE', 'PGTI', 'PGX', 'PH', 'PHAS', 'PHAT', 'PHB', 'PHG', 'PHIO', 'PHM', 'PHO', 'PHR', 'PHX', 'PI',
          'PICK', 'PICO', 'PID', 'PIE', 'PII', 'PIN', 'PINC', 'PING', 'PINS', 'PIPR', 'PIRS', 'PIXY', 'PIZ', 'PJP', 'PJT', 'PK', 'PKE', 'PKG', 'PKI',
          'PKOH', 'PKW', 'PKX', 'PLAB', 'PLAN', 'PLAY', 'PLBY', 'PLCE', 'PLD', 'PLG', 'PLL', 'PLMR', 'PLNT', 'PLOW', 'PLSE', 'PLT', 'PLTK', 'PLTR', 'PLUG',
          'PLUS', 'PLX', 'PLXS', 'PLYA', 'PM', 'PMT', 'PNC', 'PNFP', 'PNM', 'PNNT', 'PNQI', 'PNR', 'PNTG', 'PNW', 'PODD', 'POOL', 'POR', 'POST', 'POTX',
          'POWI', 'POWW', 'PPA', 'PPBI', 'PPBT', 'PPC', 'PPD', 'PPG', 'PPH', 'PPL', 'PQG', 'PRA', 'PRAA', 'PRAH', 'PRAX', 'PRCH', 'PRDO', 'PRF', 'PRFT',
          'PRFZ', 'PRG', 'PRGO', 'PRGS', 'PRI', 'PRIM', 'PRK', 'PRLB', 'PRMW', 'PRN', 'PRO', 'PROF', 'PROG', 'PRPB', 'PRPH', 'PRPL', 'PRQR', 'PRSP',
          'PRTA', 'PRTK', 'PRTS', 'PRTY', 'PRU', 'PRVB', 'PS', 'PSA', 'PSAC', 'PSB', 'PSCH', 'PSEC', 'PSEP', 'PSL', 'PSMT', 'PSN', 'PSNL', 'PSO', 'PSP',
          'PSQ', 'PST', 'PSTG', 'PSTH', 'PSTI', 'PSTX', 'PSX', 'PSXP', 'PTC', 'PTCT', 'PTE', 'PTEN', 'PTF', 'PTGX', 'PTH', 'PTLC', 'PTMN', 'PTNQ', 'PTON',
          'PTPI', 'PTR', 'PTVCB', 'PTVE', 'PUK', 'PUMP', 'PVAC', 'PVG', 'PVH', 'PVL', 'PWFL', 'PWR', 'PXD', 'PXH', 'PXI', 'PXJ', 'PXLW', 'PYPL', 'PZA',
          'PZN', 'PZZA', 'QABA', 'QADA', 'QCLN', 'QCOM', 'QCRH', 'QD', 'QDEL', 'QELL', 'QEP', 'QFIN', 'QGEN', 'QID', 'QIWI', 'QLD', 'QLGN', 'QLYS', 'QMCO',
          'QNST', 'QQEW', 'QQQ', 'QQQE', 'QQQJ', 'QQQM', 'QRTEA', 'QRVO', 'QS', 'QSR', 'QTEC', 'QTNT', 'QTRX', 'QTS', 'QTT', 'QTWO', 'QUAD', 'QUAL', 'QUIK',
          'QUMU', 'QUOT', 'QURE', 'QYLD', 'R', 'RACE', 'RAD', 'RADA', 'RAIL', 'RAMP', 'RAPT', 'RARE', 'RAVE', 'RAVN', 'RBA', 'RBAC', 'RBBN', 'RBC', 'RBCAA',
          'RC', 'RCEL', 'RCI', 'RCII', 'RCKT', 'RCL', 'RCM', 'RCMT', 'RCUS', 'RDFN', 'RDHL', 'RDI', 'RDN', 'RDNT', 'RDS.A', 'RDS.B', 'RDUS', 'RDWR', 'RDY',
          'RE', 'REAL', 'REDU', 'REED', 'REET', 'REFR', 'REG', 'REGI', 'REGL', 'REGN', 'REI', 'REK', 'REKR', 'RELL', 'REM', 'REMX', 'RENN', 'REPH', 'REPL',
          'RES', 'RESN', 'RETA', 'RETL', 'REV', 'REVG', 'REW', 'REXR', 'REYN', 'REZ', 'REZI', 'RF', 'RFIL', 'RFL', 'RFP', 'RGA', 'RGEN', 'RGLD', 'RGLS',
          'RGNX', 'RGP', 'RGR', 'RGS', 'RH', 'RHI', 'RHP', 'RICK', 'RIDE', 'RIG', 'RIGL', 'RILY', 'RING', 'RIOT', 'RJA', 'RJF', 'RJI', 'RJN', 'RKDA', 'RKT',
          'RL', 'RLAY', 'RLGT', 'RLGY', 'RLH', 'RLI', 'RLJ', 'RLMD', 'RLX', 'RM', 'RMAX', 'RMBS', 'RMD', 'RMNI', 'RMO', 'RMTI', 'RNET', 'RNG', 'RNLX', 'RNR',
          'RNST', 'RNWK', 'ROAD', 'ROBO', 'ROCK', 'RODM', 'ROG', 'ROIC', 'ROK', 'ROKU', 'ROL', 'ROLL', 'ROM', 'ROOT', 'ROP', 'ROST', 'RP', 'RPAI', 'RPAR',
          'RPAY', 'RPD', 'RPG', 'RPLA', 'RPM', 'RPRX', 'RPT', 'RPV', 'RRC', 'RRD', 'RRGB', 'RRR', 'RS', 'RSG', 'RSI', 'RSP', 'RSX', 'RTH', 'RTLR', 'RTP',
          'RTX', 'RUBY', 'RUN', 'RUSHA', 'RUSL', 'RUTH', 'RVLV', 'RVMD', 'RVNC', 'RVP', 'RVSB', 'RWJ', 'RWK', 'RWL', 'RWLK', 'RWM', 'RWO', 'RWR', 'RWT',
          'RWX', 'RXL', 'RXN', 'RXT', 'RY', 'RYAAY', 'RYAM', 'RYB', 'RYH', 'RYI', 'RYN', 'RYTM', 'SA', 'SAA', 'SABR', 'SAFE', 'SAFM', 'SAFT', 'SAGE', 'SAH',
          'SAIA', 'SAIC', 'SAII', 'SAIL', 'SAM', 'SAN', 'SAND', 'SANM', 'SANW', 'SAP', 'SASR', 'SATS', 'SAVA', 'SAVE', 'SB', 'SBAC', 'SBBP', 'SBCF', 'SBGI',
          'SBH', 'SBIO', 'SBLK', 'SBNY', 'SBRA', 'SBS', 'SBSI', 'SBSW', 'SBUX', 'SC', 'SCCO', 'SCHA', 'SCHB', 'SCHC', 'SCHD', 'SCHE', 'SCHF', 'SCHG', 'SCHH',
          'SCHL', 'SCHM', 'SCHN', 'SCHP', 'SCHR', 'SCHV', 'SCHW', 'SCHX', 'SCHZ', 'SCI', 'SCJ', 'SCL', 'SCM', 'SCO', 'SCOR', 'SCPL', 'SCS', 'SCSC', 'SCU',
          'SCVL', 'SCWX', 'SCYX', 'SCZ', 'SD', 'SDC', 'SDGR', 'SDIV', 'SDOW', 'SDS', 'SDY', 'SE', 'SEAC', 'SEAS', 'SECO', 'SECT', 'SEDG', 'SEE', 'SEEL',
          'SEER', 'SEF', 'SEIC', 'SELB', 'SEM', 'SENS', 'SESN', 'SF', 'SFBS', 'SFE', 'SFIX', 'SFL', 'SFM', 'SFNC', 'SFT', 'SGC', 'SGEN', 'SGFY', 'SGG',
          'SGH', 'SGLB', 'SGMO', 'SGMS', 'SGOL', 'SGRY', 'SGU', 'SH', 'SHAK', 'SHEN', 'SHLS', 'SHLX', 'SHO', 'SHOO', 'SHOP', 'SHW', 'SHY', 'SHYF', 'SHYG',
          'SI', 'SIBN', 'SID', 'SIEB', 'SIEN', 'SIFY', 'SIG', 'SIGA', 'SIGI', 'SII', 'SIL', 'SILJ', 'SILK', 'SILV', 'SIMO', 'SINA', 'SINO', 'SIOX', 'SIRI',
          'SITC', 'SITE', 'SIVB', 'SIVR', 'SIX', 'SIZE', 'SJB', 'SJI', 'SJM', 'SJNK', 'SJR', 'SJT', 'SJW', 'SKF', 'SKLZ', 'SKM', 'SKT', 'SKX', 'SKY', 'SKYW',
          'SKYY', 'SLAB', 'SLB', 'SLCA', 'SLDB', 'SLF', 'SLG', 'SLGN', 'SLM', 'SLNO', 'SLP', 'SLQT', 'SLRC', 'SLS', 'SLV', 'SLX', 'SLYV', 'SM', 'SMAR',
          'SMBK', 'SMCI', 'SMDV', 'SMED', 'SMFG', 'SMG', 'SMH', 'SMHI', 'SMLP', 'SMMT', 'SMN', 'SMOG', 'SMP', 'SMPL', 'SMSI', 'SMTC', 'SMTX', 'SNA', 'SNAP',
          'SNBR', 'SNCR', 'SND', 'SNDL', 'SNDR', 'SNDX', 'SNE', 'SNEX', 'SNLN', 'SNN', 'SNOW', 'SNP', 'SNPR', 'SNPS', 'SNR', 'SNV', 'SNX', 'SNY', 'SO',
          'SOAC', 'SOCL', 'SOGO', 'SOHU', 'SOI', 'SOL', 'SOLO', 'SON', 'SONO', 'SOS', 'SOXL', 'SOXS', 'SOXX', 'SOYB', 'SP', 'SPAB', 'SPAK', 'SPB', 'SPCE',
          'SPCX', 'SPDN', 'SPDW', 'SPEM', 'SPEU', 'SPG', 'SPGI', 'SPH', 'SPHB', 'SPHD', 'SPHQ', 'SPI', 'SPIB', 'SPIP', 'SPKE', 'SPLB', 'SPLG', 'SPLK',
          'SPLV', 'SPNE', 'SPNS', 'SPNT', 'SPOK', 'SPOT', 'SPPI', 'SPR', 'SPRO', 'SPRQ', 'SPRT', 'SPSB', 'SPSC', 'SPSM', 'SPT', 'SPTI', 'SPTL', 'SPTM',
          'SPTN', 'SPTS', 'SPWH', 'SPWR', 'SPXC', 'SPXL', 'SPXS', 'SPXU', 'SPXZ', 'SPY', 'SPYD', 'SPYG', 'SPYV', 'SQ', 'SQBG', 'SQM', 'SQQQ', 'SR', 'SRAC',
          'SRAX', 'SRC', 'SRCE', 'SRCL', 'SRDX', 'SRE', 'SRET', 'SREV', 'SRG', 'SRGA', 'SRI', 'SRLN', 'SRLP', 'SRNE', 'SRPT', 'SRRK', 'SRS', 'SRT', 'SRTY',
          'SRVR', 'SSB', 'SSD', 'SSL', 'SSNC', 'SSO', 'SSP', 'SSPK', 'SSRM', 'SSSS', 'SSTK', 'SSYS', 'ST', 'STAA', 'STAG', 'STAR', 'STAY', 'STBA', 'STC',
          'STCN', 'STE', 'STEP', 'STFC', 'STIC', 'STIM', 'STKL', 'STL', 'STLA', 'STLD', 'STM', 'STMP', 'STNE', 'STNG', 'STOK', 'STON', 'STOR', 'STPK',
          'STRA', 'STRL', 'STRO', 'STT', 'STWD', 'STX', 'STXS', 'STZ', 'SU', 'SUBZ', 'SUI', 'SUM', 'SUMO', 'SUN', 'SUNS', 'SUNW', 'SUP', 'SUPN', 'SUPV',
          'SURF', 'SUSL', 'SVAC', 'SVC', 'SVM', 'SVMK', 'SVRA', 'SVVC', 'SVXY', 'SWAV', 'SWBI', 'SWCH', 'SWI', 'SWIR', 'SWK', 'SWKS', 'SWM', 'SWN', 'SWX',
          'SXC', 'SXI', 'SXT', 'SYBX', 'SYF', 'SYK', 'SYKE', 'SYNA', 'SYNC', 'SYNH', 'SYNL', 'SYRS', 'SYX', 'SYY', 'T', 'TA', 'TACO', 'TACT', 'TAIL', 'TAK',
          'TAL', 'TALO', 'TAN', 'TAP', 'TARO', 'TAST', 'TBA', 'TBBK', 'TBF', 'TBI', 'TBIO', 'TBK', 'TBNK', 'TBPH', 'TBT', 'TCBI', 'TCBK', 'TCDA', 'TCF',
          'TCMD', 'TCOM', 'TCON', 'TCPC', 'TCRR', 'TCS', 'TCX', 'TD', 'TDC', 'TDG', 'TDIV', 'TDOC', 'TDS', 'TDW', 'TDY', 'TEAM', 'TECH', 'TECK', 'TECL',
          'TECS', 'TEF', 'TEL', 'TELL', 'TEN', 'TENB', 'TEO', 'TER', 'TEUM', 'TEVA', 'TEX', 'TFC', 'TFFP', 'TFI', 'TFLO', 'TFSL', 'TFX', 'TG', 'TGB', 'TGH',
          'TGI', 'TGNA', 'TGP', 'TGS', 'TGT', 'TGTX', 'THBR', 'THC', 'THCA', 'THCB', 'THCX', 'THD', 'THFF', 'THG', 'THO', 'THR', 'THRM', 'THS', 'TIGR',
          'TILE', 'TIMB', 'TIP', 'TISI', 'TITN', 'TJX', 'TK', 'TKC', 'TKR', 'TLH', 'TLMD', 'TLND', 'TLRY', 'TLS', 'TLSA', 'TLT', 'TLYS', 'TM', 'TMDX',
          'TME', 'TMF', 'TMHC', 'TMO', 'TMP', 'TMQ', 'TMST', 'TMUS', 'TMV', 'TMX', 'TNA', 'TNC', 'TNDM', 'TNET', 'TNK', 'TNL', 'TNP', 'TOL', 'TOT', 'TOUR',
          'TOWN', 'TPB', 'TPC', 'TPCO', 'TPGY', 'TPH', 'TPIC', 'TPOR', 'TPR', 'TPTX', 'TPVG', 'TPX', 'TQQQ', 'TR', 'TRC', 'TREC', 'TREE', 'TREX', 'TRGP',
          'TRHC', 'TRI', 'TRIB', 'TRIL', 'TRIP', 'TRIT', 'TRMB', 'TRMK', 'TRN', 'TRNO', 'TROW', 'TROX', 'TRP', 'TRQ', 'TRS', 'TRST', 'TRTN', 'TRTX', 'TRU',
          'TRUE', 'TRUP', 'TRV', 'TRVG', 'TRVN', 'TRX', 'TS', 'TSCO', 'TSE', 'TSEM', 'TSLA', 'TSLX', 'TSM', 'TSN', 'TSQ', 'TT', 'TTAC', 'TTC', 'TTCF', 'TTD',
          'TTEC', 'TTEK', 'TTGT', 'TTI', 'TTM', 'TTMI', 'TTNP', 'TTOO', 'TTT', 'TTWO', 'TU', 'TUFN', 'TUP', 'TUR', 'TURN', 'TUSK', 'TV', 'TVTX', 'TVTY',
          'TW', 'TWI', 'TWIN', 'TWLO', 'TWM', 'TWNK', 'TWO', 'TWOU', 'TWST', 'TWTR', 'TX', 'TXG', 'TXMD', 'TXN', 'TXRH', 'TXT', 'TYD', 'TYL', 'TYME', 'TYO',
          'TZA', 'TZOO', 'U', 'UA', 'UAA', 'UAL', 'UAMY', 'UAN', 'UAVS', 'UBA', 'UBER', 'UBS', 'UBSI', 'UBT', 'UBX', 'UCBI', 'UCO', 'UCTT', 'UDN', 'UDOW',
          'UDR', 'UE', 'UEC', 'UEIC', 'UEPS', 'UFCS', 'UFI', 'UFO', 'UFPI', 'UFS', 'UGA', 'UGI', 'UGL', 'UGP', 'UHAL', 'UHS', 'UHT', 'UI', 'UIHC', 'UIS',
          'UL', 'ULBI', 'ULE', 'ULTA', 'UMBF', 'UMC', 'UMDD', 'UMH', 'UMPQ', 'UNF', 'UNFI', 'UNG', 'UNH', 'UNIT', 'UNL', 'UNM', 'UNP', 'UNVR', 'UPLD',
          'UPRO', 'UPS', 'UPST', 'UPWK', 'URA', 'URBN', 'URE', 'URGN', 'URI', 'URNM', 'URTH', 'URTY', 'USAC', 'USAK', 'USAT', 'USB', 'USCR', 'USD', 'USDU',
          'USFD', 'USHY', 'USIG', 'USL', 'USM', 'USMC', 'USMV', 'USNA', 'USO', 'USPH', 'UST', 'USX', 'UTHR', 'UTI', 'UTL', 'UTSI', 'UTSL', 'UTZ', 'UUP',
          'UUUU', 'UVE', 'UVSP', 'UVV', 'UVXY', 'UWM', 'UWMC', 'UXIN', 'UYG', 'UYM', 'V', 'VAC', 'VALE', 'VALPQ', 'VAPO', 'VAR', 'VAW', 'VB', 'VBIV', 'VBK',
          'VBLT', 'VBR', 'VBTX', 'VC', 'VCEL', 'VCIT', 'VCLT', 'VCNX', 'VCR', 'VCRA', 'VCSH', 'VCTR', 'VCVC', 'VCYT', 'VDC', 'VDE', 'VEA', 'VEC', 'VECO',
          'VEDL', 'VEEV', 'VEON', 'VER', 'VERI', 'VERU', 'VET', 'VEU', 'VFC', 'VFF', 'VFH', 'VG', 'VGAC', 'VGIT', 'VGK', 'VGLT', 'VGR', 'VGSH', 'VGT', 'VGZ',
          'VHC', 'VHT', 'VIAC', 'VIACA', 'VIAV', 'VICI', 'VICR', 'VIE', 'VIG', 'VIH', 'VIPS', 'VIR', 'VIRT', 'VIRX', 'VIS', 'VISL', 'VITL', 'VIV', 'VIVO',
          'VIXM', 'VIXY', 'VKTX', 'VLDR', 'VLO', 'VLRS', 'VLUE', 'VLY', 'VMBS', 'VMC', 'VMI', 'VMW', 'VNDA', 'VNE', 'VNET', 'VNO', 'VNOM', 'VNQ', 'VNQI',
          'VNRX', 'VNT', 'VNTR', 'VO', 'VOC', 'VOD', 'VOE', 'VOLT', 'VONV', 'VOO', 'VOOG', 'VOT', 'VOX', 'VOXX', 'VOYA', 'VPG', 'VPL', 'VPU', 'VRA', 'VRAY',
          'VREX', 'VRM', 'VRNA', 'VRNS', 'VRNT', 'VRP', 'VRRM', 'VRS', 'VRSK', 'VRSN', 'VRT', 'VRTV', 'VRTX', 'VSAT', 'VSEC', 'VSH', 'VSPR', 'VSS', 'VST',
          'VSTM', 'VSTO', 'VT', 'VTC', 'VTEB', 'VTI', 'VTNR', 'VTOL', 'VTR', 'VTRS', 'VTV', 'VTWG', 'VTWO', 'VUG', 'VUZI', 'VV', 'VVI', 'VVNT', 'VVPR',
          'VVV', 'VWO', 'VWOB', 'VXF', 'VXRT', 'VXUS', 'VXX', 'VXZ', 'VYGR', 'VYM', 'VYNE', 'VZ', 'W', 'WAB', 'WABC', 'WAFD', 'WAL', 'WASH', 'WAT', 'WATT',
          'WB', 'WBA', 'WBAI', 'WBS', 'WBT', 'WCC', 'WCLD', 'WCN', 'WD', 'WDAY', 'WDC', 'WDFC', 'WDR', 'WEAT', 'WEC', 'WELL', 'WEN', 'WERN', 'WES', 'WETF',
          'WEX', 'WFC', 'WFH', 'WGO', 'WH', 'WHD', 'WHG', 'WHR', 'WIFI', 'WIMI', 'WING', 'WIRE', 'WISH', 'WIT', 'WIX', 'WK', 'WKHS', 'WLDN', 'WLK', 'WLKP',
          'WLL', 'WLTW', 'WM', 'WMB', 'WMC', 'WMG', 'WMK', 'WMS', 'WMT', 'WNC', 'WNEB', 'WNS', 'WOOD', 'WOOF', 'WOR', 'WORK', 'WOW', 'WPC', 'WPG', 'WPM',
          'WPP', 'WPRT', 'WPS', 'WRAP', 'WRB', 'WRE', 'WRI', 'WRK', 'WRLD', 'WSBC', 'WSBF', 'WSC', 'WSFS', 'WSM', 'WSO', 'WSR', 'WST', 'WTBA', 'WTFC', 'WTI',
          'WTRG', 'WTRH', 'WTS', 'WTTR', 'WU', 'WVE', 'WW', 'WWD', 'WWE', 'WWR', 'WWW', 'WY', 'WYNN', 'X', 'XAIR', 'XAR', 'XBI', 'XBIT', 'XEC', 'XEL',
          'XENE', 'XENT', 'XERS', 'XES', 'XHB', 'XHE', 'XHR', 'XIN', 'XL', 'XLB', 'XLC', 'XLE', 'XLF', 'XLI', 'XLK', 'XLNX', 'XLP', 'XLRE', 'XLRN', 'XLU',
          'XLV', 'XLY', 'XM', 'XME', 'XMLV', 'XNCR', 'XNET', 'XOM', 'XONE', 'XOP', 'XP', 'XPEL', 'XPER', 'XPEV', 'XPH', 'XPO', 'XPP', 'XRAY', 'XRT', 'XRX',
          'XSD', 'XSLV', 'XSOE', 'XSPA', 'XT', 'XXII', 'XYL', 'Y', 'YANG', 'YCBD', 'YCL', 'YCS', 'YELL', 'YELP', 'YETI', 'YEXT', 'YGYI', 'YINN', 'YMAB',
          'YMTX', 'YNDX', 'YOLO', 'YORW', 'YPF', 'YRD', 'YSG', 'YUM', 'YUMC', 'YXI', 'YY', 'Z', 'ZBH', 'ZBRA', 'ZDGE', 'ZEN', 'ZEPP', 'ZEUS', 'ZG', 'ZGNX',
          'ZI', 'ZION', 'ZIOP', 'ZIXI', 'ZLAB', 'ZM', 'ZNGA', 'ZNH', 'ZNOG', 'ZNTE', 'ZROZ', 'ZS', 'ZSL', 'ZTO', 'ZTS', 'ZUMZ', 'ZUO', 'ZVO', 'ZYME', 'ZYNE', 'ZYXI', ]
'''


def human_time(epoch):
    new_time = datetime.fromtimestamp(int(epoch) / 1000)
    output = new_time.strftime('%Y-%m-%d %H:%M:%S')

    return output


def get_time_now():
    curr_time = time.localtime()
    curr_clock = time.strftime("%H:%M:%S", curr_time)
    curr_m = time.strftime('%m')
    curr_y_d = time.strftime('%d%Y')

    int_curr_clock = int(f'{curr_clock[:2]}{curr_clock[3:5]}')

    return int_curr_clock, curr_m, curr_y_d


def all_fridays(year):
    return pd.date_range(start=str(year), end=str(year+1),
                         freq='W-FRI').strftime('%m/%d/%Y').tolist()


def last_chain(weeks_out):  # returns the date to put into lookup_chain
    today = str(date.today().strftime("%m/%d/%Y"))
    year = today[-4:]
    x_days = all_fridays(int(year))[:52]

    fri_count = 0

    for i in x_days:
        if today < i:
            fri_count = fri_count + 1
            if fri_count == weeks_out:
                return f'{i[-4:]}-{i[:2]}-{i[3:5]}'

    if fri_count < 5:
        y_days = all_fridays(year + 1)[:52]
        for i in y_days:
            if today < i:
                fri_count = fri_count + 1
                if fri_count == weeks_out:
                    return f'{i[-4:]}-{i[:2]}-{i[3:5]}'

                
def get_chain(stock):
    global to_date
    
    opt_lookup = TDSession.get_options_chain(
        option_chain={'symbol': stock, 'strikeCount': 50,
                      'toDate': to_date})

    return opt_lookup


def raw_chain(raw, put_call):
    cp = f'{put_call}ExpDateMap'
    raw_data = [[]]
    r = -1
    for k in raw[cp].keys():
        for strike in raw[cp][k].keys():
            for attr in raw[cp][k][strike][0].keys():

                unit = raw[cp][k][strike][0][attr]
                if unit == put_call.upper():
                    r = r + 1
                    if r > 0:
                        raw_data.append([])

                raw_data[r].append(unit)

    return raw_data


def clean_chain(raw):
    df_cp = pd.DataFrame(raw, columns=opt_column_names)
    clean = df_cp.drop(columns=columns_unwanted)

    return clean


pulls = 0
failed_pulls = 0


def get_next_chains():
    x = 0
    global pulls
    global failed_pulls

    for stock in stocks:
        error = False
        try:
            chain = get_chain(stock)
        except (exceptions.ServerError, exceptions.GeneralError, exceptions.ExdLmtError):
            error = True
            failed_pulls = failed_pulls + 1
            print('A server error occurred')

        if not error:
            try:
                working_call_data = clean_chain(raw_chain(chain, 'call'))
                add_rows(working_call_data, f'c{stock}')

                # print(working_call_data) UNCOMMENT to see working call data

                pulls = pulls + 1

            except ValueError:
                print(f'{x}: Calls for {stock} did not have values for this iteration')
                failed_pulls = failed_pulls + 1

            try:
                working_put_data = clean_chain(raw_chain(chain, 'put'))
                add_rows(working_call_data, f'p{stock}')

                # print(working_put_data) UNCOMMENT to see working put data

                pulls = pulls + 1

            except ValueError:
                print(f'{x}: Puts for {stock} did not have values for this iteration')
                failed_pulls = failed_pulls + 1

        print(f'{x}: {stock}')
        x = x + 1
        time.sleep(2)

    return 0


def main():

    global file_date, to_date

    to_date = str(last_chain(5))  # specify how many weeks of contracts you want for each pull
    t, mon, day = get_time_now()
    month = list(trade_days_2021.keys())[int(mon) - 1]

    while True:
        t, mon, day = get_time_now()
        if (t < 930) or (t > 1600):
            print(f'{t}: Market closed {month}{day}'.upper())

            time.sleep(15)
        else:
            break

    file_date = f'{month}{day}'
    pull_count = 0
    end_t = 1600

    while get_time_now()[0] < end_t:
        get_next_chains()
        pull_count = pull_count + 1
        print(pull_count)

    print('option market closed')
    print(f'failed_pulls: {failed_pulls}')
    print(f'pulls: {pulls}')

    return 0


main()


# |SQLite management| #
#
# make_sqlite_table('calls')  # inputs: puts|calls
# make_sqlite_table('puts')  # inputs: puts|calls
# delete_db_table('calls')
# delete_db_table('puts')
# show_db_table('calls')
# show_db_table('puts')
# add_rows(clean_chain(raw_chain(get_chain('SPY'), 'put')), 'puts')  # raw_chain(,'put|call')), 'puts|calls')
# delete_row('puts', '', 1321354652)
