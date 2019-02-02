import uuid

from flask import Flask, request
from flask import Response
from flask import session
from flask_restful import Api

from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest

from parser import read_components, read_board

app = Flask(__name__)
api = Api(app)
app.secret_key = 'LJSHDF*O@Y$Ksw9f;32lirF*(Y&.#LI21r40389gy:>IH34'


@app.route('/board/init', methods=['GET'])
def init_board():
    if 'board_ids' not in session:
        print('not in session')
        session['board_ids'] = []
    board_id = str(uuid.uuid4())
    session['board_ids'].append(board_id)
    print(len(session))
    print(len(session['board_ids']))
    return "{'board_id':" + board_id + "}"


@app.route('/board/<string:board_id>/upload/board', methods=['POST'])
def upload_board_file(board_id):
    print(len(session))
    if 'board_ids' not in session:
        return BadRequest('board id list failure')
    if board_id not in session['board_ids']:
        return BadRequest('board_id not found')
    f = request.files['file']
    filename = secure_filename(f.filename)
    f.save(filename)
    session[board_id] = (filename, '')

    return Response('board file uploaded successfully')


@app.route('/board/<string:board_id>/upload/components', methods=['POST'])
def upload_components_file(board_id):
    if 'board_ids' not in session:
        return BadRequest('board id list failure')
    if board_id not in session['board_ids']:
        return BadRequest('board_id not found')
    f = request.files['file']
    filename = secure_filename(f.filename)
    f.save(filename)
    session[board_id] = (session[board_id][0], filename)

    return Response('components file uploaded successfully')


@app.route('/board/<string:board_id>/parse', methods=['GET'])
def parse_board(board_id):
    if 'board_ids' not in session \
            or board_id not in session['board_ids'] \
            or board_id not in session \
            or not session[board_id]:
        return BadRequest('board not initialized properly')
    if session[board_id][0] == '':
        return BadRequest('board file not uploaded')
    if session[board_id][1] == '':
        return BadRequest('components file not uploaded')

    components_file = session[board_id][1]
    components_lines = [line.rstrip('\n') for line in open(components_file)]
    board_file = session[board_id][0]
    board_lines = [line.rstrip('\n') for line in open(board_file)]

    components = read_components(components_lines)
    component_board = read_board(board_lines, components)
    return component_board.to_json()


if __name__ == '__main__':
    app.run(debug=True)
