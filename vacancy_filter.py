import re


def salary_rejection_reason(text: str, minimum_rub: int) -> str | None:
    """Reject only unambiguous monthly RUB amounts with a known upper bound."""
    if minimum_rub <= 0:
        return None
    normalized = re.sub(r"[\u00a0\u202f]", " ", text.strip().casefold())
    amount = r"((?:\d{1,3}(?: \d{3})+|\d+))"
    pattern = rf"(?:от\s+{amount}\s+до\s+{amount}|{amount}\s*[–—-]\s*{amount}|до\s+{amount}|{amount})\s*(?:₽|руб\.?|рублей)\s*(?:на руки|до вычета налогов)?\s*за месяц\s*(?:на руки|до вычета налогов)?"
    match = re.fullmatch(pattern, normalized)
    if not match:
        return None
    groups = match.groups()
    if groups[0] and int(groups[0].replace(" ", "")) > int(groups[1].replace(" ", "")):
        return None
    if groups[2] and int(groups[2].replace(" ", "")) > int(groups[3].replace(" ", "")):
        return None
    maximum = next((value for value in (groups[1], groups[3], groups[4], groups[5]) if value), None)
    if maximum is not None and int(maximum.replace(" ", "")) < minimum_rub:
        return "salary_below_minimum"
    return None


def title_rejection_reason(
    title: str, excluded_positions: tuple[str, ...]
) -> str | None:
    normalized = title.casefold()
    return next(
        (
            word
            for word in excluded_positions
            if word.casefold() in normalized
        ),
        None,
    )


def vacancy_rejection_reason(
    *,
    title: str,
    company: str,
    description: str,
    excluded_positions: tuple[str, ...],
    excluded_companies: tuple[str, ...],
    excluded_keywords: tuple[str, ...],
) -> str | None:
    title_match = title_rejection_reason(title, excluded_positions)
    if title_match:
        return f"position:{title_match}"
    normalized_company = company.casefold()
    company_match = next(
        (term for term in excluded_companies if term.casefold() in normalized_company),
        None,
    )
    if company_match:
        return f"company:{company_match}"
    normalized_description = description.casefold()
    keyword_match = next(
        (term for term in excluded_keywords if term.casefold() in normalized_description),
        None,
    )
    return f"keyword:{keyword_match}" if keyword_match else None
