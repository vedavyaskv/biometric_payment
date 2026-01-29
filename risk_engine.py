def calculate_risk(user_city, current_city, amount, failed_attempts):
    score = 0

    # Location
    if user_city.lower() == current_city.lower():
        score += 30
    else:
        score += 10

    # Amount
    if amount < 1000:
        score += 20
    elif amount <= 5000:
        score += 10
    else:
        score += 5

    # Failed attempts
    if failed_attempts == 0:
        score += 20
    else:
        score += 5

    return score
