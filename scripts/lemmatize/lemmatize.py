import argparse
import subprocess
import time

from collections import deque
from string import punctuation

from trankit import Pipeline
from tqdm import tqdm

def count_lines(input_file):
    result = subprocess.run(['wc', '-l', input_file], capture_output=True, text=True)
    return int(result.stdout.strip(' ').split(' ')[0])

def main():
    tic = time.time()
    parser = argparse.ArgumentParser(description="Lemmatize plaintext file")
    parser.add_argument('-l', '--language', type=str, required=True, help='Language to use (fi/en)')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file')

    args = parser.parse_args()

    
    input_file = args.input
    output_file = args.output

    if args.language == 'en':
        language = 'english'
    elif args.language == 'fi':
        language = 'finnish'
    else:
        print('unknown language')
        exit(1)

    line_amt = count_lines(input_file)
    lines = deque()

    # load all lines into memory
    with open(input_file, 'r') as f:
        for line in f:
            lines.append(line.rstrip('\n'))
    
    lemmas = set()

    # lemmatize all lines
    p = Pipeline(language)
    for i in tqdm(range(line_amt)):
        line = lines.popleft()
        if line == '': continue  # strip empty lines
        lemmatized = p.lemmatize(line, is_sent=True)
        for token in lemmatized['tokens']:
            try:
                lemmas.add(token['lemma'].lower().replace('#', ''))  # trankit likes to leave # signs in composite words
            except KeyError:
                continue

    with open(output_file, 'w') as f:
        # write lemmas into output_file
        for item in lemmas:
            if item not in set(punctuation):  # don't write singular punctuation lemmas
                f.write(f'{item}\n')
            else:
                continue

    toc = time.time()
    print(f'done in {toc-tic} s')

if __name__ == "__main__":
    main()