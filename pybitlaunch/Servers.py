from .BaseAPI import BaseAPI, GET, POST, PUT, DELETE
from .SSHKeys import SSHKey

# Server object to store a new servers parameters
class Server(object):
    def __init__(self, name = None, hostID = None, hostImageID = None, sizeID = None, regionID = None, sshKeys = None, password = None, initscript = None):
        self.name = name
        self.hostID = hostID
        self.hostImageID = hostImageID
        self.sizeID = sizeID
        self.regionID = regionID
        self.sshKeys = sshKeys
        self.password = password
        self.initscript = initscript

# RebuildImage object to store new image parameters
class RebuildImage(object):
    def __init__(self, hostImageID = None, imageDescription = None):
        self.hostImageID = hostImageID
        self.imageDescription = imageDescription

# Port object to store enabled port
class Port(object):
    def __init__(self, portNumber = None, protocol = None):
        self.portNumber = portNumber
        self.protocol = protocol

# Server object service to handle object functions
class ServerService(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(ServerService, self).__init__(*args, **kwargs)
    
    # List all servers on account
    def List(self):
        # Get data from API
        data = self.getData("servers")

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None

    # Send request to create a new server
    def Create(self, server):
        # If statement block to check for valid server object
        if type(server) is not type(Server()):
            return None, "No server was provided"
        
        if server.name is None or str(server.name) == "":
            return None, "No server 'name' was provided"
        elif server.hostID is None:
            return None, "No server 'hostID' was provided"
        elif server.hostImageID is None or server.hostImageID == "":
            return None, "No server 'hostImageID' was provided"
        elif server.sizeID is None or str(server.sizeID) == "":
            return None, "No server 'sizeID' was provided"
        elif server.regionID is None or str(server.regionID) == "":
            return None, "No server 'regionID' was provided"
        
        if type(server.hostID) != type(int()):
            return None, "Invalid server 'hostID' was provided"
        elif type(server.hostImageID) != type(str()):
            return None, "Invalid server 'hostImageID' was provided"

        if server.sshKeys is not None and len(server.sshKeys) == 0:
            return None, "Invalid SSH Key was provided"
        elif server.password is not None and str(server.password) == "":
            return None, "No server 'password' provided"
        elif (server.password is None or str(server.password) == "") and (server.sshKeys is None or len(server.sshKeys) == 0):
            return None, "No server 'sshKeys' or 'password' provided"
        
        # Store server object to be processed by BaseAPI to submit the new server to the API
        newServerParams = {
            "server": server.__dict__
        }

        # Send data to API and get response
        data = self.getData("servers", type=POST, params=newServerParams)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None
    
    # Show a server by the given id
    def Show(self, id = None):
        # Check if id is passed
        if id is None or id == "":
            return None, "No server 'id' was provided"

        url = "servers/{}".format(id)

        # Get data from API
        data = self.getData(url)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None
    
    # Destroy a server by the given id
    def Destroy(self, id = None):
        # Check if id is passed
        if id is None or id == "":
            return "No server 'id' was provided"
        
        url = "servers/{}".format(id)

        # Send DELETE request to API with given id and get response
        data = self.getData(url, type=DELETE)

        # Return message response if there is one
        if data is not None:
            if "message" in data:
                return data["message"]
        
        return None
    
    # Rebuild a server
    def Rebuild(self, id = None, imgData = None):     
        # Check if id is passed
        if id is None or id == "":
            return "No server 'id' was provided"
        
        # If statement block to check for valid RebuildImage object
        if type(imgData) is not type(RebuildImage()):
            return "No image data was provided"
        if imgData.hostImageID is None or str(imgData.hostImageID) == "":
            return "No image 'hostImageID' was provided"
        elif imgData.hostImageID is None or str(imgData.hostImageID) == "":
            return "No image 'imageDescription' was provided"
           
        # Send data to API and get response
        data = self.getData("servers/{}/rebuild".format(id), type=POST, params=imgData.__dict__)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return data["message"]
        
        return None
    
    # Resize a server
    def Resize(self, id = None, sizeID = None):     
        # Check if id is passed
        if id is None or id == "":
            return "No server 'id' was provided"
        
        # If statement block to check for valid RebuildImage object
        if sizeID is None or sizeID == "":
            return "No image data was provided"
        
        resizeParams = {
            "size": sizeID
        }
           
        # Send data to API and get response
        data = self.getData("servers/{}/resize".format(id), type=POST, params=resizeParams)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return data["message"]
        
        return None
    
    # Restart a server
    def Restart(self, id = None):     
        # Check if id is passed
        if id is None or id == "":
            return "No server 'id' was provided"

        # Send data to API and get response
        data = self.getData("servers/{}/restart".format(id), type=POST)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return data["message"]
        
        return None
    
    # Change the protection status of a server
    def Protection(self, id = None, enabled = None):     
        # Check if id is passed
        if id is None or id == "":
            return None, "No server 'id' was provided"

        # Check if enabled was provided and is a boolean
        if enabled is None:
            return "Boolean 'enabled' was not provided"
        elif type(enabled) is not type(True):
            return None, "Invalid 'enabled' was provided"

        region = lambda e: "bvm-lux" if enabled else ""

        protectParams = {
            "enable": enabled,
            "region": region(enabled)
        }

        # Send data to API and get response
        data = self.getData("servers/{}/protection".format(id), type=POST, params=protectParams)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None

    # SetPorts sets the enabled ports on a server for DDoS protection (Needs Protection enabled)
    def SetPorts(self, id = None, ports = None):     
        # Check if id is passed
        if id is None or id == "":
            return None, "No server 'id' was provided"

        # Check if enabled was provided and is a boolean
        if ports is None:
            return None, "No 'ports' provided"
        
        portList = []

        for p in ports:
            portList.append(p.__dict__)

        # Send data to API and get response
        data = self.getData("servers/{}/protection/ports".format(id), type=POST, params=portList)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None    
