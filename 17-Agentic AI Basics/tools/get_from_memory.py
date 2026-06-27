def get_from_memory(memory,ticker,date,field):
    """Retrieves cached data fields from the session memory map based on a ticker and date key.

    Performs a safe, nested dictionary look-up to find previously stored or cached results 
    matching a specific company ticker symbol, execution/reporting date, and logical data 
    category field. If any key level in the hierarchy is missing, it falls back gracefully 
    without raising a KeyError.

    Args:
        memory (Dict[str, Dict[str | datetime.date, Dict[str, Any]]]): The multi-layered session 
            state or metrics cache dictionary.
        ticker (str): The unique financial asset abbreviation identifier (e.g., 'AAPL').
        date (str | datetime.date): The specific calendar day or reporting interval key 
            associated with the cached data block.
        field (str): The requested data category type or attribute identifier (e.g., 'financials', 
            'price', or 'news').

    Returns:
        Any | None: The cached data fragment or structure matching the requested lookup criteria 
        if found; otherwise, returns None.
    """
    mem = memory.get(ticker,{}).get(date,{}).get(field,None)
    return mem
    
    