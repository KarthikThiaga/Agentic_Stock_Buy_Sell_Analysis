from tools.compute_confidence import compute_confidence

def get_raw_summary(result, intent):    
    """Compiles structured text summary segments for each ticker based on user intent.

    This function processes the dynamic tool execution results for a set of tickers 
    and filters/formats the extracted data to match the evaluation constraints 
    specified in the user intent ('basis'). Depending on whether the intent requires 
    a full breakdown (price, news, and financials) or individual data points, it 
    constructs an appropriate string summary and computes a financial confidence score 
    when deep metrics are requested.

    Args:
        result (Dict[str, Dict[str, Any]]): A nested dictionary containing fetched 
            tool metrics grouped by stock ticker. Example structure:
                {
                    'AAPL': {
                        'price': '150.00',
                        'news': ['headline 1', 'headline 2'],
                        'financials': {'cash': '100B', 'debt_ratio': '0.5', 'assets': '350B'}
                    }
                }
        intent (Dict[str, Any]): A dictionary representing user configurations, 
            containing at least a 'basis' key holding a list or string of target topics 
            (e.g., {'basis': ['price', 'news', 'financials']}).

    Returns:
        List[str]: A list of string summary blocks compiled for each processed ticker.
    """
    temp_word = ''
    generated_output = []
    for ticker,info in result.items():

        if ('price' in intent['basis'] and 'news' in intent['basis'] and 'financials' in intent['basis']) or 'analysis' in intent['basis']:
            financial_confidence = compute_confidence(info['financials'])
            temp_word = f"""
            {ticker}:
            - price: {info['price']} 
            - cash: {info['financials']['cash']}
            - Debt ratio: {info['financials']['debt_ratio']}
            - Assets: {info['financials']['assets']}
            - news: {info['news']} 

            - financial confidence = {financial_confidence}
            """
        elif 'price' in intent['basis']:
            temp_word = f"price of {ticker} is {info['price']}"
        elif 'news' in intent['basis']:
            temp_word = f"news of ticker {ticker} is \n" +  "\n".join(info['news'])  

        generated_output.append(temp_word)

    
    return generated_output
