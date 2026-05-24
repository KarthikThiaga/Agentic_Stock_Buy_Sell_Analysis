def compute_confidence(financials):
    financial_confidence = 0

    if financials['assets']: financial_confidence += 1
    if financials['cash']: financial_confidence += 1
    if financials['debt_ratio']: financial_confidence += 1
    
    return financial_confidence
