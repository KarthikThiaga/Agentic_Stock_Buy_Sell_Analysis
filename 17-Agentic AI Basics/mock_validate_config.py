def validate_config(placholder):
    required = {
        'price_api_key': None,
        'news_api_key': 'abc',
        'finance_api_key': None,
        'fallback_api_key': '',
        'gemini_api_key': None,
        'price_api_url': 'abc',
        'news_api_url': None,
        'finance_api_url': None,
        'fallback_api_url': None
    }

    validation_errors = [key for (key,val) in required.items() if val == '' or not val]
    
    return validation_errors