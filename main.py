from flask import Flask, request, abort
import pkuseg

server = Flask(__name__)
seg = pkuseg.pkuseg()


@server.route('/segment', methods=['POST'])
def segment():
    body = request.get_json()
    if body is None or 'text' not in body:
        abort(400)
    if 'text' in body:
        text = body['text']
        segmented = seg.cut(text)
        return {'segmented': segmented}


if __name__ == "__main__":
    server.run(host='0.0.0.0', port=8000)
