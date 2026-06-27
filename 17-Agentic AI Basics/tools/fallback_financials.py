from tools.api_call import api_call
from tools.fallback_resolve_metric import resolve_financial_term
from tools.fallback_compute_metric import fall_back_compute_metric
from config.logger import logger


def fall_back_finance(ticker,config):

    """Retrieves and processes financial balance sheet data via a secondary api channel.

    Acts as a failover routine when primary financial data paths are exhausted. The function 
    queries an external balance sheet endpoint, extracts the latest available annual statement based 
    on the most recent fiscal tracking date, translates the raw vendor keys into standardized accounting 
    terms, and computes relevant corporate financial health metrics.

    Args:
        ticker (str): The financial stock ticker symbol representing the target corporation.
        config (Dict[str, Any]): A configuration dictionary containing access keys and endpoint parameters:
            - "url" (str): The fallback endpoint routing URL.
            - "key" (str): The api authorization token.

    Returns:
        Dict[str, float | int]: A dictionary of normalized accounting values and computed 
        leverage metrics (e.g., debt ratio) extracted from the latest balance sheet. Returns 
        an empty dictionary if an API timeout or an error during structural data parsing occurs.
    """

    # print(f"Falling back to secondary method for finance data for {ticker}")
    logger.info(f'event=fall_back_finance msg=Falling back to secondary method for finance data for {ticker}')
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
            logger.info(f'event=fall_back_finance msg=No time series data found for {ticker} in fallback API')
            # print(f"No time series data found for {ticker} in fallback API.")
    except Exception as e:
        logger.exception(f'event=fall_back_finance operation=parsing status=failure exception={e}')
        # print(f"Error parsing fallback API response for {ticker}: {e}")
        return {}

    return financial_data