def parse_price(text: str) -> float | None:
    if not text:
        return None

    cleaned = (
        text.replace("₸", "")
        .replace("$", "")
        .replace("руб.", "")
        .replace(",", ".")
        .replace("\u202f", "")
        .replace("\u00A0", "")
        .strip()
    )

    parts = cleaned.split()

    prices = []
    for part in parts:
        try:
            price = float(part)
            prices.append(price)
        except ValueError:
            continue

    if not prices:
        return None

    result = min(prices)

    if result == 0.0 and len(set(prices)) > 1:
        return max(prices)

    return result
