from .BaseAPI import BaseAPI, GET, POST, PUT, DELETE

# SSH key object to store new key parameters
class SSHKey(object):
    def __init__(self, name = None, content = None):
        self.name = name
        self.content = content

# SSH key service to handle object functions
class SSHKeyService(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(SSHKeyService, self).__init__(*args, **kwargs)
    
    # List all SSH keys on account
    def List(self):
        # Get data from API
        data = self.getData("ssh-keys")
        sshKey = data["keys"]
        return sshKey
    
    # Create new SSH key
    def Create(self, key = None):
        # If statement block to check for a valid new SSH key object
        if type(key) is not type(SSHKey()):
            return None, "No key was provided"
        if key.name is None and key.content is None:
            return None, "No SSH Key 'name' & 'content' provided"
        elif key.name is None:
            return None, "No SSH Key 'name' was provided"
        elif key.content is None:
            return None, "No SSH Key 'content' was provided"
        
        # Convert new SSH key object into json friendly format
        newKeyParams = key.__dict__

        # Send data to API and get response
        data = self.getData("ssh-keys", type=POST, params=newKeyParams)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None
    
    # Delete an SSH key by given id
    def Delete(self, id = None):
        # Check if id is passed
        if id is None or id == "":
            return "No SSH Key 'id' was provided"
        
        url = "ssh-keys/{}".format(id)

        # Send DELETE request to API with given id and get response
        data = self.getData(url, type=DELETE)

        # Return message response or None
        if data is not None:
            if "message" in data:
                return data["message"]
        
        return None

        

