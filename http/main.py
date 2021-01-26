from flask import Flask, request, abort
import pkuseg
from segment import segment, get_dict_words

server = Flask(__name__)
seg = pkuseg.pkuseg()
dict_words = get_dict_words()


# JSON input schema:
# {
#     "text": <STRING>
# }
# JSON output schema:
# {
#     "text": [<STRING>, ...]
# }
@server.route('/segmentString', methods=['POST'])
def segment_single():
    body = request.get_json()
    try:
        text = body['text']
        dict_only = body['dict_only']
        if type(text) != str or type(dict_only) != bool:
            abort(400)
    except KeyError:
        abort(400)
    segmented = segment(seg, text, dict_only, dict_words)
    return {'text': segmented}


# JSON input schema:
# {
#     "sections": [<STRING>, ...]
# }
# JSON output schema:
# {
#     "sections": [[<STRING>, ...], ...]
# }
@server.route('/segmentStrings', methods=['POST'])
def segment_multiple():
    body = request.get_json()
    try:
        sections = body['sections']
        dict_only = body['dict_only']
    except KeyError:
        abort(400)
    if type(sections) != list or type(dict_only) != bool:
        abort(400)
    segmented_sections = list()
    for section in sections:
        if type(section) != str:
            abort(400)
        segmented_sections.append(segment(seg, section, dict_only, dict_words))
    return {'sections': segmented_sections}


# JSON input schema:
# {
#     "title": <STRING>,
#     "sections": [
#         {"title": <STRING>, "content": <STRING>},
#         ...
#     ]
# }
# JSON output schema:
# {
#     "sections": [[<STRING>, ...], ...]
# }
@server.route('/segmentText', methods=['POST'])
def segment_book():
    text = request.get_json()
    segmented_sections = list()
    try:
        if type(text['title']) != str or type(text['dict_only']) != bool:
            abort(400)
        for i, section in enumerate(text['sections']):
            if type(section['title']) != str or type(section['content']) != str:
                abort(400)
            s = ''
            if i == 0:
                s += text['title']
            s += section['title']
            s += section['content']
            segmented_sections.append(segment(seg, s, text['dict_only'], dict_words))
    except KeyError:
        abort(400)
    return {'sections': segmented_sections}


if __name__ == "__main__":
    server.run(host='0.0.0.0', port=8000)
