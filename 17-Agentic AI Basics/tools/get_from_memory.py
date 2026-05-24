def get_from_memory(memory,ticker,date,field):
    mem = memory.get(ticker,{}).get(date,{}).get(field,None)
    return mem
    
    