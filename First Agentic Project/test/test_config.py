from mock_validate_config import validate_config


def test_validate_config():
    placeholder = ''
    validation_errors = validate_config(placeholder)
    assert validation_errors == ['price_api_key','finance_api_key','fallback_api_key','gemini_api_key','news_api_url','finance_api_url','fallback_api_url']

