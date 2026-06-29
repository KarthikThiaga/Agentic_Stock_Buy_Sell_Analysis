from core.output_validation import output_validation

def test_output_validation():
    assert output_validation(150.0, 'price') == True
    assert output_validation(-10.0, 'price') == False
    assert output_validation("not a number", 'price') == False

    assert output_validation(["news1", "news2"], 'news') == True
    assert output_validation([], 'news') == False
    assert output_validation("not a list", 'news') == False

    valid_financials = {
    "assets":1000,
    "liabilities":200,
    "cash":300,
    "debt_ratio":0.2
    }
    invalid_financials_1 = {
    "assets":-1000,
    "liabilities":200,
    "cash":300,
    "debt_ratio":0.2
    }

    invalid_financials_2 = {
    "assets":0,
    "liabilities":200,
    "cash":300,
    "debt_ratio":0.2
    }

    invalid_financials_3 = {
    "assets":1000,
    "liabilities":-20,
    "cash":300,
    "debt_ratio":0.2
    }

    invalid_financials_4 = {
    "assets":1000,
    "liabilities":0,
    "cash":300,
    "debt_ratio":0.2
    }

    invalid_financials_4_1 = {
    "assets":1000,
    "liabilities":200,
    "cash":-300,
    "debt_ratio":0.2
    }

    invalid_financials_5 = {
    "assets":1000,
    "liabilities":200,
    "cash":0,
    "debt_ratio":0.2
    }
    
    invalid_financials_6 = {
    "assets":1000,
    "liabilities":200,
    "cash":300,
    "debt_ratio":-0.2
    }

    invalid_financials_7 = {
    "assets":1000,
    "liabilities":200,
    "cash":300,
    "debt_ratio": 0
    }

    invalid_financials_8 = {
    "assets":1000,
    "liabilities":200,
    "cash":300,
    "debt_ratio": 1.1
    }

    invalid_financials_9 = {
    "assets":1000,
    "debt_ratio": 0.2
    }
    
    assert output_validation(valid_financials, 'financials') == True
    assert output_validation(invalid_financials_1, 'financials') == False
    assert output_validation(invalid_financials_2, 'financials') == False
    assert output_validation(invalid_financials_3, 'financials') == False
    assert output_validation(invalid_financials_4_1, 'financials') == False
    assert output_validation(invalid_financials_5, 'financials') == True   
    assert output_validation(invalid_financials_6, 'financials') == False
    assert output_validation(invalid_financials_7, 'financials') == True
    assert output_validation(invalid_financials_8, 'financials') == False
    assert output_validation(invalid_financials_9, 'financials') == False
    assert output_validation("not a dict", 'financials') == False
    assert output_validation({"assets":1000}, 'financials') == False
    assert output_validation([], 'financials') == False
    assert output_validation(None, 'financials') == False