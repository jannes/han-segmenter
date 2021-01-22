import argparse
import sys
import signal

from pkuseg import pkuseg
from segment import get_dict_words, segment

DICT_ONLY = False
DICT_WORDS = None

def main():
    global DICT_ONLY
    global DICT_WORDS
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--filepath',
        help='path to text file that should be segmented',
        type=str)
    parser.add_argument(
        '-i', '--interactive',
        help=('run in interactive mode, get input from stdin, '
              'segment each sentence, delimited by 。'),
        action='store_true')
    parser.add_argument(
        '-d', '--dict_only',
        help='segment to only dictionary words',
        action='store_true')
    args = parser.parse_args()
    if args.dict_only:
        DICT_ONLY = True
        DICT_WORDS = get_dict_words()

    if args.filepath is None and args.interactive:
        interactive()
    elif args.filepath is not None and not args.interactive:
        filemode(args.filepath)
    else:
        stdin_once(pkuseg())


def signal_handler(sig, frame):
    sys.exit(0)


def stdin_once(seg):
    input_str = sys.stdin.read()
    segmented = segment(seg, input_str, DICT_ONLY, DICT_WORDS)
    for word in segmented:
        print(word)


def interactive():
    signal.signal(signal.SIGINT, signal_handler)
    seg = pkuseg()
    while True:
        stdin_once(seg)


def filemode(filepath: str):
    seg = pkuseg()
    with open(filepath) as f:
        input_str = f.read()
    segmented = segment(seg, input_str, DICT_ONLY, DICT_WORDS)
    for word in segmented:
        print(word)
    

if __name__ == '__main__':
    main()
