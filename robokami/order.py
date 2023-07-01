import copy
from datetime import datetime


def prepare_order(
    d,
    price=None,
    lots=None,
    demo=True,
    order_note=None,
    status=None,
):
    d2 = copy.deepcopy(d)
    trade_command_phrase = "pass"
    order_id = d2.get("order_id", None)

    if demo or order_id is None or order_id == "DEMO":
        d2["order_id"] = "DEMO" if demo else None
        d2["price"] = price
        d2["lots"] = lots
        d2["status"] = "active" if status is None else status
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
        if status != d["status"] and status is not None:
            d2["status"] = status
            update_order = True
        if update_order:
            trade_command_phrase = "update_order"

    if order_note is not None:
        d["explanation"] = order_note

    return d2, trade_command_phrase


def send_trade_order(client, d, command_phrase):
    # if "lots" in d.keys():
    #     d["lots"] = abs(d["lots"])

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
            d["status"] = "cancelled"
            res = client.update_order(d=d)
            if res["status"] == "success":
                d["order_id"] = None
        elif res["detail"] == "order_cannot_be_updated":
            d["order_id"] = None
        else:
            raise Exception("Order could not be placed")
    elif command_phrase == "cancel_order":
        d["status"] = "cancelled"
        res = client.update_order(d=d)
        if res["status"] == "success":
            d["order_id"] = None

    else:
        raise Exception("Invalid command phrase")

    return res, d
