import argparse
import json
import os

def split_candidate(opt):
    with open(opt.data, 'r') as file:
        lines = file.readlines()
    #read metadata file
    with open(opt.metadata, 'r') as file:
        metadata = json.load(file)
    output_json = metadata.copy()
    for candidate in output_json["candidates"]:
        candidate_name = candidate["speech_candidate_id"]
        candidate_lines = []
        for line in lines:
            if line.startswith(candidate_name.strip()):
                #remove candidate name from line
                line = line.replace(candidate_name.strip(), '')
                candidate_lines.append(line)
        candidate_text = ''.join(candidate_lines)
        candidate["text"] = candidate_text
    
    #create output folder if it does not exist
    folder_dest = opt.dest.split('/')[:-1]
    os.makedirs('/'.join(folder_dest), exist_ok=True)
    #save output json
    with open(opt.dest, 'w') as file:
        json.dump(output_json, file ,ensure_ascii=False,indent=4)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/raw/speech.txt', help='source')
    parser.add_argument('--dest', type=str, default='data/without/topics/speech.txt', help='destination')
    parser.add_argument('--metadata', type=str, default='data/metadata/speech.json', help='metadata')
    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    split_candidate(opt)

    

if __name__ == '__main__':
    main()