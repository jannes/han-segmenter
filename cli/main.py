import argparse
import sys
import signal
import json

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
        '-j', '--json_filepath',
        help='path to json file that should be segmented',
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

    if args.filepath is None and args.json_filepath is None and args.interactive:
        interactive()
    elif args.filepath is not None and args.json_filepath is None and not args.interactive:
        filemode(args.filepath)
    elif args.json_filepath is not None and args.filepath is None and not args.interactive:
        filemode_json(args.json_filepath)
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


# JSON input schema:
# {
#     "title": <STRING>,
#     "author": <STRING>,
#     "chapters": [{"title": <STRING>, "content": <STRING>}, ...]
# }
# JSON output schema:
# {
#     "title_cut": [<STRING>, ...],
#     "chapter_cuts": [{"title": <STRING>, "cut": [<STRING>, ...]}, ...]
# }
def filemode_json(book_json_filepath: str):
    seg = pkuseg()
    with open(book_json_filepath, encoding='utf8') as f:
        book = json.load(f)
    title = book['title']
    author = book['author']
    chapters = book['chapters']

    book_cut = segment(seg, title, DICT_ONLY, DICT_WORDS)
    book_cut.extend(segment(seg, author, DICT_ONLY, DICT_WORDS))
    chapters_output = []
    for chapter in chapters:
        chapter_title = chapter['title']
        chapter_content = chapter['content']
        cut = segment(seg, chapter_title, DICT_ONLY, DICT_WORDS)
        content_cut = segment(seg, chapter_content, DICT_ONLY, DICT_WORDS)
        cut.extend(content_cut)
        chapter_output = {'title': chapter_title, 'cut': cut}
        chapters_output.append(chapter_output)

    print(json.dumps({'title_cut': book_cut, 'chapter_cuts': chapters_output}, indent=4, ensure_ascii=False))
    

if __name__ == '__main__':
    main()
