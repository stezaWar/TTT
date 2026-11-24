from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.models import RefundRequest


def test_valid_refund_request():
    refund = RefundRequest(
        order_id="A-100",
        reason="Товар пришёл с браком",
        refund_amount=Decimal("49.90"),
    )
    assert refund.refund_amount == Decimal("49.90")


def test_short_reason_is_rejected():
    with pytest.raises(ValidationError):
        RefundRequest(order_id="A-100", reason="брак", refund_amount=Decimal("10"))


def test_non_positive_amount_is_rejected():
    with pytest.raises(ValidationError):
        RefundRequest(
            order_id="A-100",
            reason="Не подошёл размер",
            refund_amount=Decimal("-5"),
        )
