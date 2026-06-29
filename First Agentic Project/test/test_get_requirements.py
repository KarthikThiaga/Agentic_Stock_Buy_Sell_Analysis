from models.get_requirements import get_requirements

def test_get_requirements():
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
    assert get_requirements(intent_compare, entity_compare) == ([{'entity': 'AAPL', 'needs': ['price','news','financials']}, 
                                                                 {'entity': 'GOOG', 'needs': ['price','news','financials']}], 
                                                                 {'compare': True, 'basis': ['price','news','financials']})
    
    intent_analysis = {'compare': False, 'basis': ['analysis']}
    entity_analysis = [
    {
        'ticker': 'AAPL',
        'price': None,
        'news': None,
        "financials": None
    }
    ]
    assert get_requirements(intent_analysis, entity_analysis) == ([{'entity': 'AAPL', 'needs': ['price','news','financials']}], {'compare': False, 'basis': ['price','news','financials']})

    intent_analysis_2 = {'compare': False, 'basis': ['analysis']}
    entity_analysis_2   = [
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

    assert get_requirements(intent_analysis_2, entity_analysis_2) == ([{'entity': 'AAPL', 'needs': ['financials']}, 
                                                                   {'entity': 'GOOG', 'needs': ['financials']}], {'compare': False, 'basis': ['financials']})   

    intent_none = {'compare': False, 'basis': []}
    entity_none = []
    assert get_requirements(intent_none, entity_none) == ("none","none")

    intent_price = {'compare': False, 'basis': ['price']}
    entity_price = [
     {
        'ticker': 'AAPL',
        'price': None,
        'news': None,
        "financials": None
    }
    ]       
    assert get_requirements(intent_price, entity_price) == ([{'entity': 'AAPL', 'needs': ['price']}], {'compare': False, 'basis': ['price']})

    intent_price_news = {'compare': False, 'basis': ['price','news']}
    entity_price_news = [
     {
        'ticker': 'AAPL',
        'price': None,
        'news': None,
        "financials": None
    }
    ]
    assert get_requirements(intent_price_news, entity_price_news) == ([{'entity': 'AAPL', 'needs': ['price','news']}], {'compare': False, 'basis': ['price','news']})

    intent_compare_no_basis = {'compare': True, 'basis': []}
    entity_compare_no_basis = [
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
    
    assert get_requirements(intent_compare_no_basis, entity_compare_no_basis) == ([{'entity': 'AAPL', 'needs': []}, 
                                                                                 {'entity': 'GOOG', 'needs': []}],  
                                                                                 {'compare': True, 'basis': []}) 
    
    intent_analysis_no_entity = {'compare': False, 'basis': ['analysis']}
    entity_analysis_no_entity = []  

    assert get_requirements(intent_analysis_no_entity, entity_analysis_no_entity) == ("none","none")    

    intent_price_no_entity = {'compare': False, 'basis': ['price']}
    entity_price_no_entity = [] 
    assert get_requirements(intent_price_no_entity, entity_price_no_entity) == ("none","none")  

    intnt_news_no_entity = {'compare': False, 'basis': ['news']}
    entity_news_no_entity = []
    assert get_requirements(intnt_news_no_entity, entity_news_no_entity) == ("none","none")

    intent_price_news_no_entity = {'compare': False, 'basis': ['price','news']}
    entity_price_news_no_entity = []
    assert get_requirements(intent_price_news_no_entity, entity_price_news_no_entity) == ("none","none")

    intent_compare_no_basis_no_entity = {'compare': True, 'basis': []}
    entity_compare_no_basis_no_entity = []  
    assert get_requirements(intent_compare_no_basis_no_entity, entity_compare_no_basis_no_entity) == ("none","none")    

    intnt_none_no_entity = {'compare': False, 'basis': []}
    entity_none_no_entity = []  
    assert get_requirements(intnt_none_no_entity, entity_none_no_entity) == ("none","none")

    intent_news_only = {'compare': False, 'basis': ['news']}
    entity_news_only = [
    {
        'ticker': 'AAPL',
        'price': None,
        'news': None,
        "financials": None
    }
    ]

    assert get_requirements(intent_news_only, entity_news_only) == ([{'entity': 'AAPL', 'needs': ['news']}], {'compare': False, 'basis': ['news']})

    intent_analysis_price = {'compare': False, 'basis': ['analysis','price']}
    entity_analysis_price = [
    {
        'ticker': 'AAPL',
        'price': None,
        'news': None,
        "financials": None
    }
    ]

    assert get_requirements(intent_analysis_price, entity_analysis_price) == ([{'entity': 'AAPL', 'needs': ['price','news','financials']}], 
                                                                              {'compare': False, 'basis': ['price','news','financials']})
    
    intent_analysis_price_no_entity = {'compare': False, 'basis': ['analysis','price']}
    entity_analysis_price_no_entity = []    
    assert get_requirements(intent_analysis_price_no_entity, entity_analysis_price_no_entity) == ("none","none")

    intent_analysis_news = {'compare': False, 'basis': ['analysis','news']}
    entity_analysis_news = [
    {
        'ticker': 'AAPL',
        'price': None,
        'news': None,
        "financials": None
    }
    ]
    assert get_requirements(intent_analysis_news, entity_analysis_news) == ([{'entity': 'AAPL', 'needs': ['news','financials']}], 
                                                                            {'compare': False, 'basis': ['news','financials']})   
    
