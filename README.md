# pybitlaunch
pybitlaunch is a python library for accessing the BitLaunch API.

You can view BitLaunch API docs here: https://developers.bitlaunch.io/

## Install
### Source
```sh
git clone https://github.com/bitlaunchio/pybitlaunch.git
cd pybitlaunch
python setup.py install
```

### PIP
```sh
pip install -U pybitlaunch
```

## Usage
```python
import pybitlaunch
```

### Authentication

You must use your API Token to authenticate with BitLaunch API. You can (re)generate your access token on the BitLaunch [API Page](https://app.bitlaunch.io/account/api).

You can then use your token to create a new client.

```python
client = pybitlaunch.Client(token)
```

## Documentation

For a comprehensive list of examples, check out the [API documentation](https://developers.bitlaunch.io/).

### Account
#### Show
```python
accountObj = client.Account.Show()
if accountObj is not None:
    # process data
```
#### Usage
```python
usage = client.Account.Usage("2020-10")
if usage is not None:
    # process data
```
#### History
```python
history = client.Account.History(1, 25)
if history is not None:
    # process data
```

### SSHKeys
#### List
```python
sshKeyObjArray = client.SSHKeys.List()
if sshKeyObjArray is not None:
    # process data
```
#### Create
```python
newKey = pybitlaunch.SSHKey(name="sshkey_name", content="sshkey_rsa_pub")

sshKeyObj, err = client.SSHKeys.Create(newKey)
if err is not None:
    # handle error
else:
    # process data
```
#### Delete
```python
err = client.SSHKeys.Delete(sshKeyObj.id)
if err is not None:
    # handle error
```

### Transactions
#### List
```python
transactionObjArray, err = client.Transactions.List(page=1, pPage=25) # Optional: page, pPage
if err is not None:
    # handle error
else:
    # process data
```
#### Show
```python
transactionObj, err = client.Transactions.Show(transactionObj.id)
if err is not None:
    # handle error
else:
    # process data
```
#### Create
```python
newTransaction = pybitlaunch.Transaction(
    amountUSD = 20,
    cryptoSymbol = None, # Optional
    lightningNetwork = None # Optional
)

transactionObj, err = client.Transactions.Create(newTransaction)
if err is not None:
    # handle error
else:
    # process data
```

### CreateOptions
#### Show
```python
createOptionsArray, err = client.CreateOptions.Show(hostID)
# createOptionsArray = ['hostID', 'image', 'region', 'size', 'available', 'bandwidthCost', 'planTypes', 'hostOptions']
if err is not None:
    # handle error
else:
    # process data
```

### Servers
#### List
```python
serverObj, err = client.Servers.List()
if err is not None:
    # handle error
else:
    # process data
```
#### Show
```python
serverObj, err = client.Servers.Show(serverObj.id)
if err is not None:
    # handle error
else:
    # process data
```
#### Create
```python
newServer = pybitlaunch.Server(
    name = "myServer",
    hostID = 4,
    hostImageID = "10000",
    sizeID = "nibble-1024",
    regionID = "lon1",
    password = "MySecurePassword", # Optional must use sshKeys instead
    sshKeys = [sshKeyObj["id"]], # Optional must use password instead
    initscript = None # Optional
)

serverObj, err = client.Servers.Create(serverObj)
if err is not None:
    # handle error
else:
    # process data
```
#### Destroy
```python
err = client.Servers.Destroy(serverObj.id)
if err is not None:
    # handle error
```
#### Rebuild
```python
createOpts, err = client.CreateOptions.Show(4)
if err is not None:
    # handle error

newImage = pybitlaunch.RebuildImage(
    createOpts["image"][0]["versions"][1]["id"],
    createOpts["image"][0]["versions"][1]["description"]
)

err = client.Servers.Rebuild(serverObj.id, newImage)
if err is not None:
    # handle error
```
#### Resize
```python
err = client.Servers.Resize(serverObj.id, "nibble-2048")
if err is not None:
    # handle error
```
#### Restart
```python
err = client.Servers.Restart(serverObj.id)
if err is not None:
    # handle error
```
#### Protection
```python
server, err = client.Servers.Protection(serverObj.id, True)
if err is not None:
    # handle error
else:
    # process data
```
#### SetPorts
```python
ports = [
    pybitlaunch.Port(1234, "tcp"),
    pybitlaunch.Port(1234, "udp"),
    pybitlaunch.Port(1235, "tcp"),
]

server, err = client.Servers.SetPorts(serverObj.id, ports)
if err is not None:
    # handle error
else:
    # process data
```