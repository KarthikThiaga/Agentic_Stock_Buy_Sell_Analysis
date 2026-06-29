from models.intent_extraction import get_intent, parsing_intent
def test_price_intent():
    query = "Apl Price"

    result = get_intent(query)

    assert result == {
        'compare': False,
        'basis': ['price'],
    }
    
def test_news_intent():
    query = "latest news on nvidia"

    result = parsing_intent(query)

    assert result == ['news']

def test_analysis_intent():
    result = parsing_intent("goodbye apple")
    assert result == []


def test_multiple_intents():
    result = parsing_intent("apple price and news")
    assert "price" in result
    assert "news" in result


def test_empty_query():
    result = parsing_intent("unwanted stuff")
    assert result == []

def test_compare_query():
    result = get_intent("compare apple and nvidia")
    assert result == {
        'compare': True,
        'basis': [],
    }

def test_empty_query2():
    result = get_intent("unwanted stuff")
    assert result == {
        'compare': False,
        'basis': [],
    }

def test_analysis_query2():
    result = get_intent("Is Apple a good buy?")
    assert result == {
        'compare': False,
        'basis': ["analysis"],
    }

def test_analysis_query3():
    result = get_intent("Is Apple a good buy and latest news?")
    assert result == {
        'compare': False,
        'basis': ["analysis", "news"],
    }
