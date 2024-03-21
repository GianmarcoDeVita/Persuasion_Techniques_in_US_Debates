import argparse
from ruamel.yaml import YAML
import os

def remove_topics(opt,params):
    topics = params[opt.topics]
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
            file.write(line)
    print(f"Uniformed dataset saved to {opt.dest}")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/dataset.csv', help='source')
    parser.add_argument('--dest', type=str, default='data/dataset_without_topics.csv', help='destination')
    parser.add_argument('--params', type=str, default='params.yaml', help='params')  # file/folder, 0 for webcam
    parser.add_argument('--topics', type=str, default='topics', help='parameter containing candidates names')
    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    with open(opt.params) as f:
        yaml = YAML(typ="safe")
        params = yaml.load(f) 
    remove_topics(opt, params)

    

if __name__ == '__main__':
    main()