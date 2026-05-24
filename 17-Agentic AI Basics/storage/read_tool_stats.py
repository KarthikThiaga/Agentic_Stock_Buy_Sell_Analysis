
import json


def read_tool_stats():
    try:
        with open('tool_stats.json','r') as file:
            content = file.read()
            data = json.loads(content)
            return data
    except FileNotFoundError:
        with open('tool_stats.json','w') as file:
            json.dump({}, file)
            return {}
    except Exception as ex_tool_stats_file:
        print(f'LOG: Opening tool_stats.json file - {ex_tool_stats_file}')
        return {}
