import re
import re
import json

def extractor(json_data):
    if isinstance(json_data, dict):  
        text = json.dumps(json_data)  # Convert JSON (dict) to string
    elif isinstance(json_data, list):  
        text = " ".join(map(str, json_data))  # Convert list to string
    else:
        text = str(json_data)  # Ensure text is a string

    email_match = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    name_match = re.search(r'Name:[\w\s]+',text)
    if email_match:
        print("Found Emails:", email_match)
        print("Names",name_match)

    else:
        print("No email found.")


