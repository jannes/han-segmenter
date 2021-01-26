from typing import Set, List
import regex as re

# matches non-hanzi strings
REGEX_HAN = re.compile('[^\p{Han}]+')

def get_dict_words() -> Set[str]:
    with open('dictionary.txt') as f:
        lines = f.readlines()
    return {line.strip() for line in lines if not line.startswith('#')}


def segment_dict_only(segmenter, text: str, dict_words: Set[str]) -> List[str]:
    def seg_rec(s: str) -> List[str]:
        # non-hanzi single character
        if len(s) == 1 and s not in dict_words:
            return []
        # dictionary word
        if s in dict_words:
            return [s]
        # try to segment further
        segments = segmenter.cut(s)
        result = list()
        # if not further segmented, segment into single characters
        if len(segments) == 1:
            segments = [char for char in segments[0]]
        # recursively segment segmented input
        for segment in segments:
            result.extend(seg_rec(segment))
        return result
    return seg_rec(text)


def segment(segmenter, text: str, dict_only=False, dict_words=None) -> List[str]:
    if dict_only:
        if type(dict_words) is not set:
            raise Exception('need to pass valid dictionary words')
        return segment_dict_only(segmenter, text, dict_words)
    else:
        presegments = re.split(REGEX_HAN, text)
        result = []
        for presegment in presegments:
            result.extend(segmenter.cut(presegment))
        return result