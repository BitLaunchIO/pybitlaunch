from .Account import AccountService
from .SSHKeys import SSHKeyService, SSHKey
from .Transactions import TransactionService, Transaction
from .Servers import ServerService, Server, Port, RebuildImage
from .CreateOptions import CreateOptionsService
from .BaseAPI import BaseAPI

# Client object to interface with the API
class Client(object):
    def __init__(self, t = "", *args, **kwargs):
        # Add services to Client object
        self.Account = AccountService(t)
        self.SSHKeys = SSHKeyService(t)
        self.Transactions = TransactionService(t)
        self.Servers = ServerService(t)
        self.CreateOptions = CreateOptionsService(t)

