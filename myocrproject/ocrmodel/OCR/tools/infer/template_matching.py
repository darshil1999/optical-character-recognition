import json
import re
import os
import requests
from bs4 import BeautifulSoup

def synonym(term):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
    return [span.text for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})] 

def find_synonyms(word):
    synonyms = synonym(word)
    if synonyms is None:
        return []
    return synonyms

def match_json_keys(json1, json2, abbreviation_mapping={}, exclude_keys=None):
    expanded_keys1 = set()
    expanded_keys2 = set()

    def expand_keys(obj, expanded_keys):
        if isinstance(obj, dict):
            for key in obj:
                if exclude_keys and key in exclude_keys:
                    continue
                expanded_key = abbreviation_mapping.get(key, key)
                words = re.findall(r'\w+', expanded_key)
                for word in words:
                    expanded_keys.add(word)
                    synonyms = find_synonyms(word)
                    expanded_keys.update(synonyms)
                expand_keys(obj[key], expanded_keys)
        elif isinstance(obj, list):
            for item in obj:
                expand_keys(item, expanded_keys)

    expand_keys(json1, expanded_keys1)
    expand_keys(json2, expanded_keys2)
    
    common_keys = expanded_keys1.intersection(expanded_keys2)
    total_keys = expanded_keys1.union(expanded_keys2)
    
    percentage_matched = len(common_keys) / len(total_keys) * 100
    return common_keys, percentage_matched


def get_matched_percentage(file, template_dir):

    files = os.listdir(template_dir)
    files = [template_dir+'/'+f for f in files if os.path.isfile(template_dir+'/'+f)]

    # File paths for JSON data
    json1_file = file

    json_list_files = files

    # Read JSON data from files
    with open(json1_file, 'r') as f:
        json1 = json.load(f)
    # json1 = json.load(file)

    # for j in json1:
    #     json1 = j
    #     break
    # print(json1)

    json_list = []
    for file in json_list_files:
        with open(file, 'r') as f:
            json_list.append(json.load(f))

    # Abbreviation mapping
    abbreviation_mapping = {
        "nm": "name",
        "c": "city",
        "addr": "address"
    }

    # Exclude keys
    # exclude_keys = ["occupation"]

    max_percentage_matched = 0
    matched_json = None
    matched_json_percentage = {}

    for data in json_list:
        print(f"Matching with {list(data.keys())[0]}....")
        exclude_keys = [data.keys()]
        ck , percentage_matched = match_json_keys(json1, data, exclude_keys= exclude_keys)
        matched_json_percentage[list(data.keys())[0]] = percentage_matched
        if percentage_matched > max_percentage_matched:
            max_percentage_matched = percentage_matched
            matched_json = data


    if matched_json is not None:
        print(f"{list(matched_json.keys())[0]} with the highest matched percentage:")
        # print(json.dumps(matched_json, indent=2))
        print("Percentage matched: %.2f%%" % max_percentage_matched)
        return list(matched_json.keys())[0], max_percentage_matched, matched_json_percentage

    else:
        print("No Template matched from the directory.")
        return "", 0, {}