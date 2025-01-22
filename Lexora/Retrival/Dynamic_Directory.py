import os
import re

def get_lexora_path(path):
    match = re.search(r'^(.*\\Lexora)(?:\\|$)', path)
    if match:
        return match.group(1)
    return None

lexora_path = get_lexora_path(os.getcwd())
print(lexora_path)