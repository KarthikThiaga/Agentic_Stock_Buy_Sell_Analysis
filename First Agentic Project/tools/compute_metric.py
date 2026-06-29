def compute_metric(financials,year):
    """Extracts balance sheet components and computes the corporate debt ratio for a specific year.

    Extracts total assets, total liabilities, and cash reserves from a nested historical 
    financial dictionary for the specified calendar year. It then calculates the leverage 
    metric (debt ratio) by evaluating liabilities against available assets. If a division 
    by zero occurs due to a lack of recorded asset parameters, the calculation fails safely 
    and sets the debt ratio score to zero.

    Args:
        financials (Dict[str | int, Dict[str, int | float]]): A nested dictionary structured 
            by year keys, mapping to inner dictionaries containing balance sheet parameters 
            (e.g., 'assets', 'liabilities', 'cash').
        year (str | int): The specific fiscal or calendar year identifier to look up.

    Returns:
        Dict[str, int | float]: A dictionary containing the extracted core values and the 
        calculated leverage metric:
            - "assets" (int | float): The asset value found, defaulting to 0.
            - "liabilities" (int | float): The liability value found, defaulting to 0.
            - "cash" (int | float): The cash value found, defaulting to 0.
            - "debt_ratio" (float | int): The calculated total liabilities divided by total 
              assets, or 0 if assets evaluate to 0.
    """
    assets = financials[year].get('assets', 0)
    liabilities = financials[year].get('liabilities', 0)
    cash = financials[year].get('cash', 0)

    try:
        debt_ratio = liabilities/assets
    except:
        debt_ratio = 0
    
    return {
        "assets": assets,
        "liabilities": liabilities,
        "cash": cash,
        "debt_ratio": debt_ratio
    }
