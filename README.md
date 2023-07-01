# Robokami Client Python SDK (robokami-py)

Robokami Client is the client to connect to Robokami IDM Server. Although it is not necessary to use this package to connect to RK-Server, it is recommended to use this package to as an initiation to Robokami IDM commands and structure.

_Note: Robokami Client is in alpha phase, so there will be breaking changes very soon._

## Installation

First download this repository

```bash
pip install pip install git+https://github.com/Tideseed/robokami-py.git
```

## Authentication

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

+ `v2`: Placeholder for IDM v2. Currently not active.
+ `test_server`: `true` for test server, `false` for live server.
+ `username`: Your username.
+ `password`: Your password.
+ `stream_anonymous`: `true` for anonymous stream, `false` for authenticated stream. The difference is you get to see private events (e.g. your own orders) in authenticated stream.
+ `real_stream_test_trade`: If `true` you will get streaming data from the live server but your orders will be executed in the test server and private events will be streamed from the test server. Although not perfect, this is the recommended setting for testing your algorithms.

## RKClient

Suppose your file is named `credfile.json`. You can load it and call the client by

```python
from robokami.main import RKClient

with open("credfile.json", "r") as f:
    creds = json.load(f)

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
    "contract": "PH23070112",
    "position": "bid",
    "price": 100,
    "lots": 1,
    "status": "active",
    "explanation": "RK test order"
}
```

+ `contract`: Name of the contract. Hourly contracts are in PHyyMMDDHH format. Block contracts are in PByyMMDDHH-XX format where XX is the number of hours.
+ `position`: `bid` for buy, `ask` for sell.
+ `price`: Price of the order.
+ `lots`: Number of lots.
+ `status`: `active` for active orders, `inactive` for inactive orders.
+ `explanation`: Explanation for the order.


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