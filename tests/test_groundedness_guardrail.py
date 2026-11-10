import pytest
from app.guardrails.groundedness import check_groundedness
context = (
    "Customers can return eligible products within 7 days of delivery. "
    "Returned items must include all original accessories, manuals, tags, and packaging."
)

def test_correct_answer_is_grounded():
    answer = "Customers can return eligible products within 7 days of delivery."
    assert check_groundedness(answer, context) is True

def test_correct_answer():
    answer="Bitcoin is acccepted"
    assert check_groundedness(answer,context) is False

@pytest.mark.xfail(reason="Word overlap can't detect wrong numbers")
def test_correct_answer_is_grounded():
    answer = "Customers can return eligible products within 30 days of delivery."
    assert check_groundedness(answer, context) is False

@pytest.mark.xfail(reason="Word overlap can't detect negation")
def test_contradiction_is_not_grounded():
    answer = "Customers cannot return any products after delivery."
    assert check_groundedness(answer, context) is False


def test_lifetime_warranty_claim_is_not_grounded():
    answer="You get a lifetime warranty and free repairs on every product"
    assert check_groundedness(answer,context) is False