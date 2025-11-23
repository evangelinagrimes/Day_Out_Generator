

class Event: 
    '''

    
    
    '''

    def __init__(self, type, status, business, businessHours, address, website, priceLevel, reviewSummary): 
        self.type = type
        self.status = status
        self.business = business
        self.businessHours = businessHours
        self.address = address
        self.website = website
        self.priceLevel = priceLevel
        self.reviewSummary = reviewSummary

    def getType(self):
        return self.type

    def getBusiness(self):
        return self.business
    
    def getAddress(self):
        return self.address
    
    def getWebsite(self): 
        return self.website
    
    def getPriceLevel(self):
        return self.priceLevel
    
    def getReviewSummary(self):
        return self.reviewSummary
    
    def getBusinessHours(self):
        return self.businessHours
    
    def getStatus(self):
        return self.status

    

    