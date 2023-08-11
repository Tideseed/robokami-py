# Robokami Client Python SDK (robokami-py)

Robokami Client is the client to connect to Robokami IDM Server. Although it is not necessary to use this package to connect to RK-Server, it is recommended to use this package to as an initiation to Robokami IDM commands and structure.

_Note: Robokami Client is in alpha phase, so there will be breaking changes very soon._

+ For more detailed documentation, see [Wiki](https://github.com/Tideseed/robokami-py/wiki).  
+ For bugs, enhancements and other issues see [Issues](https://github.com/Tideseed/robokami-py/issues)
+ See [Discussions](https://github.com/Tideseed/robokami-py/discussions) to add feedback

## Installation

First download this repository or directly install it [pip](https://pypi.org).

```bash
pip install robokami-py
```

Alternatively you can choose to install from GitHub

```bash
pip install git+https://github.com/Tideseed/robokami-py.git
```

## Authentication

> **Warning**
> During the open beta of Robokami, it is recommended to use only test CAS (EKYS) accounts.

Prepare a JSON file in the following format. Your user should have IDM access privileges for both test server (`test-ekys`, `giptest`) and live server. (If you just want to do testing with live data you only need test user IDM access privileges.)

```json
{
    "trade": {
        "v2": false,
        "test_server": true,
        "username": "USERNAME",
        "password": "PASSWORD"
    },
    "stream": {
        "v2": false,
        "test_server": true,
        "stream_anonymous": false
    },
    "real_stream_test_trade": true
}
```

```python
import json 
with open("credfile.json", "r") as f:
    creds = json.load(f)
```

Alternatively, you can directly create the dictionary in Python.

```python
creds = {
    "trade": {
        "v2": False,
        "test_server": True,
        "username": "USERNAME",
        "password": "PASSWORD"
    },
    "stream": {
        "v2": False,
        "test_server": True,
        "stream_anonymous": False
    },
    "real_stream_test_trade": True
}
```

+ `v2`: Placeholder for IDM v2. Currently not active.
+ `test_server`: `true` for test server, `false` for live server.
+ `username`: Your EPIAS username.
+ `password`: Your EPIAS password.
+ `stream_anonymous`: `true` for anonymous stream, `false` for authenticated stream. The difference is you get to see private events (e.g. your own orders) in authenticated stream.
+ `real_stream_test_trade`: If `true` you will get streaming data from the live server but your orders will be executed in the test server and private events will be streamed from the test server. Although not perfect, this is the recommended setting for testing your algorithms.


## RKClient

Suppose your file is named `credfile.json`. You can load it and call the client by

```python
from robokami.main import RKClient

rkc = RKClient(creds=creds, initiate_stream=True)
```

## Streaming Data

Stream data uses SSE (Server-Sent Events) protocol. You can simply access the stream by

```python
for event in rkc.stream_client.events():
    e_d = event.__dict__
    print(e_d)
```

## Trading

### Orders

You can place orders and update orders. Suppose you are going to send a new order for PH23052010 (i.e, hourly contract for 2023-05-20 for 10:00-11:00)

```python
order_d = {
    "c": "PH23070112",
    "position": "bid",
    "price": 100,
    "lots": 1,
    "order_status": "active",
    "order_note": "RK test order"
}
```

+ `c`: Name of the contract. Hourly contracts are in PHyyMMDDHH format. Block contracts are in PByyMMDDHH-XX format where XX is the number of hours.
+ `position`: `bid` for buy, `ask` for sell.
+ `price`: Price of the order.
+ `lots`: Number of lots.
+ `order_status`: `active` for active orders, `inactive` for inactive orders.
+ `order_note`: order_note for the order.


Then simply place the order using `rkc`.

```python
res = rkc.place_order(order_d)
```

If the result is successful, you can obtain its order id.

```python
if res["status"] == "success":
    order_id = res["order_id"]
```

You can also update the order by using the order id and changing `order_d`.

```python
my_order["price"] = 101
res = rkc.update_order(order_id, my_order)
```

### Other Trade Commands

`place_order` and `update_order` are just wrappers for `trade` command. You can use `trade` command directly to place orders, update orders, cancel orders, and get order status.

```python
rkc.trade_command(command, d)
```

where `command` is a command phrase (e.g. `"place_order"`, `"update_order"`) and `d` is the dictionary of parameters required by the command.

+ `limit_details`: With this command you can get the limit details (e.g. min/max price, lots etc.) of your account.
+ `net_positions`: Get your net position with this command. You need to specify the contract type `python {"contract_type":"hourly"}` or `python {"contract_type":"block"}` in the parameter dictionary.
+ `orders_by_id`: You can get order details by order ids. You can add a list `python {"order_ids": ["order_id1", "order_id2"]}` to the parameter dictionary.
+ `contract_details`: You can get details about contracts. (p.s. not very useful)
+ `order_detail`: Similar to `orders_by_id` but with more detail.
+ `order_book`: Get the order book for hourly and block offers. 
+ `open_contracts`: Returns the list of open contracts.
+ `organization_orders`: Returns the list of orders belonging to the organization. You need to specify `contract_type` (i.e. "hourly", "block", or "both"). You can filter by time using `after_dt` parameter and order status by using `order_status` parameter (values are "active","cancelled","passive","matched", and "partially_matched").
+ `saved_order_notes`: Returns saved order notes.
+ `matched_orders`: Returns matched orders. You need to specify `start_date` and `end_date` parameters.
+ `make_active_orders_passive`: Make all active orders passive.
+ `make_passive_orders_active`: Make all passive orders active.
