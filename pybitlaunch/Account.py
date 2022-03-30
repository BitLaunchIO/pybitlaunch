from .BaseAPI import BaseAPI

# Account object service to handle object functions
class AccountService(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(AccountService, self).__init__(*args, **kwargs)

    # Show account information
    def Show(self):
        # Get data from API
        data = self.getData("user")
        return data

    # View Usage of account
    def Usage(self, period = "latest"):
        # Get data from API
        data = self.getData("usage?period={}".format(period))
        return data
    
    # View History of account
    def History(self, page = 1, items = 25):
        # Get data from API
        data = self.getData("security/history?page={}&items={}".format(page, items))
        return data