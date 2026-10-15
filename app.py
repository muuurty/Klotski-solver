from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import io
from PIL import Image
import numpy as np

from cv_utils import detect_pieces_from_image, normalize_pieces
from solver import solve_bfs

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/detect', methods=['POST'])
def api_detect():
    if 'image' not in request.files:
        return jsonify({'error': 'no image uploaded'}), 400
    file = request.files['image']
    data = file.read()
    image = Image.open(io.BytesIO(data)).convert('RGB')
    img = np.array(image)[:, :, ::-1]

    try:
        pieces, debug = detect_pieces_from_image(img, grid_w=4, grid_h=5, debug_mode=False)
    except Exception as e:
        return jsonify({'error': 'cv_failed', 'message': str(e)}), 500

    normalized = normalize_pieces(pieces, grid_w=4, grid_h=5)
    return jsonify({'pieces': normalized, 'grid': {'w': 4, 'h': 5}})


@app.route('/api/solve', methods=['POST'])
def api_solve():
    payload = request.get_json()
    if not payload or 'pieces' not in payload:
        return jsonify({'error': 'invalid_request'}), 400

    pieces = payload['pieces']
    sizes_x = [int(p['w']) for p in pieces]
    sizes_y = [int(p['h']) for p in pieces]
    pos_x = [int(p['x']) for p in pieces]
    pos_y = [int(p['y']) for p in pieces]

    key_index = int(payload.get('key_index', 3))
    goal = payload.get('goal', {'x': 0, 'y': 0})
    goal_x, goal_y = int(goal.get('x', 0)), int(goal.get('y', 0))

    try:
        path, visited_count = solve_bfs(pos_x, pos_y, sizes_x, sizes_y,
                                        key_index=key_index,
                                        goal_x=goal_x, goal_y=goal_y,
                                        grid_w=4, grid_h=5,
                                        steps_limit=200000)
    except Exception as e:
        return jsonify({'error': 'solve_failed', 'message': str(e)}), 500

    out_path = [{'xs': state[0], 'ys': state[1]} for state in path]
    return jsonify({'path': out_path, 'moves': max(0, len(out_path)-1), 'visited': visited_count})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
