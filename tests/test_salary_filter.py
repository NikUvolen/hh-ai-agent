import pytest

from vacancy_filter import salary_rejection_reason


@pytest.mark.parametrize(("text", "expected"), [
    ("от 60 000 до 79 000 ₽ за месяц", True),
    ("60 000 – 80 000 ₽ за месяц", False),
    ("до 79 999 ₽ за месяц", True),
    ("от 50 000 ₽ за месяц", False),
    ("79 000 ₽ за месяц", True),
    ("70 000 ₽ за смену", False),
    ("70 000 USD за месяц", False),
    ("70 000 ₽", False),
    ("100 000 – 50 000 ₽ за месяц", False),
    ("1 20 ₽ за месяц", False),
    ("", False),
    ("от 50 000 до 70 000 ₽ за месяц плюс бонус 30 000 ₽", False),
])
def test_salary_filter_rejects_only_clear_low_monthly_maximum(text, expected):
    assert bool(salary_rejection_reason(text, 80_000)) is expected


def test_salary_filter_disabled():
    assert salary_rejection_reason("до 10 000 ₽ за месяц", 0) is None
