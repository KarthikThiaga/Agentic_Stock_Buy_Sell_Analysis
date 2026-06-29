from core.validate_state import validate_state

def test_validate_state_1():

    required = [
        {'entity': 'AAPL', 'needs': ['price','news','financials']}, 
        {'entity': 'GOOG', 'needs': ['price','news','financials']}
    ]

    result_valid = {
        'AAPL': {
            'price': 150,
            'news': ['News 1', 'News 2'],
            'financials': {
                "assets":1000,
                "liabilities":200,
                "cash":300,
                "debt_ratio":0.2
            }
        },
        'GOOG': {
            'price': 2800,
            'news': ['News A', 'News B'],
            'financials': {
                "assets":5000,
                "liabilities":1000,
                "cash":2000,
                "debt_ratio":0.2
            }
        }
    }

    result_invalid = {
        'AAPL': {
            'price': -150,  # Invalid price
            'news': [],     # Invalid news
            'financials': {
                "assets":1000,
                "liabilities":200,
                "cash":300,
                "debt_ratio":0.2
            }
        },
        'GOOG': {
            'price': 2800,
            'news': ['News A', 'News B'],
            'financials': {
                "assets":5000,
                "liabilities":1000,
                "cash":2000,
                "debt_ratio":0.2
            }
        }
    }

    assert validate_state(required, result_valid) == []
    assert validate_state(required, result_invalid) == [
        {'ticker': 'AAPL', 'field': 'price', 'error': 'invalid'},
        {'ticker': 'AAPL', 'field': 'news', 'error': 'invalid'}
    ]

def test_validate_state_2():

    required = [
        {'entity': 'AAPL', 'needs': ['price','news','financials']}
    ]

    result_exception = {
        'AAPL': {
        'price': None,
        'news': None,
        "financials": None
        }
    }   

    assert validate_state(required, result_exception) == [
        {'ticker': 'AAPL', 'field': 'price', 'error': 'invalid'},
        {'ticker': 'AAPL', 'field': 'news', 'error': 'invalid'},
        {'ticker': 'AAPL', 'field': 'financials', 'error': 'invalid'}
    ]   


def test_validate_state_3():

    required = [
        {'entity': 'AAPL', 'needs': ['price','news','financials']}
    ]

    result_missing = {
        'AAPL': {
            'price': 150,
            # 'news' field is missing
            'financials': {
                "assets":1000,
                "liabilities":200,
                "cash":300,
                "debt_ratio":0.2
            }
        }
    }

    assert validate_state(required, result_missing) == [
        {'ticker': 'AAPL', 'field': 'news', 'error': 'invalid'}
    ]

def test_validate_state_4():
    required = [
        {'entity': 'AAPL', 'needs': ['price','news','financials']}
    ]

    result_empty = {
        'AAPL': {
            'price': 150,
            'news': [],  # Empty news list
            'financials': {
                "assets":1000,
                "liabilities":200,
                "cash":300,
                "debt_ratio":0.2
            }
        }
    }

    assert validate_state(required, result_empty) == [
        {'ticker': 'AAPL', 'field': 'news', 'error': 'invalid'}
    ]

def test_validate_state_5():
    required = [
        {'entity': 'AAPL', 'needs': ['price','news','financials']}
    ]

    result_incorrect_financials = {
        'AAPL': {
            'price': 150,
            'news': ['News 1', 'News 2'],
            'financials': {
                "assets":-5000,
                "liabilities":1000,
                "cash":2000,
                "debt_ratio":0.2
            }
        }
    }

    assert validate_state(required, result_incorrect_financials) == [
        {'ticker': 'AAPL', 'field': 'financials', 'error': 'invalid'}
    ]  

def test_validate_state_6():
    required = [
        {'entity': 'AAPL', 'needs': ['price','news','financials']}
    ]

    result_incorrect_financials_2 = {
        'AAPL': {
            'price': 150,
            'news': ['News 1', 'News 2'],
            'financials': {
                "assets":5000,
                "liabilities":-1000,
                "cash":2000,
                "debt_ratio":0.2
            }
        }
    }

    assert validate_state(required, result_incorrect_financials_2) == [
        {'ticker': 'AAPL', 'field': 'financials', 'error': 'invalid'}
    ]  


def test_validate_state_7():
    required = [
        {'entity': 'AAPL', 'needs': ['price','news','financials']}
    ]

    result_incorrect_financials_2 = {
        'AAPL': {
            'price': 150,
            'news': ['News 1', 'News 2'],
            'financials': {
                "assets":5000,
                "liabilities":1000,
                "cash":2000,
                "debt_ratio":5.2
            }
        }
    }

    assert validate_state(required, result_incorrect_financials_2) == [
        {'ticker': 'AAPL', 'field': 'financials', 'error': 'invalid'}
    ]  


def test_validate_state_10():
    required = [
        {'entity': 'AAPL', 'needs': ['price','news','financials']}
    ]

    result_incorrect_financials_3 = {
        'AAPL': {
            'price': 150,
            'news': ['News 1', 'News 2'],
            'financials': {
                "assets":5000,
                "liabilities":1000,
                "cash":-2000,
                "debt_ratio":0.2
            }
        }
    }

    assert validate_state(required, result_incorrect_financials_3) == [
        {'ticker': 'AAPL', 'field': 'financials', 'error': 'invalid'}
    ]  

def test_validate_state_8():
    required_empty = [
    ]

    result_incorrect_financials_4 = {
        'AAPL': {
            'price': 150,
            'news': ['News 1', 'News 2'],
            'financials': {
                "assets":5000,
                "liabilities":1000,
                "cash":2000,
                "debt_ratio":0.2
            }
        }
    }

    assert validate_state(required_empty, result_incorrect_financials_4) == []


def test_validate_state_9():
    required = [
        {'entity': 'AAPL', 'needs': ['price','news','financials']}
    ]

    result_incorrect_financials_4 = {
        'AAPL': {
            'price': 150,
            'news': ['News 1', 'News 2'],
        }
    }

    assert validate_state(required, result_incorrect_financials_4) == [
        {'ticker': 'AAPL', 'field': 'financials', 'error': 'invalid'}
    ]

def test_validate_state_11():
    required = [
        {'entity': 'AAPL', 'needs': ['price','news','financials']}
    ]

    result_incorrect_5 = {
        'AAPL': {
        }
    }

    assert validate_state(required, result_incorrect_5) == [
        {'ticker': 'AAPL', 'field': 'price', 'error': 'invalid'},
        {'ticker': 'AAPL', 'field': 'news', 'error': 'invalid'},
        {'ticker': 'AAPL', 'field': 'financials', 'error': 'invalid'}
    ]