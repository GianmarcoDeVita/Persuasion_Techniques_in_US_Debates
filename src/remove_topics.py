import argparse
import os
import json
def remove_topics(opt):
    #read metadata file
    with open(opt.metadata, 'r') as file:
        metadata = json.load(file)

    topics = metadata["topics"]
    topics_stripped = [topic.strip() for topic in topics]

    #get folder from output file
    folder_dest = opt.dest.split('/')[:-1]
    os.makedirs('/'.join(folder_dest), exist_ok=True)

    with open(opt.data, 'r') as file:
        lines = file.readlines()
    with open(opt.dest, 'w') as file:
        for line in lines:
            if line.strip() in topics_stripped:
                continue
            if line =='\n':
                continue
            file.write(line.strip() + '\n')
    print(f"Uniformed dataset saved to {opt.dest}")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/raw/speech.txt', help='source')
    parser.add_argument('--dest', type=str, default='data/without/topics/speech.txt', help='destination')
    parser.add_argument('--metadata', type=str, default='data/metadata/speech.json', help='metadata')
    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    remove_topics(opt)

    

if __name__ == '__main__':
    main()