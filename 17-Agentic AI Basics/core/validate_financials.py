def validate_financials(financials):
    if not isinstance(financials,dict):
        return False
    
    required_key_fields = ['assets','liabilities','cash','debt_ratio']

    for key in required_key_fields:
        if key not in financials:
            return False
    
    if financials['assets'] <= 0:
        return False
    
    if financials['liabilities'] < 0:
        return False
    
    if financials['cash'] < 0:
        return False
    
    if financials['debt_ratio'] < 0:
        return False
    
    return True
