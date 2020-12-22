from typing import Set, List

def get_dict_words() -> Set[str]:
    with open('dictionary.txt') as f:
        lines = f.readlines()
    return {line.strip() for line in lines if not line.startswith('#')}


def segment_dict_only(text: str, dict_words: Set[str], segmenter) -> List[str]:
    def seg_rec(s: str) -> List[str]:
        if s in dict_words:
            return [s]
        segments = segmenter.cut(s)
        if len(segments) == 1:
            return [hanzi for hanzi in segments[0]]
        result = list()
        for segment in segments:
            result.extend(seg_rec(segment))
        return result
    return seg_rec(text)
            