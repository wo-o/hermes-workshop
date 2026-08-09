def final_price(amount: float, discount_percent: float) -> float:
    """Return the price after applying a percentage discount."""
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")

    return amount * (discount_percent / 100)
