from tools.compute_confidence import compute_confidence

def get_raw_summary(result, intent):    
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
