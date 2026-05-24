from storage.read_user_query_file import read_user_query_file
from storage.write_user_query_file import write_user_query_file
from models.normalize import normalize

def user_token_log(entity,score,match,logic):
    user_query_log = read_user_query_file()

    print(f'user_query_log: {user_query_log}')

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
