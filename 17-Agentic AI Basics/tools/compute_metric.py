def compute_metric(financials,year):
    
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
