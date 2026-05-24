from storage.write_memory import write_memory

def update_memory(memory,ticker,date,details):
    mem = dict(memory)
    ticker_dict = dict(mem.setdefault(ticker,{}))
    date_dict = dict(ticker_dict.setdefault(date,{}))

    date_dict.update(details)
    write_memory(memory)