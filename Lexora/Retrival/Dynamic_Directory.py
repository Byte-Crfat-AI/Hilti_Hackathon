import os
import re
def get_parent_folder_path(path):
    match = re.match(r'^(.*?\\[^\\]+)\\[^\\]+$', path)
    if match:
        return match.group(1)
    return None