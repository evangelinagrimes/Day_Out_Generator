

class Event: 
    '''

    
    
    '''

    def __init__(self, type, business, address, website=None, price=None, topReview=None): 
        self.type = type
        self.business = business
        self.address = address
        self.website = website
        self.price = price
        self.topReview = topReview

    def getType(self):
        return self.type

    def getBusiness(self):
        return self.business
    
    def getAddress(self):
        return self.address
    
    def getWebsite(self): 
        return self.website
    
    def getPrice(self):
        return self.price
    
    def getTopReview(self):
        return self.topReview

    

    