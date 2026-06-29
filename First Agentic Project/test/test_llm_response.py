from models.llm_entity_extract import llm_entity_extraction

def test_llm_extract():
    # Test case 5: partially valid
    query = "compare apple and amazon"
    intent = "compare"

    output = llm_entity_extraction(query, intent)
    assert output == None
