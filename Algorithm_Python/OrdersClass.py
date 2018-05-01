#used to track submitted orders, and active orders
#carGO probably already has a way to keep track of this

class Orders:
    activeOrders = {}
    processingOrders = {}
    finishedOrders = {}
    
    def addProcOrder(self, order, location):
        self.processingOrders[order] = location
    
    def removeProcOrder(self, order):
        del self.processingOrders[order]
        
    def addActiveOrder(self, order, location):
        self.activeOrders[order] = location
        
    def removeActiveOrder(self, order):
        del self.activeOrders[order]
        
    def addFinOrder(self, order, location):
        self.finishedOrders[order] = location
    
    def removeFinOrders(self):
        self.finishedOrders = {}
        
    def getActiveOrders(self):
        return self.activeOrders
        
    def getFinOrders(self):
        return self.finishedOrders
    
    def getProcOrders(self):
        return self.processingOrders
    
    def getActiveLocationID(self, order):
        return self.activeOrders.get(order)
        
    def getProcLocationID(self, order):
        return self.processingOrders.get(order)
