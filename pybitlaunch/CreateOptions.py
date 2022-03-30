from .BaseAPI import BaseAPI, GET, POST, PUT, DELETE

# CreateOptions object to handle object functions
class CreateOptionsService(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(CreateOptionsService, self).__init__(*args, **kwargs)
    
    # Show CreateOptions for available server options 
    def Show(self, id = None):
        # Handle no id case
        if id is None or str(id) == "":
            return None, "No 'hostID' was provided"
        
        url = "hosts-create-options/{}".format(id)

        # Get data from API
        data = self.getData(url)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None