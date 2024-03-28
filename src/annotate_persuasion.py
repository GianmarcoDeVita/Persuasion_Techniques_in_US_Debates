import argparse
import json
from dotenv import dotenv_values
import requests
import os

def annotate_persuasion(opt):
    env = dotenv_values()
    endpoint = "https://cloud-api.gate.ac.uk/process/persuasion-classifier-spans"

    #get the dest folder
    folder_dest = opt.dest.split('/')[:-1]
    os.makedirs('/'.join(folder_dest), exist_ok=True)

    #read json file with data
    with open(opt.data, 'r') as file:
        data = json.load(file)
    
    for candidate in data["candidates"]:
        text = candidate["text"]
        if not env["GATE_CLOUD_ID"] or not  env["GATE_CLOUD_PASSWORD"]:
            raise Exception("GATE_CLOUD_ID and GATE_CLOUD_PASSWORD must be set in .env file")
        response = requests.post(endpoint, data=text, auth=(env["GATE_CLOUD_ID"], env["GATE_CLOUD_PASSWORD"]), headers={"Content-Type": "text/plain", "Accept": "application/json"})
        candidate["annotations"] = response.json()
    
    #save output json
    with open(opt.dest, 'w') as file:
        json.dump(data, file ,ensure_ascii=False,indent=4)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/speeches/speech.json', help='source')
    parser.add_argument('--dest', type=str, default='data/annotated/speech.json', help='destination')
    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    annotate_persuasion(opt)

    
if __name__ == '__main__':
    main()