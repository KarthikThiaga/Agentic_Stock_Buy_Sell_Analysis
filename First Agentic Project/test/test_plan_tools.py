from core.plan_tools import plan_tools

def test_plan_tools():
    intent_compare = {'compare': True, 'basis': ['price']}
    entity_compare = [
    {
        'ticker': 'AAPL',
        'price': None,
        'news': None,
        "financials": None
    },
    {
        'ticker': 'GOOG',
        'price': None,
        'news': None,
        "financials": None
    }
    ]

    intent_compare_2 = {'compare': True, 'basis': []}
    intent_compare_3 = {'compare': True, 'basis': ['analysis']}
    intent_compare_4 = {'compare': False, 'basis': []}
    assert plan_tools(intent_compare, entity_compare) == ['price','news','financials']
    assert plan_tools(intent_compare_2, entity_compare) == ['price','news','financials']
    assert plan_tools(intent_compare_3, entity_compare) == ['price','news','financials']
    assert plan_tools(intent_compare_4, entity_compare) == []


    intent_analysis = {'compare': False, 'basis': ['analysis']}
    entity_analysis_1 = [
    {
        'ticker': 'AAPL',
        'price': None,
        'news': None,
        "financials": None
    }
    ]
    entity_analysis_2 = [
    {
        'ticker': 'AAPL',
        'price': None,
        'news': None,
        "financials": None
    },
    {
        'ticker': 'GOOG',
        'price': None,
        'news': None,
        "financials": None
    }
    ]

    intent_analysis_2 = {'compare': False, 'basis': ['analysis','price']}
    assert plan_tools(intent_analysis, entity_analysis_1) == ['financials', 'news', 'price']
    assert plan_tools(intent_analysis, entity_analysis_2) == ['financials']
    assert plan_tools(intent_analysis_2, entity_analysis_1) == ['financials', 'news', 'price']
    assert plan_tools(intent_analysis_2, entity_analysis_2) == ['financials']

    intent_price = {'compare': False, 'basis': ['price']}
    entity_price = [
     {
        'ticker': 'AAPL',
        'price': None,
        'news': None,
        "financials": None
    }
    ]
    assert plan_tools(intent_price, entity_price) == ['price']

    intent_news = {'compare': False, 'basis': ['news']}
    entity_news = [
    {
        'ticker': 'AAPL',
        'price': None,
        'news': None,
        "financials": None
    }
    ]
    assert plan_tools(intent_news, entity_news) == ['news']

    intent_price_news = {'compare': False, 'basis': ['price','news']}
    assert plan_tools(intent_price_news, entity_price) == ['price','news']

    intent_none = {
    "compare": False,
    "basis": ["something_random"]
    }
    assert plan_tools(intent_none, entity_price) == []
