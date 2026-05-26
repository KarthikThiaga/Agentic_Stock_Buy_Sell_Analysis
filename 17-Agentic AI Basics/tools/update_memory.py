from storage.write_memory import write_memory

def update_memory(memory,ticker,date,details):
    if not ticker in memory:
        memory[ticker] = {}
    
    if not date in memory[ticker]:
        memory[ticker][str(date)] = details
    else:
        memory[ticker][str(date)].update(details)
    
    write_memory(memory)