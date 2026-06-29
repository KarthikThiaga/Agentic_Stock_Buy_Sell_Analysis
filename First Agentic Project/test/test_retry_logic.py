from core.retry_tool import retry_tool
from tools.price_tool import get_price
from tools.news_tool import get_news
from tools.financial_report import get_financial_reports
from mock_tool import mock_tool


capabilities = {
    "price": get_price,
    "news": get_news,
    "financials": get_financial_reports
}



def test_retry_tool():
    # Test with a tool that fails the first two times and succeeds the third time
    # output = retry_tool("AAPL", mock_tool, "price")
    # assert output == 150, f"Expected 150 but got {output}"
    # assert mock_tool.call_counter == 3
    
    # Test with a tool that always fails
    output = retry_tool("AAPL", mock_tool, "price")  
    assert output == None, f"Expected None but got {output}"
    assert mock_tool.call_counter == 3