from .BaseAPI import BaseAPI, GET, POST, PUT, DELETE

# Transaction object to store new transaction parameters
class Transaction(object):
    def __init__(self, amountUSD = None, cryptoSymbol = None, lightningNetwork = None):
        self.amountUSD = amountUSD
        self.cryptoSymbol = cryptoSymbol
        self.lightningNetwork = lightningNetwork

# Transaction service to handle object functions
class TransactionService(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(TransactionService, self).__init__(*args, **kwargs)
    
    # List all transactions as an object array
    def List(self, page = 1, pPage = 25):
        # If statement block to handle pagination input errors
        if type(page) is not type(int()) and type(page) is not type(int()):
            return None, "Invalid 'page' & 'per page' values"
        elif type(page) is not type(int()):
            return None, "Invalid 'page' value"
        elif type(pPage) is not type(int()):
            return None, "Invalid 'per page' value"
        
        url = "transactions?page={}&items={}".format(page, pPage)

        # Get data from API
        data = self.getData(url)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None
    
    # Show transaction object by given id
    def Show(self, id = None):
        # Check if id was passed
        if id is None or id == "":
            return None, "No Transaction 'id' was provided"

        url = "transactions/{}".format(id)

        # Get data from API
        data = self.getData(url)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None
    
    # Create a new transaction from given transaction object
    def Create(self, transaction):
        # Check if transaction object was passed and is valid
        if type(transaction) is not type(Transaction()):
            return None, "No transaction was provided"
        if transaction.amountUSD is None:
            return None, "No transaction 'amountUSD' was provided"
        
        # Format the transaction to be processed by the API
        newTransactionParams = transaction.__dict__

        # Send data to API and get response
        data = self.getData("transactions", type=POST, params=newTransactionParams)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None
