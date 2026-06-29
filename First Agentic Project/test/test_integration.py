from model import orchestator

def test_price():
    query = "apple price"
    
    output = orchestator(query)

    output['output'] is not None 
     
def test_news():
    query = 'apple news'

    output = orchestator(query)
    output['output'] is not None

def test_invalid():
    query = 'Hello word'
    output = orchestator(query)
    output == "none"



     
