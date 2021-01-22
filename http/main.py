from flask import Flask, request, abort
import pkuseg
from segment import segment

server = Flask(__name__)
seg = pkuseg.pkuseg()


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
        if type(text) != str:
            abort(400)
    except KeyError:
        abort(400)
    segmented = segment(seg, text)
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
    except KeyError:
        abort(400)
    if type(sections) != list:
        abort(400)
    segmented_sections = list()
    for section in sections:
        if type(section) != str:
            abort(400)
        segmented_sections.append(segment(seg, section))
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
        if type(text['title']) != str:
            abort(400)
        for i, section in enumerate(text['sections']):
            if type(section['title']) != str or type(section['content']) != str:
                abort(400)
            s = ''
            if i == 0:
                s += text['title']
            s += section['title']
            s += section['content']
            segmented_sections.append(segment(seg, s))
    except KeyError:
        abort(400)
    return {'sections': segmented_sections}


if __name__ == "__main__":
    server.run(host='0.0.0.0', port=8000)
