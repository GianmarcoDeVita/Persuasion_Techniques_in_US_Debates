import argparse
from ruamel.yaml import YAML

def remove_empty_new_lines(opt, params):
    with open(opt.data, 'r') as file:
        lines = file.readlines()

    candidates_names = params[opt.candidates_param]

    #check if a line do not start with any of the candidates names
    new_lines = []
    for line in lines:
        if line.split(',')[0] not in candidates_names:
            new_lines.append(line)
        else:
            #otherwise the line should be appended to the last line after a space
            new_lines[-1] = new_lines[-1].strip() + ' ' + line.strip()
    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/dataset.csv', help='source')
    parser.add_argument('--dest', type=str, default='data/uniformed_dataset.csv', help='destination')
    parser.add_argument('--params', type=str, default='params.yaml', help='params')  # file/folder, 0 for webcam
    parser.add_argument('--candidates_param', type=str, default='trump_biden', help='parameter containing candidates names')
    opt = parser.parse_args()
    return opt

def main():
    opt = parse_arguments()
    with open(opt.params) as f:
        yaml = YAML(typ="safe")
        params = yaml.load(f) 
    remove_empty_new_lines(opt, params)

    

if __name__ == '__main__':
    main()