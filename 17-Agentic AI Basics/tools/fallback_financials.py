from tools.api_call import api_call
from tools.fallback_resolve_metric import resolve_financial_term
from tools.fallback_compute_metric import fall_back_compute_metric
FALL_API_KEY = 'D5UBRFGP3EKH7ROG'


def fall_back_finance(ticker,config):
    print(f"Falling back to secondary method for finance data for {ticker}")
    api_url = config.get("url")
    api_key = config.get("key")

    function = 'BALANCE_SHEET'
    params = {
        'function': function,
        'symbol': ticker,
        'apikey': api_key
    }
    response = api_call(ticker, api_url, params=params, field='fallback_finance')
    try:
        annual_reports = {}
        data = response
        balance_sheet = data.get('annualReports', [])
        if len(balance_sheet) > 0:
            financials = max(balance_sheet, key=lambda x: x['fiscalDateEnding'])
            curr_year = financials['fiscalDateEnding'][:4]
            for key in financials:
                resolved_term = resolve_financial_term(key)
                if resolved_term:
                    annual_reports[resolved_term] = financials.get(key)

            financial_data = fall_back_compute_metric(annual_reports)
        else:
            print(f"No time series data found for {ticker} in fallback API.")
    except Exception as e:
        print(f"Error parsing fallback API response for {ticker}: {e}")
        return {}

    return financial_data