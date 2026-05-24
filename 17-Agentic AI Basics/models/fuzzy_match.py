from rapidfuzz import process 

def fuzzy_match(word, choices):
    match, score, _ = process.extractOne(word,choices)
    print (f"LOG: Token {word}, match: {match}, score: {score}")
    if score >= 80:
        logic = 'fuzzy'
        return match, logic, score
    
    return None
