from config.logger import logger

def validate_financials(financials):
    """Validates a dictionary containing financial metrics against predetermined structural rules.

    This function verifies whether the input `financials` is a dictionary, contains 
    all necessary keys ('assets', 'liabilities', 'cash', 'debt_ratio'), and ensures 
    that their corresponding values fall within logically valid numerical bounds. 
    Errors are logged for any failed criteria.

    Args:
        financials (Dict[str, float | int]): A dictionary representing the financial 
            statement data of a company. Expected key-value pairs include:
                - 'assets' (int | float): Total corporate assets (must be > 0).
                - 'liabilities' (int | float): Total corporate liabilities (must be >= 0).
                - 'cash' (int | float): Extracted cash reserves (must be >= 0).
                - 'debt_ratio' (int | float): Calculated leverage ratio (must be between 0 and 1 inclusive).

    Returns:
        bool: True if the financial data is a dictionary, contains all required keys, 
        and satisfies all empirical range constraints; otherwise, False.
    """
    if not isinstance(financials,dict):
        return False
    
    required_key_fields = ['assets','liabilities','cash','debt_ratio']

    for key in required_key_fields:
        if key not in financials:
            logger.error(f'event=validate_financials field={key} status=failure msg=not found')
            return False
    
    if financials['assets'] <= 0:
        logger.error(f'event=validate_financials field=assets status=failure')
        return False
    
    if financials['liabilities'] < 0:
        logger.error(f'event=validate_financials field=liabilities status=failure')
        return False
    
    if financials['cash'] < 0:
        logger.error(f'event=validate_financials field=cash status=failure')
        return False
    
    if financials['debt_ratio'] < 0 or financials['debt_ratio'] > 1:
        logger.error(f'event=validate_financials field=debt_ratiosss status=failure')
        return False
    
    return True
