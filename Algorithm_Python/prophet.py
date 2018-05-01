#Used Anaconda distribution, fbprophet may have trouble installing in regular python
import pandas as pd #conda install -c anaconda pandas , for pandas dataframes
import numpy as np
from fbprophet import Prophet #conda install -c conda-forge fbprophet , open source prediction library
import csv
import pyowm #pip install pyowm , open weather maps api
import mysql.connector #conda install -c anaconda mysql-connector-python , mySQL connector
import os


class ProphetPrediction:
    
    def __init__(self, isSim):
        self.cnx = mysql.connector.connect(user='root', password='password', host='localhost', database='cargo') #connect to mySQL datebase
        self.cursor = self.cnx.cursor()
        
        #if we are running a sim, prophet will use a sim table to generate for our desired data
        #since it's forecasts start right after the last order in the orders table
        if isSim:
            self.table = "simOrders"
        else:
            self.table = "orders"
        
    #Length - how many minutes prohpet will predict into future from last data point
    def runPrediction(self, Length):
        self.getInclementWeather()
        self.fiveMinDemand(Length)
        self.thirtyMinDemand(Length)
        self.combineCSV()
        self.updatePredictionOutputTable()
        os.remove('fiveMinPredictionOutput.csv')
        os.remove('temp.csv')
        os.remove('thirtyMinPredictionOutput.csv')
        os.remove('predictionOutput.csv')
        return

    def fiveMinDemand(self, forecastLength):
        self.cursor.execute("SELECT CONVERT_TZ(delivered_at,'+00:00','-05:00') as time_interval, COUNT(distinct id) as count FROM " + self.table + " where delivered_at <> '0000-00-00 00:00:00' and delivered_at > '2017-11-01 00:00:00' GROUP BY date(delivered_at), hour(delivered_at), minute(delivered_at),second(delivered_at);")
        rows = self.cursor.fetchall()
        with open('temp.csv','w', newline='') as fileout: #create temp.csv for prophet to read and fill with data
            writer = csv.writer(fileout)
            writer.writerow([i[0] for i in self.cursor.description])
            writer.writerows(rows)
        df = pd.read_csv('temp.csv')
        df['time_interval'] = pd.to_datetime(df['time_interval'])
        df.index=df['time_interval']
        df = df.resample('5min').sum()
        #print(df)
        df.to_csv('temp.csv')
        x = forecastLength #period
        y = "five" #for saving .csv filename
        z = 0.01 #changepoint_prior_scale (flexibility)
        self.prophetForecast(x,y,z)
        return
    
    def thirtyMinDemand(self, forecastLength):
        self.cursor.execute("SELECT CONVERT_TZ(delivered_at,'+00:00','-05:00') as time_interval, COUNT(distinct id) as count FROM " + self.table + " where delivered_at <> '0000-00-00 00:00:00' and delivered_at > '2017-11-01 00:00:00' GROUP BY date(delivered_at), hour(delivered_at), minute(delivered_at),second(delivered_at);")
        rows = self.cursor.fetchall()
        with open('temp.csv','w', newline='') as fileout: #create temp.csv for prophet to read and fill with data
            writer = csv.writer(fileout)
            writer.writerow([i[0] for i in self.cursor.description])
            writer.writerows(rows)
        df = pd.read_csv('temp.csv')
        df['time_interval'] = pd.to_datetime(df['time_interval'])
        df.index=df['time_interval']
        df = df.resample('30min').sum()
        #print(df)
        df.to_csv('temp.csv')
        x = forecastLength #period
        y = "thirty" #for .csv filename
        z = 0.01 #changepoint_prior_scale (flexibility)
        self.prophetForecast(x,y,z)
        return
    
    def prophetForecast(self, x,y,z):
        df = pd.read_csv('temp.csv') #read temp.csv
        df = df.rename(columns={'time_interval': 'ds','count': 'y'}) #rename columns, prophet requires 'ds' and 'y' column names
        #df['y']= np.log(df['y']) #log as in logrithmic, log the y column for better prediction
        w_df = pd.read_csv('weather_dates.csv')
        
        #holiday/event dataframes to look for effects on those dates
        Thanksgiving = pd.DataFrame({
        'holiday': 'Thanksgiving',
        'ds': pd.to_datetime(['2017-11-23','2018-11-22','2019-11-28',
                              '2020-11-26','2021-11-25','2022-11-24']),
        'lower_window': 0, #days after holiday
        'upper_window': 1, #days before holiday
        })
        Christmas = pd.DataFrame({
        'holiday': 'Christmas',
        'ds': pd.to_datetime(['2017-12-25','2018-12-25','2019-12-25',
                              '2020-12-25','2021-12-25','2022-12-25']),
        'lower_window': 0,
        'upper_window': 1,
        })
        Superbowl = pd.DataFrame({
        'holiday': 'Superbowl',
        'ds': pd.to_datetime(['2018-02-04', '2019-02-03', '2020-02-02',
                              '2021-02-07', '2022-02-06']), #dates subject to change
        'lower_window': 0,
        'upper_window': 1,
        })
        NewYears = pd.DataFrame({
        'holiday': 'NewYears',
        'ds': pd.to_datetime(['2018-01-01', '2019-01-01', '2020-01-01',
                              '2021-01-01', '2022-01-01']),
        'lower_window': 0,
        'upper_window': 1,
        })
        SpringBreak = pd.DataFrame({
        'holiday': 'SpringBreak',
        'ds': pd.to_datetime(['2018-03-11, 2019-03-12']), #dates subject to change
        'lower_window': -6,
        'upper_window': 0,
        })
        StPatricks = pd.DataFrame({
        'holiday': 'StPatricks',
        'ds': pd.to_datetime(['2018-02-17', '2019-02-17', '2020-02-17',
                              '2021-02-17', '2022-02-17']),
        'lower_window': 0,
        'upper_window': 1,
        })
        Valentines = pd.DataFrame({
        'holiday': 'Valentines',
        'ds': pd.to_datetime(['2018-02-14', '2019-02-14', '2020-02-14',
                              '2021-02-14', '2022-02-14']),
        'lower_window': 0,
        'upper_window': 1,
        })
        ForthOfJuly = pd.DataFrame({
        'holiday': 'ForthOfJuly',
        'ds': pd.to_datetime(['2018-07-04', '2019-07-04', '2020-07-04',
                              '2021-07-04', '2022-07-04']),
        'lower_window': 0,
        'upper_window': 1,
        })
        
        InclementWeather = pd.DataFrame({
        'holiday': 'InclementWeather',
        'ds': pd.to_datetime(['2018-02-06 12:00:00', '2018-02-06 15:00:00', 
                              '2018-02-06 18:00:00', '2018-02-06 21:00:00']), #Freezing rain day
        'lower_window': -.125,
        'upper_window': 0,
        })
        
        InclementWeather = pd.concat([InclementWeather, w_df], ignore_index=True) #concat forecast dataframe(w_df) to InclementWeather df
        InclementWeather.drop_duplicates(subset=['ds'], inplace=True, keep='last') #remove duplicates
        
        holidays = pd.concat([Thanksgiving, Christmas, Superbowl, NewYears, SpringBreak, StPatricks, Valentines, ForthOfJuly, InclementWeather]) #concat all holiday dataframes
        
        m = Prophet(yearly_seasonality=False, holidays=holidays, changepoint_prior_scale=z) #apply holidays, change flexibility default: .05
        df['floor'] = 0 #set floor
        print("before")
        m.fit(df) #------------------------Freezes
        print("after")
        future = m.make_future_dataframe(periods=x, freq='1min', include_history = False) #freq = interval into future. period = how many times. include_history = do not include.
        forecast = m.predict(future)
        forecast['floor'] = 0
        #m.plot(forecast); #display graph
        #m.plot_components(forecast); #display seasonality/holiday information
        forecast = forecast.rename(columns={'ds': 'date_and_time','yhat': y + '_min_prediction'})
        forecast[['date_and_time', y + '_min_prediction']].to_csv(y + 'MinPredictionOutput.csv') #export prophets calculations
        return
    
    def getInclementWeather(self):
        owm = pyowm.OWM('288eca450f37eb5c71277758ee77c11f') #API key, free can only query once every 10 minutes
        fc = owm.three_hours_forecast_at_id(4379966) #get forecast at Cape Girardeau
        f = fc.get_forecast() #put forecast in object f
        
        #test forecast
        #for i in f._weathers[:38]: 
        #      print(i.get_reference_time('iso'),i.get_status())
        
        lst = list() #list to store dates, type string
        for i in f._weathers[:8]: #put tommorow's forecasted dates that are within working hours and have certain weather codes in a list
             #check for specific weather ids. Mostly Severe weather conditions(freezing rain, heavy rain, etc.) See https://openweathermap.org/weather-conditions for codes.
             if (i.get_reference_time('date').hour >= 15 or i.get_reference_time('date').hour <= 6) and (i.get_weather_code() == '511' or i.get_weather_code() == '502' or i.get_weather_code() == '503' or i.get_weather_code() == '202' or i.get_weather_code() == '212' or i.get_weather_code() == '602' or i.get_weather_code() == '601'):
                 lst.append(i.get_reference_time('iso'))
        w_df = pd.DataFrame({'holiday': 'InclementWeather', #put lst into dataframe that matches prophet's holiday format.
                             'ds': lst,
                             'lower_window': -.125,
                             'upper_window': 0}) 
        del lst[:]
        w_df['ds'] = pd.to_datetime(w_df['ds']) #convert string to datetime
        w_df.ds = w_df.ds.dt.tz_localize('UTC').dt.tz_convert('US/Central') #convert to local time, adds -5:00 to end of the datetime
        w_df.ds = w_df.ds.dt.tz_localize(None) #removes -5:00 at end
        w_df.drop_duplicates(subset=['ds'], inplace=True, keep='last') #remove duplicate times just in case
        w_df.to_csv('weather_dates.csv') #save to .cvs file

        
    def combineCSV(self):
        fiveMinPrediction = pd.read_csv('fiveMinPredictionOutput.csv', index_col=0) #read 5min prediction file
        thirtyMinPrediction = pd.read_csv('thirtyMinPredictionOutput.csv', index_col=0) #read 30min prediction file
        CombinedCSV = pd.merge(fiveMinPrediction, thirtyMinPrediction, on = 'date_and_time', how = 'left') #combine using common date_and_time
        CombinedCSV['date_and_time'] = pd.to_datetime(CombinedCSV['date_and_time']) #convert to datetime type
        
        #convert to UTC, disabled for testing
#        CombinedCSV.date_and_time = CombinedCSV.date_and_time.dt.tz_localize('US/Central').dt.tz_convert('UTC') #convert to UTC timezone
#        CombinedCSV.date_and_time = CombinedCSV.date_and_time.dt.tz_localize(None) #remove trailing timezone number
        
        CombinedCSV["five_min_drivers"] = np.nan #column added by request of group member
        CombinedCSV["thirty_min_drivers"] = np.nan #column added by request of group member
        CombinedCSV.index.name = 'id'
        CombinedCSV.to_csv('PredictionOutput.csv', sep=',', index=True, encoding='utf-8') #output to .csv
        return
    
    def updatePredictionOutputTable(self): #create temp_table, insert predictionOutput.csv into temp_table, compare temp_table with prediction_output table, update existing entries, insert new entries, drop temp_table.
        self.cursor.execute("CREATE TEMPORARY TABLE temp_table LIKE prediction_output;")
        self.cursor.execute("LOAD DATA LOCAL INFILE 'predictionOutput.csv' INTO TABLE temp_table COLUMNS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 LINES(@dummy, date_and_time, five_min_prediction, thirty_min_prediction, @dummy, @dummy);")
        self.cursor.execute("INSERT INTO prediction_output (date_and_time, five_min_prediction, thirty_min_prediction) SELECT date_and_time, five_min_prediction, thirty_min_prediction FROM temp_table WHERE date_and_time NOT IN (SELECT date_and_time FROM prediction_output);")
        self.cursor.execute("UPDATE prediction_output JOIN temp_table ON prediction_output.date_and_time = temp_table.date_and_time  SET prediction_output.five_min_prediction = temp_table.five_min_prediction, prediction_output.thirty_min_prediction = temp_table.thirty_min_prediction;")
        self.cursor.execute("DROP TEMPORARY TABLE temp_table;")
        self.cnx.commit()
        return
    
#    def createPrediction_OutputTable(self): #create prediction_output table in mySQL and insert data from predictionOutput.csv
#        self.cursor.execute("CREATE TABLE prediction_output (id INT AUTO_INCREMENT PRIMARY KEY, date_and_time DATETIME, five_min_prediction DOUBLE, thirty_min_prediction DOUBLE, five_min_drivers INT, thirty_min_drivers INT);")
#        self.cursor.execute("LOAD DATA LOCAL INFILE 'predictionOutput.csv' INTO TABLE prediction_output COLUMNS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 LINES;")
#        self.cnx.commit()
#        return
