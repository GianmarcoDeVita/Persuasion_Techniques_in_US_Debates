import argparse
import json
import os

def uniform_candidate_names(opt):
    with open(opt.data, 'r') as file:
        lines = file.readlines()
    #read metadata file
    with open(opt.metadata, 'r') as file:
        metadata = json.load(file)
    #create output folder if it does not exist
    folder_dest = opt.dest.split('/')[:-1]
    os.makedirs('/'.join(folder_dest), exist_ok=True)
    for candidate in metadata["candidates"]:
        old_names = candidate["candidate_raw_names"]
        new_name = candidate["speech_candidate_id"]
        for i in range(len(lines)):
            for name in old_names:
                if name in lines[i]:
                    lines[i] = lines[i].replace(name, new_name)
    with open(opt.dest, 'w') as file:
        for line in lines:
            file.write(line.strip() + '\n')

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/raw/speech.txt', help='source')
    parser.add_argument('--dest', type=str, default='data/without/topics/speech.txt', help='destination')
    parser.add_argument('--metadata', type=str, default='data/metadata/speech.json', help='metadata')
    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    uniform_candidate_names(opt)

    

if __name__ == '__main__':
    main()