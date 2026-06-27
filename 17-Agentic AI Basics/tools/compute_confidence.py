def compute_confidence(financials):
    """Computes a simplistic inventory completeness confidence score for financial datasets.

    Evaluates the presence of core foundational accounting elements within the provided 
    financial map payload. Each successfully populated validation metric increments the 
    overall tracking asset score by 1 point.

    Args:
        financials (Dict[str, Any]): A data container holding parsed target corporate financial 
            metrics, containing keys for 'assets', 'cash', and 'debt_ratio'.

    Returns:
        int: A calculated integer metric confidence tier value ranging from 0 (completely empty data) 
        to 3 (all core metrics present).
    """
    financial_confidence = 0

    if financials['assets']: financial_confidence += 1
    if financials['cash']: financial_confidence += 1
    if financials['debt_ratio']: financial_confidence += 1
    
    return financial_confidence
