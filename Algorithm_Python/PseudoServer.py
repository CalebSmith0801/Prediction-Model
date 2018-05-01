#GUI Interface that modifies the prediction_output tables with the recommended number of drivers
#Takes prophets predicted number of orders and converts that to drivers by
#Taking the ceiling of the predicted number of orders and subtracting that from available drivers and
#the estimateed number of drivers who are going to finish delivering their order and be back within
#five and thirty minutes

import OrdersClass
import prophet

import pymysql
import datetime
import math
import queue
import threading

from tkinter import Tk, ttk, Label, IntVar, DISABLED, NORMAL

class Server:
	#our mySQL server
    cargoDB = pymysql.connect(host='localhost', user='root', password='password', db='cargo' )
    cursor = cargoDB.cursor()
    Orders = OrdersClass.Orders()
    
	#Sets up tkinter GUI
    def __init__(self, master):
        self.master = master
        self.master.resizable(0, 0)
        self.master.geometry("300x300")
        self.master.winfo_toplevel().title("Pseudo Server")
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 13), padding = [0, 5])
        self.startButton = ttk.Button(root, text="Start", command=self.StartServer) #command=root.destroy
        self.startButton.grid(row = 0, column = 0, columnspan=2, pady=(30, 20))
        
        self.staticLabel = Label(root, text="Server Status:", font=("Arial", 12))
        self.statusLabel = Label(root, text ="Not Running", fg="red", font=("Arial", 12))
        self.staticLabel.grid(row=1, column = 0, sticky = "E", padx=(0, 10))
        self.statusLabel.grid(row=1, column = 1, sticky = "W")
        
        self.isChecked = IntVar()
        self.simCheckBut = ttk.Checkbutton(root, text='Simulation', variable=self.isChecked)
        self.simCheckBut.grid(row=2, column=0, columnspan=2, pady=(10, 10))
        
        self.unresponsiveLabel = Label(root, text="Program may seem unresponsive for a few seconds when server is starting. "
                                       + "Don't close the program", font=("Arial", 8), wraplength=290, justify='left')
        self.unresponsiveLabel.grid(row=3, column = 0, columnspan=2, pady=(100, 0))
        
        
        
    def setUpServerDateTime(self):        
        if self.isSimulation():
                self.todayTime = datetime.datetime(2018, 4, 16, 9, 0, 0, 0) #run simlutation for Feb, 16, 2018
        else:
            self.todayTime = datetime.datetime.now()
            
        self.todayTime = self.todayTime.replace(second=0, microsecond=0) #the id in prediction output table is a datetime of the form 12:05:00
        
        #set 1 minute prior to todayTime so that the query statement in loopServer will read any changes in database in between timeDataLastChecked and todayTime for first run
        self.timeDataLastChecked = self.todayTime + datetime.timedelta(minutes=-1) #used when looping; to check the database for updates every minute
        
        self.todayTimeUTC = self.todayTime + datetime.timedelta(hours=5)
        self.timeDataLastCheckedUTC = self.timeDataLastChecked + datetime.timedelta(hours=5)
        
	#waits for prophet code to finish
    def listen_for_result(self):
        print("listening")
        #Check if there is something in the queue
        try:
            self.res = self.thread_queue.get(0)
            self.statusLabel['text']="Running..."
            self.statusLabel['fg'] ='green'
            self.startButton.config(state=NORMAL)
            self.LoopServer()
        except queue.Empty:
            print("No Queue")
            root.after(1000, self.listen_for_result)
    
    def StartServer(self):
        if self.startButton['text'] == "Start":
            self.statusLabel['text'] = "Starting..."
            self.statusLabel['fg'] ='black'
            self.startButton['text'] = "Stop"
            self.startButton.config(state=DISABLED) #make it so you can't stop thread while it is running until prophet has finished
            
            self.simCheckBut.config(state=DISABLED)
            self.setUpServerDateTime()
            
			#check if prediction_table exits
            self.cursor.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'cargo' AND table_name = 'prediction_output'")
            
            predictionTable = self.cursor.fetchone()
            if predictionTable == None:
                self.createPredictionTable()
			
			#check if prophet prediction has been generated for today
            self.cursor.execute("SELECT * FROM prediction_output WHERE date_and_time = '%s'" %(self.todayTime))
            prophetResult = self.cursor.fetchone()
            if prophetResult == None: #if prophet hasn't been ran yet today
                self.thread_queue = queue.Queue()
                self.new_thread = threading.Thread(
                        target=runProphet,
                        kwargs={'thread_queue':self.thread_queue, 'today':self.todayTimeUTC, 'isSim':self.isSimulation()})
                self.new_thread.start()
                root.after(5000, self.listen_for_result)
            else:
                self.statusLabel['text']="Running..."
                self.statusLabel['fg'] ='green'
                self.startButton.config(state=NORMAL)
                self.LoopServer()

            
        elif self.startButton['text'] == "Stop":
            self.statusLabel['text'] = "Not Running"
            self.statusLabel['fg'] ='red'
            self.startButton['text'] = "Start"
            self.simCheckBut.config(state=NORMAL)
    
    
    def LoopServer(self):
        print("todayTime: ", self.todayTime)
        if self.isSimulation():
            loopTime = 1000 #make server loop where every 5 seconds realtime is 1 simulation minute
        else:
            loopTime = 60000 #make server loop every second. will need to be changes since each loop can take 5-20 seconds, so it will get behind
        
        
        self.calculateSubmittedOrders()
        self.calculateActiveDrivers()

        
        self.PredictDriversNeeded()
        self.timeDataLastChecked, self.timeDataLastCheckedUTC = self.todayTime, self.todayTimeUTC #will be used when querying database to see if there are any updates
        self.todayTime = self.todayTime + datetime.timedelta(minutes=1)
        self.todayTimeUTC = self.todayTimeUTC + datetime.timedelta(minutes=1)

        if self.isSimulation() and self.todayTime > datetime.datetime(2018, 4, 18, 2, 0, 0, 0):
            print("FINISHED")
            return
        
        if self.statusLabel['text'] == "Running...":
            root.after(loopTime, self.LoopServer) #loops server
            
    #To simulate live data, I used two datetimes, 1 minute apart which increment every loop
	#the database queries check any rows between these two times, which it thinks is 'live' data
	def calculateSubmittedOrders(self):
        self.cursor.execute("SELECT id, location_id from orders where submitted_at >= '%s' and submitted_at < '%s' order by id" %(self.timeDataLastCheckedUTC, self.todayTimeUTC))
        results = self.cursor.fetchall()
        
        for newOrder in results:
            if newOrder not in self.Orders.getProcOrders(): #if order is not already in the submitted order list
                self.Orders.addProcOrder(newOrder[0], newOrder[1])
                
    def calculateActiveDrivers(self):
        for submittedOrders in self.Orders.getProcOrders():
            #created_at < todayTime is used for simulation since static data has ever order status as delivered so we can't just grab the most recent like we would if it was live data
            self.cursor.execute("SELECT status from order_statuses where order_id = '%s' and created_at <= '%s' order by id desc limit 1;" %(submittedOrders, self.todayTimeUTC))
            status = self.cursor.fetchone()[0]
            if status != "submitted" and status != "processing" and status != "requesting" and status != 'failed':
                self.Orders.addActiveOrder(submittedOrders, self.Orders.getProcLocationID(submittedOrders))
                
        for activeOrders in self.Orders.getActiveOrders():
            if activeOrders in self.Orders.getProcOrders():
                self.Orders.removeProcOrder(activeOrders)
                
            self.cursor.execute("SELECT status from order_statuses where order_id = '%s' and created_at <= '%s' order by id desc limit 1;" %(activeOrders, self.todayTimeUTC))
            status = self.cursor.fetchone()[0]
            if status == "delivered":
                self.Orders.addFinOrder(activeOrders, self.Orders.getProcLocationID(activeOrders))
                
        for finOrders in self.Orders.getFinOrders():
            self.Orders.removeActiveOrder(finOrders)
        self.Orders.removeFinOrders()
               
    def PredictDriversNeeded(self):     
        
        #Even though an order is submitted, a driver is not needed until the restaurant 
        #has processed the order and hits 'request driver'.
        self.cursor.execute("Select AVG(Time_Till_Driver_Needed) from time")
        averageTimeTillDriverNeeded = self.cursor.fetchone()[0] #round to nearest integer 
        
        
        #takes the value predicted at the current time - the averageTimeTillDriverNeeded
        #because the amount of orders predicted at that time will have finished processing
        #and the restaurant will approximately be requesting a driver at the current time now
        self.cursor.execute("Select five_min_prediction from prediction_output where date_and_time = '%s'" %(self.todayTime - datetime.timedelta(minutes = int(averageTimeTillDriverNeeded / 60))))
        Result = self.cursor.fetchone()
        if Result == None:
            prophetForecast5Min = 0
        else:
            prophetForecast5Min = Result[0]
            
        self.cursor.execute("Select thirty_min_prediction from prediction_output where date_and_time = '%s'" %(self.todayTime - datetime.timedelta(minutes = int(averageTimeTillDriverNeeded / 60))))
        Result = self.cursor.fetchone()
        if Result == None:
            prophetForecast30Min = 0
        else:
            prophetForecast30Min = Result[0]
        
        #used created_at <= todaytime for simulation purposes
        #used timedelt seconds = 20 because brian said he updates the table every 20 seconds, so this will help the delay
        self.cursor.execute("SELECT num_drivers FROM cargo.drivers where created_at <= '%s' order by id desc limit 1" %(self.todayTimeUTC + datetime.timedelta(seconds = 20)))
        AvailableDrivers = self.cursor.fetchone()[0]
        
        ReturnTimes = []
        for order in self.Orders.getActiveOrders():
           ReturnTimes.append(self.EstimateDriverReturnTime(order))
        
        ReturnsWithin5Min = []
        ReturnsWithin30Min = []
        
        for driver in ReturnTimes:
            if driver < (5*60):
                ReturnsWithin5Min.append(driver)
            if driver < (30*60):
                ReturnsWithin30Min.append(driver)
        #print (self.todayTime, " 5: ", prophetForecast5Min, " Avail: ", AvailableDrivers, " Returns: ", len(ReturnsWithin5Min))
        #print (self.todayTime, " 30: ", prophetForecast30Min, " Avail: ", AvailableDrivers, " Returns: ", len(ReturnsWithin30Min))
        FiveMinDriversNeeded = math.ceil(prophetForecast5Min) - AvailableDrivers - len(ReturnsWithin5Min)
        ThirtyMinDriversNeeded = math.ceil(prophetForecast30Min) - AvailableDrivers - len(ReturnsWithin30Min)
        self.cursor.execute("UPDATE prediction_output SET five_min_drivers = %s, thirty_min_drivers = %s, total_drivers = %s, inactive_drivers = %s "
                            "WHERE date_and_time = '%s';" 
                            %(FiveMinDriversNeeded, ThirtyMinDriversNeeded, AvailableDrivers + len(self.Orders.getActiveOrders()), AvailableDrivers, self.todayTime))
        self.cargoDB.commit()
    
    #Uses the time table.
	#looks up the order status and estimated how long until that status will be delivered
	#assumes a driver will return after finishing an order and not clocking off
	def EstimateDriverReturnTime(self, orderID):     
        self.cursor.execute("SELECT status from order_statuses where order_id = '%s' and created_at <= '%s' order by id desc limit 1; " %(orderID, self.todayTimeUTC));
        status = self.cursor.fetchone()[0]
        
        self.cursor.execute("select location_id from orders where id = '%s'" %orderID)    
        location = self.cursor.fetchone()[0]
       
        self.cursor.execute("select location_id from time where location_id = '%s'" %location )
        timeLocationID = self.cursor.fetchone();
        
        if timeLocationID == None: #if location_id is not in table (EX new restaurant added)
            location = -1 #use default restaurant times (avg of all the other restaurants)
    
        
        self.cursor.execute("select created_at from order_statuses where order_id = '%s' and status = '%s'" % (orderID, status))
        timePassed = (self.todayTimeUTC - self.cursor.fetchone()[0]).total_seconds()   
        
        returnTime = 0
        if status == 'accepted':
            self.cursor.execute("SELECT Time_Till_Driver_Back from time where location_id = '%s';" % (location));
            returnTime = float(self.cursor.fetchone()[0]) - timePassed
            
        elif status == 'arrived':
            self.cursor.execute("SELECT Arrived_Time + Delivery_Time from time where location_id = '%s';" % (location));
            returnTime = float(self.cursor.fetchone()[0]) - timePassed
            
        elif status == 'delivering':
            self.cursor.execute("SELECT Delivery_Time from time where location_id = '%s';" % (location));
            returnTime = float(self.cursor.fetchone()[0]) - timePassed
    
        return returnTime
            
    def createPredictionTable(self):
        self.cursor.execute("CREATE TABLE prediction_output (id INT(11), " +
                                                            "date_and_time DATETIME, " +
                                                            "five_min_prediction DOUBLE, " +
                                                            "thirty_min_prediction DOUBLE, " +
                                                            "five_min_drivers INT(11), "+
                                                            "thirty_min_drivers INT(11), "+
                                                            "inactive_drivers INT(11), "+
                                                            "total_drivers INT(11))")
    def isSimulation(self):
        if self.isChecked.get() == 1:
            return True
        
        
def runProphet(today, isSim, thread_queue=None):
    cargoDB = pymysql.connect(host='localhost', user='root', password='password', db='cargo' )
    cursor = cargoDB.cursor()
        
    p = prophet.ProphetPrediction(isSim)
    
    if today.hour != 0:
            hourSpan = 31 - today.hour
    else:
        hourSpan = 7
            
    endOfDay = today + datetime.timedelta(hours=hourSpan) #set end of day to 2AM that night (next day's morning)
    if isSim:
        table = "simOrders"
    else:
        table = "orders"
    cursor.execute("SELECT delivered_at FROM " + table + " order by delivered_at desc limit 1")
    lastPredictionDate = cursor.fetchone()[0] #by default set the last prediction day to last order, this assumes the prediction has never been run before    
    cursor.execute("SELECT date_and_time FROM prediction_output order by date_and_time desc limit 1")
    result = cursor.fetchone()
    if result != None:
        lastPredictionDate = result[0] #if prediction has been run before, set to last time predicted  
    minutes_diff = math.ceil((endOfDay - lastPredictionDate).total_seconds() / 60.0) 
    p.runPrediction(minutes_diff) #run python to generate prediction from its last date to the end of day today
    #time.sleep(2)
    result = "Prophet Finished" 
    cargoDB.close()
    thread_queue.put(result)

    

root = Tk()
serverGUI = Server(root)
root.mainloop()