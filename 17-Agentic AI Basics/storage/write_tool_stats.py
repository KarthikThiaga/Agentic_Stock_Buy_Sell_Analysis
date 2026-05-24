import json 
def write_tool_stats(data):
    try:
        with open('tool_stats.json','w',  encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except Exception as ex_write_tool_stats:
        print(f'LOG: Writing tool_stats.json file - {ex_write_tool_stats}')
