from models.entity_extraction import entity_extraction
from models.extract_intent_entity import extract_intent_entity

def test_duplicate_entries():
    query = "compare apple and apple"
    output = entity_extraction(query)
    assert output == [{'ticker': 'AAPL', 'price': None, 'news': None, 'financials': None}]

    query = "compare apple google and apple"
    output = entity_extraction(query)
    assert output == [{'ticker': 'AAPL', 'price': None, 'news': None, 'financials': None},
                      {'ticker': 'GOOG', 'price': None, 'news': None, 'financials': None}]

def test_duplicate_entries2():
    # query = "compare iphone and apple"
    # output1, output2,error = extract_intent_entity(query)
    # assert output1 == 'none'
    # assert output2 == 'none'
    # assert error == {'duplicate': True}

    # query = "compare google and google"
    # output1, output2,error = extract_intent_entity(query)
    # assert output1 == 'none'
    # assert output2 == 'none'
    # assert error == {'duplicate': True}

    query = "compare google amazon and google"
    output1, output2,error = extract_intent_entity(query)
    
    assert output1  == [{'ticker': 'GOOG', 'price': None, 'news': None, 'financials': None},
                                {'ticker': 'AMZN', 'price': None, 'news': None, 'financials': None}]
    assert output2  == {'compare': True,'basis': []}
    assert error == {}