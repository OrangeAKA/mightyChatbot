from app.services.orders import lookup, reply_for


def test_lookup_known_order():
    assert lookup("ORD-001")["status"] == "in_transit"


def test_lookup_case_insensitive():
    assert lookup("ord-002") is not None


def test_lookup_unknown_returns_none():
    assert lookup("ORD-999") is None


def test_reply_in_transit():
    assert "in transit" in reply_for("ORD-001")
    assert "May 20, 2026" in reply_for("ORD-001")


def test_reply_delivered():
    assert "delivered" in reply_for("ORD-002")


def test_reply_processing():
    assert "processed" in reply_for("ORD-003")


def test_reply_unknown_order():
    assert "couldn't find" in reply_for("ORD-999")
