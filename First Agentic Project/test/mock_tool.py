def mock_tool(ticker, config):

    
    mock_tool.call_counter += 1
    print(f"Mock tool called with ticker: {ticker} and calls count: {mock_tool.call_counter}")

    if mock_tool.call_counter < 4:
        return None

    return 150  

mock_tool.call_counter = 0 
    