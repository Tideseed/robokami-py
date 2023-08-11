import copy
from datetime import datetime
from robokami.main import RKClient


def prepare_order(
    d: dict,
    price: int | float = None,
    lots: int = None,
    demo: bool = True,
    order_note: str = None,
    order_status: str = None,
):
    """Wrapper function for sending trade order.

    Args:
        d (dict): Order dictionary
        price (int | float, optional): Price of the order. Defaults to None.
        lots (int, optional): Number of lots. Defaults to None.
        demo (bool, optional): If True, order is placed in demo mode. Defaults to True.
        order_note (str, optional): Order note. Defaults to None.
        order_status (str, optional): Order status. Defaults to None.

    Returns:
        dict: Order dictionary
        str: Command phrase
    """
    d2 = copy.deepcopy(d)
    trade_command_phrase = "pass"
    order_id = d2.get("order_id", None)

    if demo or order_id is None or order_id == "DEMO":
        d2["order_id"] = "DEMO" if demo else None
        d2["price"] = price
        d2["lots"] = lots
        d2["order_status"] = "active" if order_status is None else order_status
        if demo:
            d2["ts"] = datetime.now().timestamp()
        else:
            trade_command_phrase = "place_order"
    else:
        update_order = False
        if price != d["price"] and price is not None:
            d2["price"] = price
            update_order = True
        if lots != d["lots"] and lots is not None:
            d2["lots"] = lots
            update_order = True
        if order_status != d["order_status"] and order_status is not None:
            d2["order_status"] = order_status
            update_order = True
        if update_order:
            trade_command_phrase = "update_order"

    if order_note is not None:
        d["order_note"] = order_note

    return d2, trade_command_phrase


def send_trade_order(client: RKClient, d: dict, command_phrase: str):
    """Wrapper function for sending trade order.

    Args:
        client (Client): Client object
        d (dict): Order dictionary
        command_phrase (str): Command phrase
    """
    if command_phrase == "place_order":
        res = client.place_order(d)

        if res["status"] == "success":
            d["order_id"] = res["order_id"]
            d["ts"] = datetime.now().timestamp()
        else:
            raise Exception("Order could not be placed")

    elif command_phrase == "update_order":
        res = client.update_order(
            d=d,
        )
        if res["status"] == "success":
            # d["order_id"] = res[0]["response"]
            d["ts"] = datetime.now().timestamp()
        elif res["detail"] == "partial_match_occured":
            d["order_status"] = "cancelled"
            res = client.update_order(d=d)
            if res["status"] == "success":
                d["order_id"] = None
        elif res["detail"] == "order_cannot_be_updated":
            d["order_id"] = None
        else:
            raise Exception("Order could not be placed")
    elif command_phrase == "cancel_order":
        d["order_status"] = "cancelled"
        res = client.update_order(d=d)
        if res["status"] == "success":
            d["order_id"] = None

    else:
        raise Exception("Invalid command phrase")

    return res, d
