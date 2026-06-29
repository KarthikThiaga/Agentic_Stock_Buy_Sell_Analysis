from models.entity_extraction import entity_extraction

def test_extract_apple():
    query = "moonjuice corporation"

    result = entity_extraction(query)

    assert result[0]['ticker'] == []