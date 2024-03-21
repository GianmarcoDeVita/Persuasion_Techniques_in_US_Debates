import argparse
import json

def uniform_candidate_names(opt):
    with open(opt.data, 'r') as file:
        lines = file.readlines()
    #read metadata file
    with open(opt.metadata, 'r') as file:
        metadata = json.load(file)

    for candidate in metadata["candidates"]:
        old_name = candidate["candidate_raw_name"]
        new_name = candidate["speech_candidate_id"]
        for i in range(len(lines)):
            lines[i] = lines[i].replace(old_name, new_name)
    with open(opt.dest, 'w') as file:
        for line in lines:
            file.write(line)

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