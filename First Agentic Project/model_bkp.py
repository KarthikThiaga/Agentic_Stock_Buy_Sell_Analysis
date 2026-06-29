from rapidfuzz import process 
from google import genai
from datetime import datetime
import requests
import json 
import re
import time 
from app import ui

StreamlitUI = ui.StreamlitUIDisplay()
memory = {}

FALLBACK_API_URL = 'https://www.alphavantage.co/query'
FALL_API_KEY = 'D5UBRFGP3EKH7ROG'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0'
    }


FALL_BACK_EXACT_MATCH = {
    "assets": ["totalAssets"],
    "liabilities": ["totalLiabilities"],
    "cash": ["cashAndCashEquivalentsAtCarryingValue"]
}

user_query_mem = {}

STOP_WORDS = ['compare', 'or', 'and', 'of', 'are', 'vs' ,'what']

PRICE_API_URL = "https://finnhub.io/api/v1/quote"
NEWS_API_URL = "https://newsapi.org/v2/everything"
FINANCIAL_REPORT_URL = "https://finnhub.io/api/v1/stock/financials-reported"
FINANCIAL_METRICS_NEEDED = {'Total assets', 'Total liabilities', 'Cash and cash equivalents', 'Accounts payable', 'Inventories','Total current liabilities'}


BLACKLIST = ["other", "misc", "non-current"]


EXACT_MATCH = {
    "assets": ["total assets"],
    "liabilities": ["total liabilities"],
    "cash": ["cash and cash equivalents"]
}

FUZZY_MATCH = {
    "assets": [
        "assets, current",
        "assets total"
    ],
    "liabilities": [
        "liabilities, current",
        "total liabilities",
        "liabilities"
    ],
    "cash": [
        "cash equivalents",
    ]
}

def emit_event(message):
    if message['type'] == 'info':
        StreamlitUI.ui_info(message.get('text',''))
    
    if message['type'] == 'error':
        StreamlitUI.ui_error(message.get('text',''))
    
    if message['type'] == 'success':
        StreamlitUI.ui_success(message.get('text',''))
    
    if message['type'] == 'warning':
        StreamlitUI.ui_warning(message.get('text',''))

    if message['type'] == 'exception':
        StreamlitUI.ui_exception(message.get('text',''))

    if message['type'] == 'spinner':
        StreamlitUI.ui_spinner(message.get('text',''))   
    
    if message['type'] == 'progress':
        StreamlitUI.ui_progress_bar(0)  

    if message['type'] == 'output':
        StreamlitUI.ui_success(message.get('text',''))


PRICE_KEYWORDS = ['price', 'trading', 'value', 'quote']
NEWS_KEYWORDS = ['news','update', 'happening', 'recent']
BUY_KEYWORDS = ['buy', 'invest','good', 'worth','analyse']
COMPARISON_KEYWORDS = ['compare', 'comparison', 'difference', 'good', 'best', 'better']

def parsing_intent(query):
    intents = []
    if any (word in query for word in PRICE_KEYWORDS):
        intents.append('price')
    if any (word in query for word in NEWS_KEYWORDS):
        intents.append('news')
    if any(word in query for word in BUY_KEYWORDS):
        intents.append('analysis')
    
    return intents

def get_intent(query):
    emit_event({'type': 'info', 'text': 'Parsing intent from query'})
    q = query.lower()

    intent = {
        'compare': any(word in q for word in COMPARISON_KEYWORDS),
        'basis': parsing_intent(q),
    }

    return intent

entity = []

ALIAS_MAP = {}

try:
    with open('alias_map.json','r') as file:

        try:
            ALIAS_MAP = json.load(file)
        except Exception as ex_json:
            print(f'ERROR: Error while loading ALIAS_MAP check {file} for exception {ex_json}')
except FileNotFoundError:
    print(f'ERROR: alias_map.json file not found - creation a new one')
    with open('alias_map.json','w') as file:
        file.write(ALIAS_MAP)

except Exception as ex_file_error:
    print(f'ERROR: error while opening alias_map.json file - {ex_file_error}')

COMPANY_DB = {
    'apple': 'AAPL',
    'nvidia': 'NVDA',
    'jpmorgan': 'JPM',
    'google': 'GOOG',
    'microsoft': 'MSFT',
    'amazon': 'AMZN'
}

def fuzzy_match(word, choices):
    match, score, _ = process.extractOne(word,choices)
    print (f"LOG: Token {word}, match: {match}, score: {score}")
    if score >= 80:
        logic = 'fuzzy'
        return match, logic, score
    
    return None

def user_token_log(entity,score,match,logic):
    user_query_log = read_user_query_file()

    word = normalize(entity)

    if word in user_query_log.keys():
        items = user_query_log[word]
        items["count"] += 1
        items["confidence"] = int(
            (items["confidence"] * (items["count"] - 1) + score)/items["count"]
        )
    else:
        user_query_log[word] = {
            "resolved": match,
            "confidence": score,
            "source": logic,
            "count": 1
        }
        
    write_user_query_file(user_query_log)

def read_user_query_file():
    try: 
        with open('user_query.json','r') as file:
            try: 
                data = json.load(file)
                return data
            except Exception as ex_json_read_error:
                print(f'ERROR: JSON read failed for user map - {ex_json_read_error}')
    except FileNotFoundError:
        with open('user_query.json', 'w') as file:
            file.write({})
            return {}
    except Exception as ex_user_file:
        print(f'ERROR: user_query.json file open failed - {ex_user_file}')
        return {}

def write_user_query_file(data):
    try:
        with open('user_query.json','w') as file:
            json.dump(data, file, indent=4)
    except Exception as ex_write_user_json:
        print(f'ERROR: while writing user_query.json file - {ex_write_user_json}')


def entity_extraction(query):
    emit_event({'type': 'info', 'text': 'Extracting entities from query'})
    seen = set()
    words = re.findall(r'\b\w+\b', query.lower())
    tokens = [word for word in words if word not in STOP_WORDS]
    entities = []


    for token in tokens:

        if len(token) > 3:
            try:
                company_name,logic,score = fuzzy_match(token,COMPANY_DB.keys())
            except Exception as ex_fuzzy:
                print(f'ERROR: Fuzzy matching failed for token {token} - {ex_fuzzy}')
                company_name = None

            if not company_name:
                try:
                    company_name,logic,score = fuzzy_match(token,ALIAS_MAP.keys())
                except Exception as ex_fuzzy_alias:
                    print(f'ERROR: Fuzzy matching failed for token {token} in alias map - {ex_fuzzy_alias}')
                    company_name = None

            if  company_name:
                if company_name in ALIAS_MAP:
                    ticker = ALIAS_MAP[company_name]
                elif company_name in COMPANY_DB:
                    ticker = COMPANY_DB[company_name]

                user_token_log(token,score,ticker,logic)

                if ticker not in seen:

                    entity = {
                        'ticker': ticker,
                        'price': None,
                        'news': None,
                        'financials': None
                    }
                    seen.add(ticker)
                    entities.append(entity)
            

    return entities

def normalize(text):
    return text.lower().strip()

def llmcall(prompt):
    client = genai.Client(api_key='AIzaSyBXxSjUUjhw9n8F1NFQXIfFf51sv6RA_EU')
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents={"text": prompt}
    )

    return (response.text)

def required_llm_call(entity, intent):
    if len(entity) == 0:
        return True
    elif intent['compare'] and len(entity) < 2:
        return True
    elif 'analysis' in intent['basis'] and len(entity) < 1:
        return True
    else:
        return False


def llm_entity_extraction(query,intent):
    
    print("LOG: Fuzzy extraction insufficient --> Triggering LLM")
    prompt = f'''
        Extract stock entities from the query.

        Query: {query}

        Return STRICT JSON:

        {{
        "entities": [
            {{
            "input": "appl",
            "resolved": "AAPL", 
            "confidence": 0.7
            }}
        ]
        }}

        Rules:
        - "input" = exact word/phrase from query
        - confidence = your certainty (0 to 1)
        - If none:
        {{"entities": []}}
        - this entities should contain only stock related word
        - Stops words shall be ignored in entities

        NO extra text.
    '''
    
    try:
        resp = re.sub(r"```json|```", "", llmcall(prompt))
        print(resp)
        data = json.loads(resp)["entities"]

        list_of_entities = []
        try:
            for items in data:
                user_token_log(entity = items["input"],
                            match = items["resolved"],
                            score = int(items["confidence"] * 100),
                            logic = 'llm')
                list_of_entities.append(items["resolved"])
        except KeyError:
            print(f'ERROR: Clean prompt the response is {resp}')
        except Exception as ex_entity_error:
            print(f'ERROR: in llm_call to log user query = {ex_entity_error}')

        response = {
            "tickers": list_of_entities
        }
        
        return response

    except Exception as ex1:
        print(f'LLM response JSON load failed  - Exception is {ex1}')
        return None


def extract_intent_entity(query):
    intent = get_intent(query)
    entity = entity_extraction(query)

    call_llm = required_llm_call(entity,intent)

    if call_llm:

        company_names = llm_entity_extraction(query,intent)

        if not company_names:
            emit_event({'type': 'info', 'text': "No entities found in query."})
            return "none","none"

        new_entries = []

        for ticker in company_names:
            exists = False 
            for items in entity:
                if ticker == items['ticker']:
                    exists = True
            
            if not exists:
                new_entity = {
                    'ticker': ticker,
                    'price': None,
                    'news': None,
                    'financials': None
                }
                new_entries.append(new_entity)


            entity.extend(new_entries)
    
    return entity,intent


def get_requirements(intent, entity):
        
    if len(entity) == 0:
        return "none","none"

    required = []
    req = plan_tools(intent, entity)
    
    if intent['compare']:
        intent['basis'] = req
        
    for enty in entity:
        new_req = {
            'entity': enty['ticker'],
            'needs': req
            }
        required.append(new_req)

    return required,intent



def plan_tools(intent, entity):

    emit_event({'type': 'info', 'text': 'Planning tools to execute based on intent and entities'})
    
    plan = []

    if intent['compare']:
        plan = ['price','news','financials']
    
    elif "analysis" in intent['basis']:
        plan = ['financials']

        if len(entity) == 1:
            plan.append('news')
            plan.append('price')        

    elif 'price' in intent['basis']:
        plan.append('price')
    
    elif 'news' in intent['basis']:
        plan.append('news') 

    
    return plan


def api_call(ticker,url):
    
    if not ticker:
        raise Exception('Ticker missing for price fetch')

    api_url = url

    params = { 
        "symbol": ticker,
        "token": 'd6v6jk9r01qig546muf0d6v6jk9r01qig546mufg'
    }

    try:
        response = requests.get(api_url,params=params).json()
        return(response)
    except Exception as ex1:
        print(f"api call failed exception: {ex1}")
        response = 'none'
        return response
    

def get_price(ticker):

    if ticker in memory and 'price' in memory[ticker]:
        return memory[ticker]['price']
    
    api_url = PRICE_API_URL

    response = api_call(ticker,api_url)
    try:
        if response == 'none':
            price = 0
        else:
            price = response['c']
    except Exception as ex2:
        print(f"get_price function exception: {ex2}")
        price = 0

    memory.setdefault(ticker, {})['price'] = price
    return price


def get_news(ticker):
    if not ticker:
        raise Exception('Ticker missing for news fetch')
    
    recent_news = []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q":ticker,
        "searchIn": "title",
        "apiKey": "7edafe2e5d804d59b16f305502fc5c54"
    }


    try: 
        res = requests.get(url, params=params).json()
        i=0
        while i < 6:
            news = (res['articles'][i]['title'])
            recent_news.append(news)
            i += 1
        
        return recent_news
    except Exception as ex3:
        print(f'get_news function exception: {ex3}')
        emit_event({'type': 'error', 'text': f'Failed to fetch news for {ticker}'}) 
        return None 
    
def get_financial_reports(ticker):
    if ticker in memory and 'financials' in memory[ticker]:
        return memory[ticker]['financials']
    annual_data = {}
    api_url = FINANCIAL_REPORT_URL
    response = api_call(ticker,api_url)
    try:
        if response == 'none':
            return annual_data
        else:
            data = response['data']
            current_data = max(data, key=lambda x: x['year'])
            curr_year = current_data['year']
            annual_data[curr_year] = {}
            reports = current_data['report']['bs']

            # for item in data: 
            #     curr_year = item['year']
            #     annual_data[curr_year] = {}
            #     reports = item['report']['bs']
            metric_store = {}
            for details in reports:
                key, score = resolve_metric(details['label'])
                if key:
                    current = metric_store.get(key)
                    if current:
                        current_score = current.get('score', 0)
                    else:
                        current_score = 0
                    if not current or score > current_score:
                        metric_store[key] = {
                            "value": details['value'],
                            "score": score,
                            "label": details["label"]
                        }
                    

            annual_data[curr_year] = {
                k: v['value'] for k, v in metric_store.items()
            }

    except Exception as ex3:
        print(f"get_financial_report function exception: {ex3}")
        return annual_data

    financial_data = compute_metrics(annual_data,curr_year)

    memory.setdefault(ticker, {})['financials'] = financial_data
    return financial_data

def resolve_metric(input):
    label = normalize(input)

    if any(b in label for b in BLACKLIST):
        return None, 0
    

    for key,phrases in EXACT_MATCH.items():

        if any(p == label for p in phrases):
            return key,3
    
    for key,phrases in FUZZY_MATCH.items():

        if any(p in label for p in phrases):
            return key,2
        

    return None,0

def compute_metrics(financials,year):
    
    assets = financials[year].get('assets', 0)
    liabilities = financials[year].get('liabilities', 0)
    cash = financials[year].get('cash', 0)

    try:
        debt_ratio = liabilities/assets
    except:
        debt_ratio = 0
    
    return {
        "assets": assets,
        "liabilities": liabilities,
        "cash": cash,
        "debt_ratio": debt_ratio
    }

def fall_back_price(ticker):
    print(f"Falling back to secondary method for price for {ticker}")
    function = 'TIME_SERIES_DAILY'
    params = {
        'function': function,
        'symbol': ticker,
        'apikey': FALL_API_KEY
    }
    response = requests.get(FALLBACK_API_URL, params=params, headers=HEADERS)
    fallback_price = response
    if response.status_code == 200:
        try:
            data = response.json()
            time_series = data.get('Time Series (Daily)', {})
            if time_series:
                latest_date = sorted(time_series.keys())[-1]
                fallback_price = time_series[latest_date]['4. close']
                fallback_price = float(fallback_price)
            else:
                print(f"No time series data found for {ticker} in fallback API.")
        except Exception as e:
            print(f"Error parsing fallback API response for {ticker}: {e}")

    return fallback_price

def resolve_financial_term(term):
    for key, synonyms in FALL_BACK_EXACT_MATCH.items():
        if term in synonyms:
            return key
    return None

def fall_back_finance(ticker):
    print(f"Falling back to secondary method for finance data for {ticker}")
    function = 'BALANCE_SHEET'
    params = {
        'function': function,
        'symbol': ticker,
        'apikey': FALL_API_KEY
    }
    response = requests.get(FALLBACK_API_URL, params=params, headers=HEADERS)
    if response.status_code == 200:
        try:
            annual_reports = {}
            data = response.json()
            balance_sheet = data.get('annualReports', [])
            if len(balance_sheet) > 0:
                financials = max(balance_sheet, key=lambda x: x['fiscalDateEnding'])
                curr_year = financials['fiscalDateEnding'][:4]
                for key in financials:
                    resolved_term = resolve_financial_term(key)
                    if resolved_term:
                        annual_reports[resolved_term] = financials.get(key)

                financial_data = fall_back_compute_metrics(annual_reports)
            else:
                print(f"No time series data found for {ticker} in fallback API.")
        except Exception as e:
            print(f"Error parsing fallback API response for {ticker}: {e}")
            return {}

    return financial_data

def fall_back_compute_metrics(financials):
    
    assets = float(financials.get('assets', 0))
    liabilities = float(financials.get('liabilities', 0))
    cash = float(financials.get('cash', 0))

    try:
        debt_ratio = liabilities/assets
    except Exception as e:
        print(f"Error computing debt ratio: {e}")
        debt_ratio = 0
    
    return {
        "assets": assets,
        "liabilities": liabilities,
        "cash": cash,
        "debt_ratio": debt_ratio
    }

def fall_back_news(ticker):
    print(f"Falling back to secondary method for news for {ticker}")
    url = FALLBACK_API_URL
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "apikey": FALL_API_KEY
    }

    try:
        res = requests.get(url, params=params).json()
        recent_news = []
        feed = res.get('feed', [])

        top_news = sorted(feed, key=lambda x: datetime.strptime(x['time_published'], '%Y%m%dT%H%M%S'), reverse=True)[:6]
        for items in top_news:
            recent_news.append(items['title'])

        return recent_news
    except Exception as e:
        print(f"Error fetching news from fallback API for {ticker}: {e}")
        return None
                


capabilities = {
    "price": get_price,
    "news": get_news,
    "financials": get_financial_reports
}

fall_back_capabilities = {
    "price": fall_back_price,
    "news": fall_back_news,
    "financials": fall_back_finance
}

def execute_tool(required):
    emit_event(
        {
            'type': 'info',
            'text': 'Executing tools to fetch required data'
        }
    )  
    result_dict = {}
    for entries in required:
        try:
            key_val = entries['entity']
        except KeyError:
            print ('Function: execute_tool -KeyError')
            return {}
        except Exception:
            print(f'Function: execute_tool - {Exception}')
            return {}

        if key_val not in result_dict:
            result_dict[key_val] = {}
        
        needs = entries['needs']
        result_dict[key_val].update(dynamic_tool_execution(key_val, needs))
        
    return result_dict

def compute_confidence(financials):
    financial_confidence = 0

    if financials['assets']: financial_confidence += 1
    if financials['cash']: financial_confidence += 1
    if financials['debt_ratio']: financial_confidence += 1
    
    return financial_confidence

def generate_output(result,intent):
    emit_event({
        'type': 'info',
        'text': 'Generating output based on fetched data and intent'
    })
    generated_output = []
    temp_word = ''
    for ticker,info in result.items():

        if ('price' in intent['basis'] and 'news' in intent['basis'] and 'financials' in intent['basis']) or 'analysis' in intent['basis']:
            financial_confidence = compute_confidence(info['financials'])
            temp_word = f"""
            {ticker}:
            - price: {info['price']} 
            - cash: {info['financials']['cash']}
            - Debt ratio: {info['financials']['debt_ratio']}
            - Assets: {info['financials']['assets']}
            - news: {info['news']} 

            - financial confidence = {financial_confidence}
            """

        elif 'price' in intent['basis']:
            temp_word = f"price of {ticker} is {info['price']}"
        elif 'news' in intent['basis']:
            temp_word = f"news of ticker {ticker} is \n" +  "\n".join(info['news'])  

        generated_output.append(temp_word)

    if intent['compare'] and set(intent['basis']) == {'price','news','financials'}:
        prompt = f''' 
        You're a financial assistant.

        ONLY use the raw data below.
        DO NOT assume or add extra knowledge.

        Data:
        {generated_output}
        
        Task:
        Compare the stocks based ONLY on:

        1. Financial strength (debt ratio, cash)
        2. Current price (relative valuation hint)
        3. News sentiment

        Rules:
        - If one stock clearly stronger → choose it
        - If similar strength → say "similar strength"
        - If one has better price and other has better financial → say "mixed signals"
        - Output should be a single line with name of the stock. This is most important rule. Do NOT output anything else.
        - If mixed signals → say "no clear winner"
        - Do NOT default to insufficient unless truly missing
        No Assumptions
        '''
        final_output = llmcall(prompt)
    
    
    elif 'analysis' in intent['basis']:
        prompt = f''' 
        You're a financial assistant

        ONLY use raw data below. 
        DO NOT assume or add extra knowledge 

        Data: 
        {generated_output}
        
        Task:
        Analyze and give niche results 

        Rules:
        Answer should be based ONLY on the data provided.
        No Assumptions
        With the data provided - Analyze on 3 parameters - financial strength (debt ratio, cash), current price (relative valuation hint), news sentiment.
        If all parameters indicate strong buy → say "strong buy"
        If all parameters indicate strong sell → say "strong sell"
        If mixed signals → say "no clear recommendation" - Use it very very rarely
        Try to provide either buy or sell recommendation based on the data.
        buy, sell, hold, strong buy, strong sell - these are the only outputs allowed.
        The Clear recommendation is most important rule. Do NOT output anything else.
        If data is insufficient, say "insufficient data" 
        '''
        final_output = llmcall(prompt)
    
    else:
        final_output = '\n'.join(generated_output)

    return final_output
    
def validate_financials(financials):
    if not isinstance(financials,dict):
        return False
    
    required_key_fields = ['assets','liabilities','cash','debt_ratio']

    for key in required_key_fields:
        if key not in financials:
            return False
    
    if financials['assets'] <= 0:
        return False
    
    if financials['liabilities'] < 0:
        return False
    
    if financials['cash'] < 0:
        return False
    
    if financials['debt_ratio'] < 0:
        return False
    
    return True

url_dict = {
    "price": PRICE_API_URL,
    "news": NEWS_API_URL,
    "financials": FINANCIAL_REPORT_URL
}

REQUIRED_STATE = {
    'price': lambda x: isinstance(x,(int,float)) and x>0,
    'news': lambda x: isinstance(x,list) and len(x) > 0,
    'financials': lambda x:validate_financials(x)
}

def validate_state(required, result):
    errors = []

    for req in required:
        ticker = req['entity']
        needs = req['needs']

        entity_data = result.get(ticker, {})

        for need in needs:
            rule = REQUIRED_STATE.get(need)
            if rule:
                value = entity_data.get(need)

                try:
                    if not rule(value):
                        errors.append(
                            {
                                'ticker': ticker,
                                'field': need,
                                'error': 'invalid'
                            }
                        )
                except:
                    errors.append(
                        {
                            'ticker': ticker,
                            'field': need,
                            'error': 'exception'
                        }
                    )
        
    return errors 


def recover_state(result, errors):
    retry_count = {}

    for err in errors:
        ticker = err['ticker']
        field = err['field']

        key = f"{ticker}_{field}"
        retry_count[key] = retry_count.get(key,0) + 1

        if retry_count[key] > 1:
            continue

        tool = capabilities.get(field)
        url = url_dict.get(field)

        if tool:
            try:
                result[ticker][field] = tool(ticker,memory,url)
            except:
                continue
        
    return result

def llmcall(prompt):
    client = genai.Client(api_key='AIzaSyBXxSjUUjhw9n8F1NFQXIfFf51sv6RA_EU')
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents={"text": prompt}
    )

    return (response.text)

def promotion_to_alias():
    try:
        with open('user_query.json','r') as file:
            user_data = json.load(file) 
    except Exception as ex_read_user_query_file:
        print(f'LOG: Opening user_query.json in promotion_to_alias function - {ex_read_user_query_file}')
        return
    try:
        with open('alias_map.json','r') as file:
            alias_data = json.load(file)
    except Exception as ex_read_alias_map_file:
        print(f'LOG: Opening alias_map.json in promotion_to_alias function - {ex_read_alias_map_file}')
        return


    updated = False

    for query,info in user_data.items():
        if info['count'] >= 3 and info['confidence'] >= 80:
            resolved = info['resolved']

            if query not in alias_data:
                alias_data[query] = resolved
                print(f"PROMOTION: {query} → {resolved}")
                updated = True
        
    if updated:
        try:
            with open('alias_map.json','w') as f:
                json.dump(alias_data,f,indent=4)
        except Exception as ex_write_alias:
            print(f'LOG: promotion to alias failed and reason is {ex_write_alias}')


def retry_tool(ticker, tool, need):
    retry_count = 0

    output = tool(ticker)
    rule = REQUIRED_STATE.get(need)
    while not rule(output) and retry_count < 2:
        output = tool(ticker)
        retry_count += 1

    return output if rule(output) else None

def read_tool_stats():
    try:
        with open('tool_stats.json','r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        with open('tool_stats.json','w') as file:
            json.dump({}, file)
            return {}
    except Exception as ex_tool_stats_file:
        print(f'LOG: Opening tool_stats.json file - {ex_tool_stats_file}')
        return {}

def write_tool_stats(data):
    try:
        with open('tool_stats.json','w') as file:
            json.dump(data, file, indent=4)
    except Exception as ex_write_tool_stats:
        print(f'LOG: Writing tool_stats.json file - {ex_write_tool_stats}')

def update_tool_stats(need, state, success):
    tool_stats = read_tool_stats()
    if need not in tool_stats:
        tool_stats[need] = {"calls": 0, "successes": 0, "failures": 0,"fallback successes": 0, "fallback failures": 0}

    tool_stats[need]["calls"] += 1

    if success:
        if state == "fallback":
            tool_stats[need]["fallback successes"] += 1
        else:
            tool_stats[need]["successes"] += 1
    else:
        if state == "fallback":
            tool_stats[need]["fallback failures"] += 1
        else:
            tool_stats[need]["failures"] += 1

    write_tool_stats(tool_stats)


def choose_execution_path(need):
        tool_stats = read_tool_stats()
    
        if need in tool_stats:
            stats = tool_stats[need]
            emit_event({
                "type": "info",
                "text": f"Tool stats for {need} - Calls: {stats['calls']}, Success: {stats['successes']}, Failure: {stats['failures']}, Fallback Successes: {stats['fallback successes']}, Fallback Failures: {stats['fallback failures']}"
            })
            if stats['failures'] > 0 and stats['fallback successes'] > 0: 
                if  stats['fallback successes'] / stats['failures'] > 0.5:
                    return "fallback"
        
        return "primary"

def execute_with_retries(ticker, tool, need):
    output = retry_tool(ticker, tool, need)
    if output is not None:
        update_tool_stats(need, "primary", True)
        return output
    else:
        update_tool_stats(need, "primary", False)
        return None

def output_validation(output, need):
    rule = REQUIRED_STATE.get(need)
    if rule and rule(output):
        return True
    return False

def generate_output_with_retries(ticker, url, tool, need, path, max_retries):
    retry_count = 0
    while retry_count < max_retries:
        output = tool(ticker,memory,url)
        if output_validation(output, need):
            update_tool_stats(need, path, True)
            return output
        retry_count += 1

def primary_tool_execution(ticker, need):
    tool = capabilities.get(need)
    if tool:
        url = url_dict.get(need)
        output = generate_output_with_retries(ticker, url, tool, need, "primary", 2)
        if output is not None and output_validation(output, need):
            return output
    return None

def fallback_tool_execution(ticker, need):
    fallback_tool = fall_back_capabilities.get(need)
    if fallback_tool:
        url = FALLBACK_API_URL
        fallback_output = generate_output_with_retries(ticker, url, fallback_tool, need, "fallback", 2)
        if fallback_output is not None and output_validation(fallback_output, need):
            return fallback_output
    return None

def dynamic_tool_execution(ticker, needs):
    result = {}
    for need in needs:
        execution_path = choose_execution_path(need)

        if execution_path == "primary":
            output = primary_tool_execution(ticker, need)
            if output is not None and output_validation(output, need):
                result[need] = output
                continue
            else:
                output = fallback_tool_execution(ticker, need)
                if output is not None and output_validation(output, need):
                    result[need] = output
                    continue
                else:
                    result[need] = None 

        elif execution_path == "fallback":
            output = fallback_tool_execution(ticker, need)
            if output is not None and output_validation(output, need):
                result[need] = output
                continue
            else:
                output = fallback_tool_execution(ticker, need)
                if output is not None and output_validation(output, need):
                    result[need] = output
                    continue
                else:
                    result[need] = None

    return result

def orchestator(query):
    #1. Extract intent and entity
    entity, intent = extract_intent_entity(query)

    #2. Get requirements based on intent and entity
    required, intent = get_requirements(intent, entity)

    if required == "none":
        emit_event({
            "type": "error",
            "text": "Sorry, I couldn't understand your query. Please try again with a different phrasing."
            })
        
        return
    
    #3. Execute tools based on requirements and get results
    result = execute_tool(required)

    #4. Validate state and if errors → recover state
    errors = validate_state(required, result)

    if errors:
        emit_event({
            "type": "error",
            "text": "Tool are having some issues fetching data, please try again later"
        })
        print(f"LOG: validation errors = {errors}")

    #5. Generate output based on result and intent
    output = generate_output(result, intent)

    emit_event({
        "type": "success",
        "text": "Here is the result for your query: "
    })
    emit_event({
        "type": "output",
        "text": output
    })


query = ui.display_ui()

submit_button = StreamlitUI.ui_button("Submit Query")
spinner = StreamlitUI.ui_spinner("Processing your query...")

if submit_button:
    if query.strip() == "":
        emit_event({
            "type": "error",
            "text": "Please enter a valid stock related query."
        })
    else:
        with spinner:
            time.sleep(2)  # Simulate processing time

            orchestator(query)
            

promotion_to_alias()

