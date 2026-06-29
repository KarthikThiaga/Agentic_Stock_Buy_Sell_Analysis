from tools.price_tool import get_price
from tools.news_tool import get_news
from tools.financial_report import get_financial_reports
from tools.fallback_price import fall_back_price
from tools.fallback_news import fall_back_news
from tools.fallback_financials import fall_back_finance
from config.settings import Settings    
settings = Settings()


API_CONFIG = {
    "price": {
        "url": settings.PRICE_API_URL,
        "key": settings.PRICE_API_KEY
    },
    "news": {
        "url": settings.NEWS_API_URL,
        "key": settings.NEWS_API_KEY
    },
    "financials": {
        "url": settings.FINANCIAL_REPORT_URL,
        "key": settings.FINANCE_API_KEY
    },
    "fallback": {
        "url": settings.FALLBACK_API_URL,
        "key": settings.FALLBACK_API_KEY
    }
}

def test_api_success():
        
    config=(API_CONFIG.get("price",{}))
    output = get_price("AAPL", config)
    assert output > 0

    config=(API_CONFIG.get("news",{}))
    output = get_news("AAPL", config)
    assert output != [] and isinstance(output,list)

    config=(API_CONFIG.get("financials",{}))
    output = get_financial_reports("AAPL", config)
    assert output != {} and isinstance(output,dict)

    config=(API_CONFIG.get("fallback",{}))
    output = fall_back_price("AAPL", config)
    assert output > 0

    output = fall_back_news("AAPL", config)
    assert output != [] and isinstance(output,list)

    output = fall_back_finance("AAPL", config)
    assert output != {} and isinstance(output,dict)



# def test_api_response():
#     ## Test case 1: connection error
#     ## Test case 2: return None
#     ## Test case 3: return []
#     ## Test case 4: Internal server error
#     config=(API_CONFIG.get("price",{}))
#     output = get_price("AAPL", config)
#     assert output == 0

#     config=(API_CONFIG.get("news",{}))
#     output = get_news("AAPL", config)
#     assert output == []

#     config=(API_CONFIG.get("financials",{}))
#     output = get_financial_reports("AAPL", config)
#     assert output == {}

#     config=(API_CONFIG.get("fallback",{}))
#     output = fall_back_price("AAPL", config)
#     assert output == 0

#     output = fall_back_news("AAPL", config)
#     assert output == []

#     output = fall_back_finance("AAPL", config)
#     assert output == {}
    



    
    
