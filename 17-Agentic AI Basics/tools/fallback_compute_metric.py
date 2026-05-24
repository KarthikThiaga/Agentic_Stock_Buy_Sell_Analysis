def fall_back_compute_metric(financials):
    
    assets = float(financials.get('assets', 0))
    liabilities = float(financials.get('liabilities', 0))
    cash = float(financials.get('cash', 0))

    try:
        debt_ratio = liabilities/assets
    except Exception as e:
        print(f"Error computing debt ratio: {e}")
        debt_ratio = 0
    
    return {
        "assets": assets,
        "liabilities": liabilities,
        "cash": cash,
        "debt_ratio": debt_ratio
    }

