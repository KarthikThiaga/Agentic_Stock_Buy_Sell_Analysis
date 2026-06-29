from config.settings import Settings

settings = Settings()

def validate_config(settings):
    """
        pass API related details in dict format
        list of keys which has incorrect values will be displayed
    """
    required = {
        'price_api_key': settings.PRICE_API_KEY,
        'news_api_key': settings.NEWS_API_KEY,
        'finance_api_key': settings.FINANCE_API_KEY,
        'fallback_api_key': settings.FALLBACK_API_KEY,
        'gemini_api_key': settings.GEMINI_API_KEY,
        'price_api_url':settings.PRICE_API_URL,
        'news_api_url':settings.NEWS_API_URL,
        'finance_api_url':settings.FINANCIAL_REPORT_URL,
        'fallback_api_url':settings.FALLBACK_API_URL
    }

    validation_errors = [key for (key,val) in required.items() if not val or str(val).strip() == '']
    
    return validation_errors
    