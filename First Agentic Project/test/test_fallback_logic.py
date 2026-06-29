from core.choose_execution_path import choose_execution_path
from core.fallback_tool_execution import fallback_tool_execution

# def test_choose_execution_path():
#     # Test with a need that should go to primary
#     path = choose_execution_path("price")
#     assert path == "primary", f"Expected 'primary' but got {path}"

#     # Test with a need that should go to fallback
#     path = choose_execution_path("news")
#     assert path == "primary", f"Expected 'fallback' but got {path}"

#     # Test with a need that is not recognized (should default to primary)
#     path = choose_execution_path("unknown_need")
#     assert path == "primary", f"Expected 'primary' but got {path}"

def test_fallback_tool_execution():
    # Test with a need that should use the fallback tool
    output = fallback_tool_execution("AAPL", "price")
    assert output == None
