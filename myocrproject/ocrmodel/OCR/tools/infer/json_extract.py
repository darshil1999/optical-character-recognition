import openai
import os
import json
import time
from config.config import key

# Set the maximum number of requests allowed per minute
MAX_REQUESTS = 3
# Set the time window duration in seconds (1 minute = 60 seconds)
TIME_WINDOW = 60
# Store the timestamps of recent requests
request_times = []
openai.api_key = key

def allow_request():
    current_time = time.time()
    # Remove timestamps older than the time window
    request_times[:] = [timestamp for timestamp in request_times if current_time - timestamp <= TIME_WINDOW]
    # Check the number of requests within the time window
    if len(request_times) < MAX_REQUESTS:
        request_times.append(current_time)
        return True
    else:
        return False

def get_json(savepath, filepath):
    if os.path.isdir(filepath):
        files = os.listdir(filepath)
        files = [f for f in files if os.path.isfile(filepath+'/'+f)]
        basename = files[-1]
        filename = os.path.splitext(basename)[0]
        file = open(os.path.join(savepath + "/json", filename + "_text.json"))
    else:
        basename = os.path.basename(filepath)
        filename = os.path.splitext(basename)[0]
        file = open(os.path.join(savepath + "/json", filename + "_text.json"))

    raw_json = json.load(file)
    answer = {}
 
    for input_json in raw_json:
        print("Extracting json " + list(input_json.keys())[0])

        while not allow_request():
            time.sleep(1)

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo', 
            messages=[{"role": "user", "content":f"{input_json} get me the important fields in key value pairs in json format. Do not include any explanations, only provide a RFC8259 compliant JSON response without deviation.Check if the text have any possible rows of columns if any, then make the nested json of rows"}],
            temperature=0
        )
      
        res = response['choices'][0]['message']['content']
        try:
            res = json.loads(res)
        except Exception as e:
            print("No Key Value Pairs Found.")
            res = {}
        answer[str(list(input_json.keys())[0])] = res

    file.close()

    #Storing the result in the file
    result_json = json.dumps(answer, ensure_ascii=False)
    out_path = os.path.join(savepath + "/json", filename + "_result.json")
    out_file = open(out_path, "w")
    out_file.write(result_json)
    out_file.close()

    return result_json, out_path