from config.logger import logger
def fall_back_compute_metric(financials):
    """Calculates flat-level corporate balance sheet components and leverage ratios.

    Serves as a secondary calculation pathway when a temporal index (year tracking) 
    is unavailable. It extracts total assets, total liabilities, and cash balances 
    directly from the root level of the provided financial structure, casting values 
    to floats. The corporate leverage metric (debt ratio) is evaluated by dividing 
    liabilities by total assets. If a division error occurs—such as when assets evaluate 
    to zero—the exception is safely isolated, recorded via the system logger, and a 
    default ratio value of zero is assigned.

    Args:
        financials (Dict[str, Any]): A un-nested flat data container holding asset, 
            liability, and cash parameters directly at its top-level namespace.

    Returns:
        Dict[str, float]: A dictionary containing normalized float values and the 
        calculated fallback leverage ratio:
            - "assets" (float): The total corporate assets found, defaulting to 0.0.
            - "liabilities" (float): The total corporate liabilities found, defaulting to 0.0.
            - "cash" (float): Total cash reserves found, defaulting to 0.0.
            - "debt_ratio" (float): The calculated leverage metric, or 0.0 if assets 
              are missing or evaluate to 0.
    """
    assets = float(financials.get('assets', 0))
    liabilities = float(financials.get('liabilities', 0))
    cash = float(financials.get('cash', 0))

    try:
        debt_ratio = liabilities/assets
    except Exception as e:
        logger.exception(f'event=fall_back_compute_metric operation=compute_debt_ratio status=failure exception={e}')
        # print(f"Error computing debt ratio: {e}")
        debt_ratio = 0
    
    return {
        "assets": assets,
        "liabilities": liabilities,
        "cash": cash,
        "debt_ratio": debt_ratio
    }

