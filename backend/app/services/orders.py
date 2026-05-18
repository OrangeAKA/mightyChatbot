# STUB: mock order database — replace with Supabase query on Day 3

_ORDERS: dict[str, dict] = {
    "ORD-001": {"status": "in_transit", "eta": "May 20, 2026", "item": "Rewards Card"},
    "ORD-002": {"status": "delivered", "delivered_on": "May 15, 2026", "item": "Gift Voucher"},
    "ORD-003": {"status": "processing", "eta": "May 22, 2026", "item": "Cashback Statement"},
}


def lookup(order_id: str) -> dict | None:
    return _ORDERS.get(order_id.upper())


def reply_for(order_id: str) -> str:
    order = lookup(order_id)
    if order is None:
        return f"I couldn't find order {order_id}. Please double-check the order number."
    s = order["status"]
    if s == "in_transit":
        return f"Order {order_id} ({order['item']}) is in transit — expected by {order['eta']}."
    if s == "delivered":
        return f"Order {order_id} ({order['item']}) was delivered on {order['delivered_on']}."
    if s == "processing":
        return f"Order {order_id} ({order['item']}) is being processed — ships around {order['eta']}."
    return f"Order {order_id} status: {s}."
