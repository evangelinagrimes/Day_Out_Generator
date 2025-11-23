

class Event: 
    '''
    Represents a local business or activity event with relevant details.
    
    This class stores information about restaurants, activities, and other 
    establishments retrieved from the Google Places API, including business 
    details, hours, pricing, and review information.
    
    Attributes:
        type (str): The category/type of event (e.g., 'restaurant', 'activity', 'dessert')
        status (str): The current business status (e.g., 'OPERATIONAL', 'CLOSED_TEMPORARILY')
        business (str): The name of the business or establishment
        businessHours (dict): Dictionary containing opening hours information
        address (str): The formatted street address of the business
        website (str): The business website URL
        priceLevel (str): Price level indicator (e.g., 'PRICE_LEVEL_INEXPENSIVE', 'N/A')
        reviewSummary (str): Summary of customer reviews
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

    def __str__(self):
        return f"----------| {self.business} |-----------\nTYPE: {self.type}\nSTATUS: {self.status}\nADDRESS: {self.address}\nOPEN HOURS: {self.businessHours}\nWEBSITE: {self.website}\nPRICE: {self.priceLevel}\nREVIEW SUMMARY: {self.reviewSummary}\n{'--' * 20}"