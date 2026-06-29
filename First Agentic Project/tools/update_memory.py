from storage.write_memory import write_memory

def update_memory(memory,ticker,date,details):
    """Appends or updates structural tracking metrics inside the persistent session cache.

    Safely ensures that a hierarchical dictionary path exists for the designated corporate 
    ticker symbol and localized execution date. If the specific date key is unpopulated, it 
    initializes the record payload directly; if it already contains existing data fields, 
    the collection is updated in-place with the new attributes. Finally, the mutated memory 
    map is serialized and saved back to disk storage.

    Args:
        memory (Dict[str, Dict[str, Dict[str, Any]]]): The multi-layered runtime cache or 
            session state mapping structure.
        ticker (str): The unique financial asset abbreviation identifier (e.g., 'AAPL').
        date (str | datetime.date): The calendar day or reporting interval key associated with 
            the mutation tracking checkpoint.
        details (Dict[str, Any]): A payload subset mapping logical attributes (e.g., 'price', 
            'news', or 'financials') to updated evaluation metrics.
    """
    if not ticker in memory:
        memory[ticker] = {}
    
    if not str(date) in memory[ticker]:
        memory[ticker][str(date)] = details
    else:
        memory[ticker][str(date)].update(details)
    
    write_memory(memory)