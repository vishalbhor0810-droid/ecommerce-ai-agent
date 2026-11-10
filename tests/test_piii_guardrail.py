
import pytest
from app.guardrails.pii import mask_pii


def test_masks_email():
    assert mask_pii("My email is priya.nair@example.com") == "My email is ***EMAIL***"

def test_masks_plain_phone():
    assert mask_pii("Call me on 9876543210") == "Call me on ***PHONE***"

def test_masks_phone_with_plus91_space():
    assert mask_pii("Call +91 9876543210 now") == "Call ***PHONE*** now"

def test_masks_phone_with_plus91_dash():
    assert mask_pii("Call +91-9876543210") == "Call ***PHONE***"

def test_masks_phone_with_plus91_no_space():
    assert mask_pii("My number is +919876543210") == "My number is ***PHONE***"

def test_keeps_order_id():
    assert mask_pii("Where is ORD1002?") == "Where is ORD1002?"

def test_keeps_long_order_id():
    assert mask_pii("Where is ORD9876543210?") == "Where is ORD9876543210?"

def test_keeps_amount():
    assert mask_pii("I paid 4911 rupees") == "I paid 4911 rupees"

def test_keeps_long_card_like_number():
    assert mask_pii("Card number 12349876543210") == "Card number 12349876543210"

@pytest.mark.xfail(reason="Spaced phone numbers are not detected - known limitation")
def test_masks_spaced_phone():
    assert mask_pii("Call 99208 98194") == "Call ***PHONE***"