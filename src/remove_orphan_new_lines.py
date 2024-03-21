import argparse
import json

def remove_orphan_new_lines(opt):
    with open(opt.data, 'r') as file:
        lines = file.readlines()
    #read metadata file
    with open(opt.metadata, 'r') as file:
        metadata = json.load(file)

    candidates_names = list(map(lambda x: x["speech_candidate_id"],metadata["candidates"]))

    #check if a line do not start with any of the candidates names
    new_lines = []
    for line in lines:
        if line.split(',')[0] not in candidates_names:
            new_lines.append(line)
        else:
            #otherwise the line should be appended to the last line after a space
            new_lines[-1] = new_lines[-1].strip() + ' ' + line.strip()
    with open(opt.dest, 'w') as file:
        for line in new_lines:
            file.write(line)
    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/raw/speech.txt', help='source')
    parser.add_argument('--dest', type=str, default='data/without_topics/speech.txt', help='destination')
    parser.add_argument('--metadata', type=str, default='data/metadata/speech.json', help='metadata')
    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    remove_orphan_new_lines(opt)

    

if __name__ == '__main__':
    main()