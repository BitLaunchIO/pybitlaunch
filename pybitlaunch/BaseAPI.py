import sys
import requests
import logging
import json
import os
from . import __name__, __version__

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

# Set globals for http methods
GET = "GET"
POST = "POST"
DELETE = "DELETE"
PUT = "PUT"

class Error(Exception):
    """Base exception class for this module"""
    pass

class TokenError(Error):
    pass

class DataReadError(Error):
    pass

class JSONReadError(Error):
    pass

class NotFoundError(Error):
    pass

# Base class for API objects
class BaseAPI(object):
    def __init__(self, token = "", *args, **kwargs):
        self.baseURI = "https://app.bitlaunch.io/api/"
        self.token = token
        self._log = logging.getLogger(__name__)
        
        self._session = requests.Session()

        for attr in kwargs.keys():
            setattr(self, attr, kwargs[attr])

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_log']
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self._log = logging.getLogger(__name__)

    def __performRequest(self, url, type=GET, params=None):
        # Check if extra params were passed
        if params is None:
            params = {}
        
        # Handle if no token was provided
        if not self.token:
            raise TokenError("No token was provided. Please provide a valid token.")

        url = urlparse.urljoin(self.baseURI, url)

        # Anonymous function to return a value passed
        identity = lambda x: x

        # Anonymous function to convert passed value to JSON
        json_dumps = lambda x: json.dumps(x)

        header = {"Content-type": "application/json"}

        # Define how each 'Method' is used 
        lookup = {
            GET: (self._session.get, header, "params", identity),
            POST: (self._session.post, header, "data", json_dumps),
            PUT: (self._session.put, header, "data", json_dumps),
            DELETE: (self._session.delete, header, "data", json_dumps)
        }

        # Get required values for given 'Method'
        requestsMethod, headers, payload, transform = lookup[type]

        agent = "{}/{} {}/{}".format('pybitlaunch', __version__, requests.__name__, requests.__version__)

        # Update headers with token and agent
        headers.update({"Authorization": "Bearer " + self.token, "User-Agent": agent})

        # Package values from given 'Method' to be passed to requests method
        kwargs = {"headers": headers, payload: transform(params)}

        # Query API and return response
        return requestsMethod(url, **kwargs)
    
    def getData(self, url, type=GET, params=None):
        # Set params to empty dictionary if None
        if params is None:
            params = dict()

        # Query the API
        req = self.__performRequest(url, type, params)
        if req.status_code == 204:
            return True

        if req.status_code == 404:
            raise NotFoundError()

        try:
            # Convert reponse to json
            data = req.json()
        except ValueError as e:
            if req.status_code != 200:
                raise JSONReadError("Read failed from BitLaunch: %s" % str(e))
            else:
                # Return None if Query was success but has no return values
                return None
        
        if data is None:
            return ""
        else:
            return data

    def __str__(self):
        return "<%s>" % self.__class__.__name__

    def __unicode__(self):
        return u"%s" % self.__str__()

    def __repr__(self):
        return str(self)
