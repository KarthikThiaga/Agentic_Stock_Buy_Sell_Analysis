from storage.read_user_query_file import read_user_query_file
from storage.write_user_query_file import write_user_query_file
from models.normalize import normalize

def user_token_log(entity,score,match,logic):
    """Logs and maintains analytics on entity tokens extracted from user queries.

    Tracks historical occurrences of normalized entity tokens by updating an ongoing 
    log file. If an entity token has been processed before, its invocation counter 
    is incremented and its running mean confidence score is dynamically updated. 
    Otherwise, a new tracking record is initialized. The finalized state is then 
    committed back to persistent storage.

    Args:
        entity (str): The raw string token parsed from the user's query text.
        score (int | float): The classification confidence score assigned by the 
            resolving matcher tool.
        match (str): The resolved target value (e.g., stock ticker) associated 
            with the entity.
        logic (str): The specific matching strategy applied to resolve the token 
            (e.g., 'fuzzy' or 'llm').
    """
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
